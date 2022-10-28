from unicodedata import category
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    CATEGORY_CHOICES = [
        ('fruit', 'Fruits'), ('vegetable', 'Verduras'), ('flower', 'Flores')
    ]
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    createdDate = models.DateField()
    price = models.PositiveSmallIntegerField(MinValueValidator(1))
    stock = models.PositiveSmallIntegerField(MinValueValidator(1))

    def __str__(self) -> str:
        return self.name
