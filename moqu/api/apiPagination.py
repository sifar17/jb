from rest_framework.pagination import PageNumberPagination

class categoryPageNumberPagination(PageNumberPagination):
    page_size = 10

class moviePageNumberPagination(PageNumberPagination):
    page_size = 10
    
class quotePageNumberPagination(PageNumberPagination):
    page_size = 30