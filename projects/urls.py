from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),

    path('create_project/', views.create_project, name='create_project'), # Путь для создания какого то проекта.
    path('update_project/<str:pk>/', views.update_project, name='update_project'), # Путь для кнопки обновить проект.
    path('delete_project/<str:pk>/', views.delete_project, name='delete_project'), # Путь для кнопки удалить проект.
]
