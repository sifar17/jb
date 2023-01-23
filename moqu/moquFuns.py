# This file defines functions that are supporting the functions
# ... especially the main function 'moquHome'
# ... in views.py file

from django.core.paginator import Paginator
from .models import Movie, Quote, Category, CategoryChecked, SearchKeyword
from django.db.models import Q

# ==================================================================
# This function takes pk as argument (default value of pk is None)
# ... and returns
# ... ... if pk is passed: movie name, its quotes and 
#                          ... the search parameter for the quotes 
# ... ... if pk is not passed: all movies, all quotes and 
#                          ... the search parameter for the quotes 

def get_movieAndQuote(movies_display, pk = None):
    
    if pk is not None:
        movie_name = Movie.objects.get(id=pk)
        quote_listDB = movie_name.quotes.all()
        
    else:
        movie_name = 'All quotes'
        quote_listDB = Quote.objects.filter(movie__in = movies_display)

    if SearchKeyword.objects.exists():
        search_keyword = SearchKeyword.objects.all().first()
        # Use of .first()
        # ... although we are allowing only one instance in this SearchKeyword database, 
        # ... still, to make sure only the first instance is selected in case there are multiple instances in the SearchKeyword database.
        quotes_display = quote_listDB.filter(quote__icontains = search_keyword).order_by('movie')

    else:
        search_keyword = ''
        quotes_display = quote_listDB.order_by('movie')

    return movie_name, quotes_display, search_keyword

# ==================================================================
# This function takes selected/checked categories as argument
# ... and returns 
# ... ... movies to be displayed on html page
# ... ... search parameter coming from GET request for movies 

def get_moviesDisplay(request, categories_checked):

    qmovie = get_qGetRequest(request, 'movie_contains')

    if categories_checked:
        movies_display = Movie.objects.filter(category__in = categories_checked).filter(name__icontains = qmovie)
    else:
        movies_display = Movie.objects.filter(name__icontains = qmovie)

    return movies_display, qmovie

# ==================================================================
# This function takes request as argument
# ... and returns 
# ... ... checked categories to be displayed on html page
# ... ... unchecked categories to be displayed on html page
# ... ... search parameter coming from GET request for categories

def get_categoriesChecked_categoriesUnchecked(request):

    qcategory = get_qGetRequest(request, 'category_contains')

    categories_checked = Category.objects.filter(
        Q(name__in = CategoryChecked.objects.values_list('name', flat = True)) &
        Q(name__icontains = qcategory)).distinct()
    
    categories_unchecked = Category.objects.filter(
        ~Q(name__in = CategoryChecked.objects.values_list('name', flat = True)) &
        Q(name__icontains = qcategory)).distinct()

    return categories_checked, categories_unchecked, qcategory

# ==================================================================
# This function deletes the previous search keyword (deletes all)
# ... from SearchKeyword database 
# ... and saves the new search keyword coming from the Post request

def save_searchKeyword(request):

    qquote = get_qPostRequest(request, 'quote_contains')
    
    if qquote != '':
        SearchKeyword.objects.all().delete()
        SearchKeyword(name = qquote).save()
    else:
        SearchKeyword.objects.all().delete()

# ==================================================================
# This function deletes the previous list of categories (deletes all) 
# ... from CategoryChecked database 
# ... and saves the new list of categories coming from the Post request

def save_categoryChecked(request):

    CategoryChecked.objects.all().delete()
    qcategory_checked = request.POST.getlist('categorybox_checked')
    for category in qcategory_checked:
        category_name = category
        CategoryChecked(name = category_name).save()

# ==================================================================
# These two functions take request & keywords from user as arguments
# ... and return the keywords as strings   

def get_qPostRequest(request, q_param):
    q = request.POST.get(q_param) if request.POST.get(q_param) != None else ''
    return q

def get_qGetRequest(request, q_param):
    q = request.GET.get(q_param) if request.GET.get(q_param) != None else ''
    return q

# ==================================================================
# This function takes previous_page_last_quoteid, previous_page_last_movie
# ... & quotes_display as arguments
# ... and returns the previous_page_last_quote_index   

def get_previous_page_last_quote_index(previous_page_last_quoteid, previous_page_last_movie, quotes_display):

    previous_page_last_movie_quoteSet = quotes_display.filter(movie__name = previous_page_last_movie).order_by('id')
    
    for row_index, row in enumerate(previous_page_last_movie_quoteSet, 1):
        if row.id == previous_page_last_quoteid:
            previous_page_last_quote_index = row_index
            break

    return previous_page_last_quote_index

# ==================================================================
# This function takes paginator_quote & page_number as arguments
# ... and returns previous_page_last_quoteid &
# ... previous_page_last_movie   

def get_previous_page_items(paginator_quote, page_number):

    previous_page_queryset = paginator_quote.page(int(page_number)-1).object_list

    dict_previous_page_idMovie = {row.id: row.movie for row in previous_page_queryset}

    previous_page_last_quoteid = [row.id for row in previous_page_queryset][-1]
    previous_page_last_movie = [row.movie for row in previous_page_queryset][-1]    

    return previous_page_last_quoteid, previous_page_last_movie

# ==================================================================
# This function takes pageSet_display_list, current_page as arguments 
# ... and returns current_pageSet_number, previous_pageSet_number
# This function helps to create the 'next10' (or next5, etc) button  
# ... makes easier to navigate through pages in set of 10 (or 5, etc)

def get_pageSet_items(pageSet_display_list, current_page):

    current_page_position = ['', '']

    for pageSet in pageSet_display_list:
        for page in pageSet:
            if page == current_page:
                current_page_position[0], current_page_position[1] = pageSet_display_list.index(pageSet), pageSet.index(page)

    current_pageSet_number = current_page_position[0]

    if current_pageSet_number >= 1:
        previous_pageSet_number = current_pageSet_number - 1
    else:
        previous_pageSet_number = 0

    if current_pageSet_number <= len(pageSet_display_list) - 2:
        next_pageSet_number = current_pageSet_number + 1
    else:
        next_pageSet_number = 0

    return current_pageSet_number, previous_pageSet_number, next_pageSet_number

# ==================================================================
# This function takes paginator_quote as argument 
# ... and returns pageSet_display_list
# => pageSet_display_list = 
# ... ... list of set of predefined number of pages
# ... ... that is to displayed
# => pageSet_display = 
# ... ... number representing the set of predefined number of pages
# ... ... maximum number of pages to be displayed in one go 

def get_pageSet_display(paginator_quote):
    paginator_quote_range = paginator_quote.page_range
    pageSet_display = 10
    pageSet_display_total = len(paginator_quote_range)//pageSet_display + 1

    list_paginator_quote_range = list(paginator_quote_range)

    pageSet_display_start_page = 1

    pageSet_display_list = []

    for pageSet in range(1, pageSet_display_total + 1):

        pageSet_display_end_page = pageSet_display_start_page + pageSet_display
            
        if len(list_paginator_quote_range[pageSet_display_start_page-1:]) < pageSet_display:
            pageSet_display_list.append(list_paginator_quote_range[pageSet_display_start_page-1:])
        else:
            pageSet_display_list.append(list_paginator_quote_range[pageSet_display_start_page-1:pageSet_display_end_page-1])

        pageSet_display_start_page = pageSet_display_end_page
    
    return pageSet_display, pageSet_display_list

# ==================================================================
# This function takes a queryset from Quote model as argument
# ... and returns the number of pages as 
# ... given in the Paginator class of django 

def quote_perPage(request, quotes_display):
    global paginator_quote, page_number

    quotes_count_perPage = 5
    orphans = 0 if quotes_count_perPage <= 10 else 1 if quotes_count_perPage <= 10 else 2 if quotes_count_perPage <= 20 else 3

    paginator_quote = Paginator(quotes_display, quotes_count_perPage, orphans = orphans)

    page_number = request.GET.get('page')
    
    quotes_display_perPage = paginator_quote.get_page(page_number)
    
    current_page = quotes_display_perPage.number

    return quotes_display_perPage, paginator_quote, current_page

# ====================================================================
# This function takes a queryset from Quote model as argument
# ... formats it and returns a dictionary containing
# ... movie name(s) as key(s) and associated quote(s) as value(s)
# ... quote(s) is/are the nested lists of individual quotes with
# ... the lists of each line (in the quote) which has
# ... speaker (if any), line of quote, reference as elements
 
def get_quoteFormatted(quotes_display_perPage, quotes_display):
    
    dict_mapMovieQuote = {}

    for row in quotes_display_perPage:
        if row.movie not in dict_mapMovieQuote:
            dict_mapMovieQuote[row.movie] = [row.quote.split('\n')]
        else:
            dict_mapMovieQuote[row.movie].append(row.quote.split('\n'))

    quote_dictDisplay = {}

    for movie, quote_listDisplay in dict_mapMovieQuote.items():   

        # This if...else statement is to make sure that the current
        # ... page doesn't start afresh i.e. with index 1
        # ... if the first movie on current page is in continuation
        # ... from the previous page.
        # ... Instead of a number, current_page_first_quote_index 
        # ... is being passed to enumerate function. 

        if quotes_display_perPage.has_previous():
            previous_page_last_quoteid, previous_page_last_movie = get_previous_page_items(paginator_quote, page_number)
            if movie == previous_page_last_movie:
                previous_page_last_quote_index = get_previous_page_last_quote_index(previous_page_last_quoteid, previous_page_last_movie, quotes_display)
                current_page_first_quote_index = previous_page_last_quote_index + 1
            else:
                current_page_first_quote_index = 1
        else:
            current_page_first_quote_index = 1

        dict_quoteLine_list = {}

        for q_index, quote in enumerate(quote_listDisplay, current_page_first_quote_index):
        
            quoteLine_list = []
            dict_quoteLine_list[q_index] = []
    
            for l_index, line in enumerate(quote, 1):
                speakerContent_list = ['','', '']
                if ':' in line:
                    speakerContent_list[0] += f'{line[:line.index(":")+1]} '
                    if '---' in line:
                        speakerContent_list[1] += f'{line[line.index(":")+2:line.index("---")]}'
                        speakerContent_list[2] += f'\n\n{line[line.index("---"):]}'
                    else:
                        speakerContent_list[1] += f'{line[line.index(":")+2:]}'
                else:
                    if '---' in line:
                        speakerContent_list[1] += f'\n{line[:line.index("---")]}'
                        speakerContent_list[2] += f'\n\n{line[line.index("---"):]}'
                    else:
                        speakerContent_list[1] += f'\n{line}'
                quoteLine_list.append(speakerContent_list)
        
            dict_quoteLine_list[q_index] += quoteLine_list 

        quote_dictDisplay[movie] = dict_quoteLine_list
    
    return quote_dictDisplay

