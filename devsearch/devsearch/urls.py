"""devsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),  # подключаем документ по пути, делаем главную страницу index.html
    path('', include('users.urls')),  # подключаем пути проекта users
]

# Мы можем сделать что пути будут добавляться только в тот момент, когда мы работаем в режиме разработки.
if settings.DEBUG: # Если в режиме разработки, то у нас будет использоваться urlpatterns что бы картинки отображались корректно. Когда сайт выкладывать на продакшен, когда он готовый, на хостингах это реализуется по другому. Если выложили на хостинг данная настройка отрабатывать уже не будет. Пути настраиваютя на самом хостинге.
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Объединяем settings.MEDIA_URL с document_root=settings.MEDIA_ROOT Что бы у нас корректно отображались изображения.