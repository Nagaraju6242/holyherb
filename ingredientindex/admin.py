from django.contrib import admin
from .models import Ingredient
# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_display = ["letter","name"]
    list_display_links = ["letter","name"]

admin.site.register(Ingredient,IngredientAdmin)
