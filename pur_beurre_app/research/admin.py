from django.contrib import admin

from .models import Food, Category, CategoryFoods

admin.site.register(Food)
admin.site.register(Category)
admin.site.register(CategoryFoods)
