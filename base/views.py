from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'base/index.html')


def about(request):
    
    context = {
        'jbAbout_active': 'active',
    }

    return render(request, 'base/about.html', context)