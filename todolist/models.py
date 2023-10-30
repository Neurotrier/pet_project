from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class UserList(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    is_finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listform', kwargs={'username': self.user.username, 'list_slug': self.slug})

class Task(models.Model):
    content = models.CharField(max_length=300, verbose_name="Задача")
    is_finished = models.BooleanField(default=False)
    user_list = models.ForeignKey('UserList', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('taskform', kwargs={'username': self.user.username, 'list_slug': self.user_list.slug, 'taskid': self.id})


