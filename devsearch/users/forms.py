from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill
from django.forms import ModelForm # что бы данные брались из нашей модели


class SkillForm(ModelForm):
    """Для добавления навыков"""
    class Meta:
        model = Skill
        fields = '__all__' # Можем взять из модели все поля
        exclude = ['owner'] # Исключаем поля которые нам не нужны

    def __init__(self, *args, **kwargs):
        """Инициализатор будет использовать любые элементы из родительского элемента, через наследование родительского класса."""
        super().__init__(*args, **kwargs)  # наследуемся от ModelForm
        # .widget.attrs.update - виджеты, атрибуты, обновить(в виде словаря передать любые атрибуты которые мы хотим)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    """Форма для редактирования пользователя """
    class Meta:
        model = Profile # Данные будем брать из модели Profile
        fields = ['name', 'email', 'username',
                  'bio', 'short_info', 'profile_image',
                  'social_github', 'social_youtube',
                  'social_website'] # разрешаем редактировать

    def __init__(self, *args, **kwargs):
        """Инициализатор будет использовать любые элементы из родительского элемента, через наследование родительского класса."""
        super().__init__(*args, **kwargs)  # наследуемся от ModelForm
        # .widget.attrs.update - виджеты, атрибуты, обновить(в виде словаря передать любые атрибуты которые мы хотим)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class CustomUserCreationForm(UserCreationForm):
    """Форма, для регистрации пользователя"""

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        """Инициализатор будет использовать любые элементы из родительского элемента, через наследование родительского класса."""
        super().__init__(*args, **kwargs)  # наследуемся от ModelForm
        # .widget.attrs.update - виджеты, атрибуты, обновить(в виде словаря передать любые атрибуты которые мы хотим)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
