from django.db.models.signals import post_save  # Сигналы уведомления в админке. Нам надо что бы когда создавался пользователь, что бы профиль создавался автоматически.
from django.db.models.signals import post_delete
from django.dispatch import receiver  # декоратор для подключения
from .models import Profile


# sender - отправитель
# instance - как экземпляр текущий
# created - созданный, если профиль был создан.
# **kwargs - набор именованных параметров.
@receiver(post_save, sender=Profile)
def profile_update(sender, instance, created, **kwargs):
    print('Profile Saved!')
    print('Instance:', instance)
    print('CREATED:', created)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    print('Deleting user...')

# Можем сделать не таким способом а через дикаратор
# post_save.connect(profile_update, sender=Profile) # первым параметром передаем имя функции без вызова
# post_delete.connect(delete_user, sender=Profile)
