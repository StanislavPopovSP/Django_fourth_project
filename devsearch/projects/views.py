from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required # Декоратор для того что бы только пользователь смог что то делать

def projects(request):
    """Функция, отвечает за доступ ко всем объектам таблицы"""
    pr = Project.objects.all()
    context = {'projects': pr}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    """Функция, отвечает за доступ конкретного поля таблицы"""
    project_obj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': project_obj})

@login_required(login_url='login') # перенаправляет на страницу незарегистрированного пользователя
def create_project(request):
    """Функция, отвечает за создание какого-то проекта, для авторизированного пользователя."""
    profile = request.user.profile # привяжем профиль пользователя к данной форме
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid(): # проверяется валидность введенных данных, встроенная проверка.
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account') # перенаправим на какую-то страницу

    context = {'form': form}
    return render(request, 'projects/form-template.html', context)
