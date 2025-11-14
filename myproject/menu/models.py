from django.db import models
from django.urls import reverse, NoReverseMatch


# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.menu.name} - {self.name}"

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'