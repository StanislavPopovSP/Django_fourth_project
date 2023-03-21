from django.shortcuts import render
from .models import Project

def projects(request):
    pr = Project.objects.all()
    context = {'projects': pr}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    """Функция, будет возвращать страницу просмотра отдельного проекта"""
    project_obj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': project_obj})
