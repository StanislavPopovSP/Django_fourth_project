from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import logout, login, authenticate  # есть готовый элемент который делает разлогинивание
from django.contrib.auth.models import User  # Нужно связать БД пользователей кот-я есть с моделью пользователей.
from django.core.exceptions import ObjectDoesNotExist  # Нужно предусмотреть ошибку если пользователя не будет в БД. ObjectDoesNotExist - объект не существует.
from django.contrib import messages  # Через ошибки message, можно вывести информацию для пользователя.
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required  # для закрытия доступа, незарегистрированных пользователей.
from .utils import search_profiles


def login_user(request):
    # Проверяет аутентификацию пользователя и отправляет данные для авторизации.
    # if request.user.is_authenticated:
    #     return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Хотим получить данные из модели по этому имени. Проверку сделать.
        # try:
        #     user = User.objects.get(username=username)  # проверяем пользователя, если все ок, он уникальный
        # except ObjectDoesNotExist:  # если не ок
        #     messages.error(request, 'Username does not exists')

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
    """Доступ к данным профиля, какого-то пользователя через функцию search_profiles, которая осуществляет еще поиск разработчиков."""
    prof, search_query = search_profiles(request)  # будет возвращать кортеж с данными, распаковываем в две переменные

    context = {
        'profiles': prof,
        'search_query': search_query
    }
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


@login_required(login_url='login')
def create_skill(request):
    """Добавления навыков"""
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)  # мы получаем все данные кот-е будут отправляться методом POST
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile  # связываем владельца скиллов с профилем
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    """Редактирования навыков"""
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)  # мы получаем все данные кот-е будут отправляться методом POST, что бы эти данные привязывались к конкретному пользователю.
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was update successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    """Удаление навыков"""
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}

    return render(request, 'users/delete.html', context)


@login_required(login_url='login')
def inbox(request):
    """Доступ к сообщениям зарегистрированного пользователя"""
    profile = request.user.profile
    messages_requests = profile.messages.all()  # message_requests = # из таблицы Message достаем все данные по имени related_name='messages'. Относительно пользователя достаем эти сообщения, что бы другие пользователи эти сообщения не видели.
    # подсчёт прочитанных и не прочитанных сообщений
    unread_count = messages_requests.filter(is_read=False).count()

    context = {
        'messages_requests': messages_requests,  # все сообщения
        'unread_count': unread_count  # не прочитанные
    }

    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def view_message(request, pk):
    """Открывает сообщение пользователя"""
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read is False:
        message.is_read = True
        message.save()

    context = {
        'message': message
    }

    return render(request, 'users/message.html', context)


def create_message(request, pk):
    """Для заполнения и отправки сообщения"""
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    # Что бы не было ошибки при поиске отправителя
    try:
        sender = request.user.profile
    except: # если пользователь не может получить данные
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST) # в данном поле пользователь будет вводить данные
        if form.is_valid(): # проверка валидации
            message = form.save(commit=False)
            message.sender = sender # если валидные данные, то что бы сохранился отправитель
            message.recipient = recipient # сохраняем получателя

            if sender: # Если отправитель существует, у него только будет работать
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully send!')
            return redirect('user_profile', pk=recipient.id)


    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', context)
