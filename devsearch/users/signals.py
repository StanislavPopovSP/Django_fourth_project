from django.db.models.signals import post_save  # post_save - сохранение данных. Сигналы уведомления в админке. Нам надо что бы когда создавался пользователь, что бы профиль создавался автоматически.
from django.db.models.signals import post_delete
from django.dispatch import receiver  # декоратор для подключения
from .models import Profile
from django.contrib.auth.models import User


# sender - отправитель
# instance - как экземпляр текущий
# created - созданный, если профиль был создан.
# **kwargs - набор именованных параметров.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Функция, объединяет пользователя с его профилем, при создании."""
    print('Profile signal!')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    """Функция, отвечает за редактирование пользователя"""
    profile = instance # это какой конкретный профиль пользователя будет обновляться.
    user = profile.user # в user будет профиль пользователя сохраняться

    if created is False: # если пользователя не создаем, тогда это идёт обновление.
        user.first_name = profile.name # Что бы данные перезаписывались, относительно тех которые существуют.
        user.username = profile.username
        user.email = profile.email
        user.save() # сохраняем в БД

#
@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    """Функция, отвечает за удаление пользователя"""
    print('Deleting user...')
    user = instance.user
    user.delete()
#
# # Можем сделать не таким способом а через дикаратор
# post_save.connect(create_profile, sender=User) # первым параметром передаем имя функции без вызова.
# post_save.connect(update_user, sender=Profile) # запускаем, обновлять будем профиль пользователя, а не самого пользователя.
# post_delete.connect(delete_user, sender=Profile)
