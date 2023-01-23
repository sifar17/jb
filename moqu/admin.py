from django.contrib import admin
from . models import Category, CategoryChecked, Movie, Quote, SearchKeyword

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CategoryChecked)
class CategoryCheckedAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'quote']

@admin.register(SearchKeyword)
class SearchKeywordAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
