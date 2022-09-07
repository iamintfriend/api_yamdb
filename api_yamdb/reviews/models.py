from django.db import models

from users.models import User


SCORE_CHOICES = [
    (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
    (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'),
]


class Review(models.Model):
    """Модель отзывов к произведениям."""

    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.TextField(verbose_name='текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'дата публикации', auto_now_add=True
    )
    score = models.IntegerField(choices=SCORE_CHOICES)

    class Meta:
        ordering = ('-pub_date',)  # Пока такое упорядочивание
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    text = models.TextField(verbose_name='текст комментария')
    pub_date = models.DateTimeField(
        'дата добавления', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text[:15]
