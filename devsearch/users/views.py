from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import logout, login, authenticate  # есть готовый элемент который делает разлогинивание
from django.contrib.auth.models import User  # Нужно связать БД пользователей кот-я есть с моделью пользователей.
from django.core.exceptions import ObjectDoesNotExist  # Нужно предусмотреть ошибку если пользователя не будет в БД. ObjectDoesNotExist - объект не существует.


def login_user(request):
    # Функция, проверяет аутентифицирован пользователь или нет и отправляет данные для авторизации.
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Хотим получить данные из модели по этому имени. Проверку сделать.
        try:
            user = User.objects.get(username=username) # проверяем пользователя, если все ок, он уникальный
        except ObjectDoesNotExist: # если не ок
            print('Username does not exists')

        user = authenticate(request, username=username, password=password) # сохраняем
        if user is not None: # если пользователь уникальный, авторизируй.
            login(request, user)
            return redirect('profiles')
        else:
            print('Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logout_user(request):
    """Функция, отвечает за кнопку выхода"""
    logout(request)
    return redirect('login')


def profiles(request):
    """Функция, за доступ ко всем объектам профиля, какого-то пользователя"""
    prof = Profile.objects.all()
    context = {'profiles': prof}
    return render(request, 'users/index.html', context)


def user_profile(request, pk):
    """Функция, отвечает за доступ конкретного поля таблицы"""
    prof = Profile.objects.get(id=pk)

    top_skill = prof.skill_set.exclude(description__exact="")  # Исключаю элементы у которых описание пустое. description__exact="" - исключить элементы, которые будут содержать пустую строку(в виде описания).
    other_skills = prof.skill_set.filter(description="")  # Будем выводить элементы с пустым описанием

    context = {
        'profile': prof,
        'top_skills': top_skill,
        'other_skills': other_skills,
    }
    return render(request, 'users/profile.html', context)
