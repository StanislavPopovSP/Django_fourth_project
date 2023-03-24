from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import logout # есть готовый элемент который делает разлогинивание


def login_user(request):
    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request) # доп модуль для выхода
    return redirect('login')


def profiles(request):
    prof = Profile.objects.all()
    context = {'profiles': prof}
    return render(request, 'users/index.html', context)


def user_profile(request, pk):
    prof = Profile.objects.get(id=pk)

    top_skill = prof.skill_set.exclude(description__exact="") # Исключаю элементы у которых описание пустое. description__exact="" - исключить элементы, которые будут содержать пустую строку(в виде описания).
    other_skills = prof.skill_set.filter(description="") # Будем выводить элементы с пустым описанием

    context = {
        'profile': prof,
        'top_skills': top_skill,
        'other_skills': other_skills,
    }
    return render(request, 'users/profile.html', context)


