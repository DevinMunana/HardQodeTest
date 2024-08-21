from django.contrib.auth.models import AbstractUser
from django.db import models
from product.courses import models as courses_models

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""
    username = models.CharField(unique=True, max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    courses = models.ManyToManyField(courses_models.Course, through="Subscription")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.FloatField(default=1000)

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    user_name = models.CharField(max_length=128)
    course_name = models.CharField(max_length=128)
    course = models.ForeignKey(courses_models.Course, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
