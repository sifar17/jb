from rest_framework import serializers
from moqu.models import Category, Movie, Quote

class CategorySerializer(serializers.ModelSerializer):
    movies = serializers.StringRelatedField(many = True, read_only = True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'movies']
        ordering = ['id']

class MovieSerializer(serializers.ModelSerializer):
    quotes = serializers.StringRelatedField(many = True, read_only = True)
    # to show the category-name (string) instead of category-id (int)
    category = serializers.CharField()

    class Meta:
        model = Movie
        # depth = 1
        fields = ['id', 'name', 'category', 'quotes']
        # ordering = ['id']

class QuoteSerializer(serializers.ModelSerializer):
    # to show the movie-name (string) instead of movie-id (int)
    movie = serializers.CharField()
    
    class Meta:
        model = Quote
        # depth = 1
        fields = ['id', 'movie', 'quote']
        # fields = '__all__'
        # ordering = ['id']