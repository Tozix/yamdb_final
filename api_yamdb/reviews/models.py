import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

SCORE = zip(range(1, 11), range(1, 11))


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ['slug']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        unique=True
    )

    class Meta:
        ordering = ['slug']
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100)
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.date.today().year),
        ])
    description = models.CharField(
        verbose_name='Описание',
        max_length=200)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='genres')

    class Meta:
        ordering = ['category']
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """Отзывы к произведениям"""
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField('Оценка', default=0, choices=SCORE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзывам"""
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
