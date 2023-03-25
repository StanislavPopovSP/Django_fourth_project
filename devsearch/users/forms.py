from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """Класс, отвечает за создание своей формы, для регистрации пользователя"""

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
