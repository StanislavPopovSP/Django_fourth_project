from django.forms import ModelForm
from .models import Project
from django import forms # для изменения в форме поля Tags

class ProjectForm(ModelForm):
    class Meta: # Что бы конкретно что-то выводилось на нашу страницу, какие поля попадали в элементы формы, нужен класс Meta.
        model = Project # Данные будем брать из модели Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags'] # какие поля попадут в форму

        widgets = {
            'tags': forms.CheckboxSelectMultiple()  # Вывел Checkbox поле теги
        }

        # Добавим к форме стили которые предустановлены.
    def __init__(self, *args, **kwargs):
        """Инициализатор будет использовать любые элементы из родительского элемента, через наследование родительского класса."""
        super().__init__(*args, **kwargs) # наследуемся от ModelForm
        # .widget.attrs.update - виджеты, атрибуты, обновить(в виде словаря передать любые атрибуты которые мы хотим)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # Что бы каждое поле не прописывать сделаем цикл for
        # self.fields['title'].widget.attrs.update({'class': 'input'})  # Что бы внешний вид формы поменялся, нужно иметь возможность из род-го класса испоьзовать какие-то виджеты и их атрибуты.
        # self.fields['description'].widget.attrs.update({'class': 'input'})  # Что бы внешний вид формы поменялся, нужно иметь возможность из род-го класса испоьзовать какие-то виджеты и их атрибуты.