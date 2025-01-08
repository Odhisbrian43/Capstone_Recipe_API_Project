from django.db import models
from accounts.models import CustomUser
import jsonfield
from django.core import validators

#Category model.
class Category(models.Model):
    name = models.CharField(max_length=100)

#Recipe model.
class Recipe(models.Model):
    #Recipe model fields.
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )
    description = models.TextField()
    ingredients = jsonfield.JSONField(default=[], null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    instructions = models.TextField()
    preparation_time = models.PositiveIntegerField
    cooking_time = models.PositiveIntegerField
    servings = models.PositiveIntegerField
    created_date = models.DateField(auto_now_add=True)

    #Recipe instance string representation.
    def __str__(self):
        return f'{self.title} category:{self.category} by:{self.author}'

