from django.shortcuts import render
from .models import Profile


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
