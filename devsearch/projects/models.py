from django.db import models
from users.models import Profile

class Project(models.Model):
    """Работа с проектами"""
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
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
        """Заголовок проекта"""
        return self.title

    # Класс Meta отвечает за дополнительные настройки. (Пример способ сортировки)
    class Meta:
        """Порядок вывода элементов"""
        ordering = ['-vote_total'] # Привяжемся к положительным либо отрицательным отзывам

    def reviewers(self): # Что бы элементы считались
        queryset = self.review_set.all().values_list('owner__id', flat=True) # через self.review_set.all() будем брать все данные, список значений(id владельца)
        return queryset

    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count() # value='up' - как имя, количество
        total_votes = reviews.count() # Сохраним общее количество отзывов.
        ratio = (up_votes / total_votes) * 100 # рейтинг общий
        self.vote_total = total_votes
        self.vote_ratio = ratio

        self.save()


class Tag(models.Model):
    """Работа с тегами"""
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True) # Дата создания тега

    def __str__(self):
        """Имя тега"""
        return self.name


class Review(models.Model):
    """Работа с комментариями"""
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    ) # Будет два варианта положительный, либо отрицательный отзыв.
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True) # владелец отзыва. null=True - поле владельца может быть пустым и писать комментарий может любой пользователь и не зарегистрированный.
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # делать поле пустым не будем, пот-то отзывы делаем по какому-то проекту. Обязательно поле проекты должно быть заполнено.
    body = models.TextField(null=True, blank=True) # будет там отзыв, тело самого отзыва.
    value = models.CharField(max_length=200, choices=VOTE_TYPE) # а атрибут choices добавим VOTE_TYPE - будем выбирать один из элементов VOTE_TYPE. Из выпадающего списка будет выбираться одно из значений. max_length=200 - для текста выпадающего списка.
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Будем видеть положительный или отрицательный отзыв"""
        return self.value

    class Meta:
        """Уникальный отзыв от одного имени."""
        unique_together = [['owner', 'project']] # unique_together - специальное имя переменной, пара уникальных элементов. Что бы пользователь был уникальный для одного проекта.
