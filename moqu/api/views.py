from rest_framework import viewsets
from .serializers import CategorySerializer, MovieSerializer, QuoteSerializer
from moqu.models import Category, Movie, Quote
from . apiPagination import categoryPageNumberPagination, moviePageNumberPagination, quotePageNumberPagination

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = categoryPageNumberPagination

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Movie.objects.all().order_by('id')
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = moviePageNumberPagination


class QuoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    pagination_class = quotePageNumberPagination
