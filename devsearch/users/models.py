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
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)  # Владелец скилов.
    name = models.CharField(max_length=200, blank=True, null=True)  # имя самого навыка
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    """Для отправки сообщения"""
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True) # отправитель
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages') # получатель, related_name - имя по кот-му мы сможем обратиться к данному полю, если какое-то поле по внешнему ключу мы хотим получать доступ, мы к нему не добавляли _set, в место этого мы можем обратиться по этому имени.
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True) # работает как CharField, только валидация будет на ввод email, что бы была @ и один символ после собачки.
    subject = models.CharField(max_length=200, null=True, blank=True) # тема письма
    body = models.TextField() # тело сообщения, поле обязательное для заполнения
    is_read = models.BooleanField(default=False, null=True) # нужно как-то отслеживать сообщение прочитано или нет, есть два состояния, либо прочитано, лио нет. По умолчанию не прочитанное сообщение. null=True - и уже программно будет, что сообщение прочитано.
    created = models.DateTimeField(auto_now_add=True) # Дата создания этого сообщения

    def __str__(self):
        return f'{self.subject}'

    # Надо что бы в Админке в какой-то последовательности выводились поля.
    class Meta:
        """Сортировка полей"""
        ordering = ['is_read', '-created'] # Сначала прочитанные или нет, что бы непрочитанные были вверху. По дате создания.