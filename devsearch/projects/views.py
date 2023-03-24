from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm

def projects(request):
    """Функция, отвечает за доступ ко всем объектам таблицы"""
    pr = Project.objects.all()
    context = {'projects': pr}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    """Функция, отвечает за доступ конкретного поля таблицы"""
    project_obj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': project_obj})


def create_project(request):
    """Функция, отвечает за отправку данных какого-то проекта"""
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid(): # проверяется валидность введенных данных, встроенная проверка.
            form.save()
            return redirect('projects') # перенаправим на какую-то страницу

    context = {'form': form}
    return render(request, 'projects/form-template.html', context)
