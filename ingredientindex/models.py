from django.db import models
from products.models import Product
# Create your models here.

class Ingredient(models.Model):
    letter = models.CharField(max_length=1,help_text="Enter the first Letter")
    name   = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    products = models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name'),