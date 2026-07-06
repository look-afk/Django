from tabnanny import verbose

from django.contrib.auth.models import User
from django.db import models

class Skills(models.Model):
    name = models.CharField(max_length=28)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name
    
class Vacancy(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "ОТкрыто"),
        ("closed", "Закрытый"),
    ]

    slug = models.SlugField(max_length=12)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=15, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True)
    skills = models.ManyToManyField(Skills)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    


    def __str__(self):
        return self.slug
    
    class Meta:
        verbose_name = "Baкансия"
        verbose_name_plural = "Вакансии"