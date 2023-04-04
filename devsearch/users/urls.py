from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('account/', views.user_account, name='account'), # аккаунт

    path('login/', views.login_user, name='login'), # авторизация
    path('logout/', views.logout_user, name='logout'), # выйти
    path('register/', views.register_user, name='register'), # регистрация

    path('edit-account/', views.edit_account, name='edit-account'), # редактирования пользователя
    path('create-skill/', views.create_skill, name='create-skill'), # добавление навыков
    path('update-skill/<str:pk>/', views.update_skill, name='update-skill'), # редактирование навыков
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill'), # редактирование навыков

    path('inbox/', views.inbox, name='inbox'), # редактирование навыков
]
