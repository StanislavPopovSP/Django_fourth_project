from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import logout, login, authenticate  # есть готовый элемент который делает разлогинивание
from django.contrib.auth.models import User  # Нужно связать БД пользователей кот-я есть с моделью пользователей.
from django.core.exceptions import ObjectDoesNotExist  # Нужно предусмотреть ошибку если пользователя не будет в БД. ObjectDoesNotExist - объект не существует.
from django.contrib import messages  # Через ошибки message, можно вывести информацию для пользователя.
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required  # для закрытия доступа, незарегистрированных пользователей.


def login_user(request):
    # Проверяет аутентификацию пользователя и отправляет данные для авторизации.
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Хотим получить данные из модели по этому имени. Проверку сделать.
        try:
            user = User.objects.get(username=username)  # проверяем пользователя, если все ок, он уникальный
        except ObjectDoesNotExist:  # если не ок
            messages.error(request, 'Username does not exists')

        user = authenticate(request, username=username, password=password)  # сохраняем
        if user is not None:  # если пользователь уникальный, авторизируй.
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def register_user(request):
    """Отвечает за регистрацию пользователя"""
    page = 'register'
    form = CustomUserCreationForm()  # получили внешний вид

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # указываем аргументы, которые будут вводиться пользователем
        if form.is_valid():  # если данные введенные валидные, то -->
            user = form.save(commit=False)  # данные сохранились commit=False
            user.username = user.username.lower()  # переведем данные в нижний регистр(user будет отправляться в БД в нижнем регисте), что бы не привязываться к регистру(если брать данные).
            user.save()
            login(request, user)  # После сохранения пользователя в БД, логиним пользователя.
            messages.success(request, 'User account was created!')
            return redirect('profiles')  # И укажем страницу куда нужно перенаправить пользователя после того как зарегистрировался.

        else:
            messages.error(request, 'An error has occurred during registration')  # ошибка при регистрации

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    """Отвечает за кнопку выхода"""
    logout(request)
    messages.error(request, 'User was logged out!')
    return redirect('login')


def profiles(request):
    """Доступ ко всем объектам профиля, какого-то пользователя"""
    prof = Profile.objects.all()
    context = {'profiles': prof}
    return render(request, 'users/index.html', context)


def user_profile(request, pk):
    """Отвечает за доступ конкретного поля таблицы"""
    prof = Profile.objects.get(id=pk)

    top_skill = prof.skill_set.exclude(description__exact="")  # Исключаю элементы у которых описание пустое. description__exact="" - исключить элементы, которые будут содержать пустую строку(в виде описания).
    other_skills = prof.skill_set.filter(description="")  # Будем выводить элементы с пустым описанием

    context = {
        'profile': prof,
        'top_skills': top_skill,
        'other_skills': other_skills,
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')  # login_url='login' - если не зарегистрировал что бы перенаправляло на данную страницу
def user_account(request):
    """ Отвечает за меню, поле мой аккаунт"""
    prof = request.user.profile  # сюда будем сохранять из пользователей профиль пользователя.
    skills = prof.skill_set.all()  # скилы аккаунта
    projects = prof.project_set.all()  # проекты аккаунта
    context = {
        'profile': prof,
        'skills': skills,
        'projects': projects
    }

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    """Выводит форму для редактирования пользователя и отправляет данные в БД"""
    profile = request.user.profile
    form = ProfileForm(instance=profile)  # что бы в форме были уже данные пользователя из его профиля.

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # сохраняем в форму всё что приходит методом POST и FILE, что бы эти данные привязывались к конкретному пользователю.
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)
