from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Object(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Visit(models.Model):
    visiter = models.ForeignKey(User, related_name='visits', verbose_name=("Пользователь"), on_delete=models.CASCADE)
    objct = models.ForeignKey(Object, related_name='visits', verbose_name=("Объект"), on_delete=models.CASCADE)
    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)
    date = models.DateField(null=True)
    started = models.DateField(null=True)
    ended = models.DateField(null=True)

    def __str__(self):
        return f'Визит на {self.objct}'
