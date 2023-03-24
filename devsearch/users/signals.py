from django.db.models.signals import post_save  # Сигналы уведомления в админке. Нам надо что бы когда создавался пользователь, что бы профиль создавался автоматически.
from django.db.models.signals import post_delete
from django.dispatch import receiver  # декоратор для подключения
from .models import Profile
from django.contrib.auth.models import User


# sender - отправитель
# instance - как экземпляр текущий
# created - созданный, если профиль был создан.
# **kwargs - набор именованных параметров.
# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Функция, объединяет при создании в админке пользователя, автоматически создается профиль пользователя."""
    print('Profile signal!')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )


# @receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    print('Deleting user...')
    user = instance.user
    user.delete()

# Можем сделать не таким способом а через дикаратор
post_save.connect(create_profile, sender=User) # первым параметром передаем имя функции без вызова
post_delete.connect(delete_user, sender=Profile)
