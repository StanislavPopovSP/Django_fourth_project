from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),

    path('login/', views.login_user, name='login'), # авторизация
    path('logout/', views.logout_user, name='logout'), # выйти
    path('register/', views.register_user, name='register'), # регистрация
    path('account/', views.user_account, name='account'), # аккаунт
]
