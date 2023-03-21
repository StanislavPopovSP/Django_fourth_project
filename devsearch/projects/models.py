from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200) # Название самого какого то проекта
    description = models.TextField(null=True, blank=True) # Поле по больше(Пустое поле, по умолчанию null)
    featured_image = models.ImageField(null=True, blank=True, upload_to='projects/%Y/%m/%d/', default='default.jpg') # Поле для изображения, поле будет заполняться динамически. upload_to - указывает по какому пути будет загружаться изображение. default='default.jpg' не указываем путь к папке, значит она должна лежать в медиа.
    # В БД будет храниться ссылка на эту картинку.(/%Y/%m/%d/ - подстановочный шаблон(/%Y - создастся папка 2023 года, /%m - март, /%d - день в конце / после слеша будет имя изображения.)) И если не загрузили ни какое значение, напишем default='' и подставим какую-то картинку.
    demo_link = models.CharField(max_length=2000, null=True, blank=True) # будет два перехода
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True) # для подсчёта кол-ва процентов
    vote_ratio = models.IntegerField(default=0, null=True, blank=True) # для подсчёта кол-ва
    created = models.DateTimeField(auto_now_add=True)  # Дата создания какого-то проекта.

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True) # Дата создания тега

    def __str__(self):
        return self.name