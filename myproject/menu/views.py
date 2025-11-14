from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    menus = Menu.objects.all()
    return render(request, 'menu/index.html', {'menus': menus})
