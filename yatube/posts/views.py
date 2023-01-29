from django.shortcuts import render
from django.http import HttpResponse


# Главная страница
def index(request):    
    return HttpResponse('Главная страница')


# Страница со списком мороженого
def group_posts(request):
    return HttpResponse('Список постов')


# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из path()
def post(request, slug):
    return HttpResponse(f'Пост {slug}') 