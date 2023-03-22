from django.db import models
from django.contrib.auth.models import User  # Модель самого пользователя есть в самом django


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Один профиль пользователя может быть связан с одним зарегистрированным пользователем, у которого могут быть проекты и т.д. Что бы одна регистрационная учётка соответствовала одному профилю пользователя.
    # В админке у нас есть пользователи, но нам надо как то связать с профилем пользователя, как бы пользователь это одно, а профиль пользователя, что бы его можно было какими-то данными наполнять его профиль. У пользователя может быть свой профиль, в котором могут быть более расширенные данные.
    # Когда мы пользователя зарегистрировали он попадает в общую модель пользователей, которая есть уже в django, и что бы профиль пользователя, его личные данные могли связываться только с этим одним полем.
    # null=True, blank=True что бы если пользователь создан, учётная запись могла быть пустой.
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)  # что бы у него проходила валидация от самого django
    username = models.CharField(max_length=200, blank=True, null=True)
    short_info = models.CharField(max_length=200, blank=True, null=True)  # краткое описание
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}'


class Skill(models.Model):
    """Модель, отвечающая за навыки пользователя"""
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True) # имя самого навыка
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'