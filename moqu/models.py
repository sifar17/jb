from django.db import models

# Create your models here.

class CategoryAbstarct(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        abstract = True
        ordering = ['id']

class Category(CategoryAbstarct):

    # to show the name (string format) of Category in admin
    def __str__(self):
        return self.name

class CategoryChecked(CategoryAbstarct):

    # to show the name (string format) of CheckedCategory in admin
    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'movies')

    # Following code is to avoid the UnorderedObjectListWarning
    class Meta:
        ordering = ['id']
        
    # to show the name (string format) of Movie in admin
    def __str__(self):
        return self.name

class Quote(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE, related_name = 'quotes')
    quote = models.TextField()

    # Following code is to avoid the UnorderedObjectListWarning
    class Meta:
        ordering = ['id']

    # to show the name (string format) of Quote in admin
    def __str__(self):
        return self.quote 

class SearchKeyword(models.Model):
    name = models.TextField()

    # to show the name (string format) of SearchKeyword in admin
    def __str__(self):
        return self.name