from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    class Meta: # Что бы конкретно что-то выводилось на нашу страницу, какие поля попадали в элементы формы, нужен класс Meta.
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags'] # какие поля попадут в форму