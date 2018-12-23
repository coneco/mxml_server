from django.shortcuts import render
from datetime import datetime

# Create your views here.

def index(request):

    context = {
        'nav_root': 'index',
        'title': 'Home',
        'year': datetime.now().year,
        }
    return render(request, 'app/index.html', context)

def models(request):
    context = {
        'nav_root': 'models',
        'title': 'Models',
        'year': datetime.now().year,
        }
    return render(request, 'app/models.html', context)

def logs(request):
    context = {
        'nav_root': 'logs',
        'title': 'Logs',
        'year': datetime.now().year,
        }
    return render(request, 'app/logs.html', context)
