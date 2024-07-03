from django.db import models
from django.utils.translation import gettext as _


class Author(models.Model):
    full_name = models.CharField(max_length=64)

    def __str__(self):
        return self.full_name


class Post(models.Model):
    title = models.CharField(max_length=64, verbose_name=_("Title"))
    subtitle = models.CharField(max_length=64, verbose_name=_("Subtitle"))
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
