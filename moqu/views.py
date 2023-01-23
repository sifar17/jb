from django.shortcuts import render
from . moquFuns import *

# ===================================================================
# This is the main function which
# ... calls all the necessary functions and
# ... renders the Home page of moqu

def moquHome(request, pk = None):

    if request.POST.get('category-apply', False) == 'category-selected':
        save_categoryChecked(request)

    elif request.POST.get('search_in_quote', False) == 'searchKeyword':
        save_searchKeyword(request)

    categories_checked, categories_unchecked, qcategory = get_categoriesChecked_categoriesUnchecked(request)

    movies_display, qmovie = get_moviesDisplay(request, categories_checked)

    movie_name, quotes_display, search_keyword = get_movieAndQuote(movies_display, pk)

    quotes_display_perPage, paginator_quote, current_page = quote_perPage(request, quotes_display)
    
    quote_dictDisplay = get_quoteFormatted(quotes_display_perPage, quotes_display)

    pageSet_display, pageSet_display_list = get_pageSet_display(paginator_quote)

    current_pageSet_number, previous_pageSet_number, next_pageSet_number = get_pageSet_items(pageSet_display_list, current_page)
    
    context = {
        'categories_checked': categories_checked,
        'categories_unchecked': categories_unchecked,
        'movies_display': movies_display,
        'qmovie': qmovie,
        'qcategory': qcategory,
        'search_keyword': search_keyword,
        'movie_name': movie_name,
        'paginator_quote': paginator_quote,
        'quotes_display': quotes_display,
        'quotes_display_perPage': quotes_display_perPage,
        'pageSet_display': pageSet_display,
        'pageSet_display_list': pageSet_display_list,
        'current_pageSet': pageSet_display_list[current_pageSet_number],        
        'next_pageSet': pageSet_display_list[next_pageSet_number],
        'previous_pageSet': pageSet_display_list[previous_pageSet_number],
        'quote_dictDisplay': quote_dictDisplay,
        'moquHome_active': 'active',
        }

    return render(request, 'moqu/index.html', context)

# ===================================================================
# This function renders the Know Moqu page

def moquAbout(request):

    context = {
        'moquAbout_active': 'active',
    }
    
    return render(request, 'moqu/about.html', context)

# ===================================================================
# This function renders the Moqu API page

def moquApi(request):

    context = {
        'moquApi_active': 'active',
    }
    return render(request, 'moqu/api.html', context)
