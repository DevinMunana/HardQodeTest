from django.db import models
from product.users import models #import CustomUser


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    lessons = models.ManyToManyField("Lesson", through="Course_Lesson_Junction")
    lessons_count = models.IntegerField()
    price = models.FloatField()
    students_count = models.IntegerField()
    max_students_count = models.IntegerField()
    groups_filled_percent = models.FloatField()
    demand_course_percent = models.FloatField()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


# class Course_User_Junction(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Course_Lesson_Junction(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ManyToManyField(Course, through=Course_Lesson_Junction)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class User_Group_Junction(models.Model):
    user = models.ForeignKey(models.CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)


class Group(models.Model):
    """Модель группы."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    students = models.ManyToManyField(models.CustomUser, through=User_Group_Junction)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)