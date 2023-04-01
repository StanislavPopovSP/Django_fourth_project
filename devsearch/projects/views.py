from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required  # Декоратор для того что бы только пользователь смог что то делать
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  # Для работы с пагинацией страниц PageNotAnInteger - работа с ошибками EmptyPage - пустая страница.
from django.contrib import messages


def projects(request):
    """Доступ ко всем объектам таблицы, пагинация"""
    pr = Project.objects.all()
    page = request.GET.get('page') # нужно создать страницу (получаем данные методом get саму страницу)
    results = 3 # сколько результирующих элементов будет на странице
    paginator = Paginator(pr, results) # кол-во элементов из всех данных которые мы берем.

    try:
        pr = paginator.page(page) # получаем саму страницу (если страниц несколько, то будем присваивать все страницы)
    except PageNotAnInteger: # если страниц не найдено
        page = 1 # если других страниц не будет, страница должна быть только одна. (если больше числовых значений не найдено, то присваиваем 1 )
        pr = paginator.page(page)
    except EmptyPage: # если страница пустая
        page = paginator.num_pages  # .num_pages - что бы кол-во страниц приходило(если 0, то значит 0).
        pr = paginator.page(page)

    # Сделаем кол-во отображаемых страниц в пагинаторе.
    left_index = int(page) - 4 # Что бы 4 элемента оставалась только видимых

    if left_index < 1: # это значит нету страниц
        left_index = 1 # Это когда будем переходить по стрелке в лево left_index = 1 - что бы не мог перейти на отрицательную страницу.

    right_index = int(page) + 5

    if right_index > paginator.num_pages: # .num_pages - кол-во страниц которое есть в данном случае.
        right_index = paginator.num_pages + 1

    # Кол-во страниц пагинации
    custom_range = range(left_index, right_index)

    context = {
        'projects': pr,
        'paginator': paginator,
        'custom_range': custom_range
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    """Функция, отвечает за доступ конкретного поля таблицы, обработка комментариев"""
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False) # данные в БД не попадают
        review.project = project_obj # Наш отзыв привязывается к конкретному проекту
        review.owner = request.user.profile # привязываем владельца к профилю пользователя
        review.save() # данные сохранили в БД

        project_obj.get_vote_count() # перезаписываем project_obj

        messages.success(request, 'Your review was successfully submitted!') # если все ок
        return redirect('project', pk=project_obj.id)

    context = {
        'project': project_obj,
        'form': form
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')  # перенаправляет на страницу незарегистрированного пользователя
def create_project(request):
    """Функция, отвечает за создание какого-то проекта, для авторизированного пользователя."""
    profile = request.user.profile  # привяжем профиль пользователя к данной форме
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():  # проверяется валидность введенных данных, встроенная проверка.
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')  # перенаправим на какую-то страницу

    context = {'form': form}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    """Редактирует проект пользователя."""
    profile = request.user.profile
    project = profile.project_set.get(id=pk)  # нужно получить данные по профилю пользователя.
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        new_tags = request.POST.get('tags').replace(',', ' ').split() # получаем список тегов, заменили на пробельный символ, разбили по пробельному символу по умолчанию.
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)  # будет возвращать либо тег кот-й сущ-ет, либо которого нету(новый) Метод get_or_create - получить или создать.
                project.tags.add(tag)
            return redirect('account')

    context = {
        'form': form,
        'project': project
    }

    return render(request, 'projects/form-template.html', context)

@login_required(login_url='login')
def delete_project(request, pk):
    """Удаляет проект пользователя"""
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'object': project}

    return render(request, 'projects/delete.html', context)
