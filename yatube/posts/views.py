from django.shortcuts import render
from django.http import HttpResponse


# Главная страница
def index(request): 
    template = 'posts/index.html'
    title = "Это главная страница проекта Yatube"
    context = {
        'title': title,
        'text': 'Главная страница',
    }
    return render(request, template, context)   


# Страница со списком мороженого
def group_posts(request):
    template = 'posts/group_list.html'
    title = "Здесь будет информация о группах проекта Yatube"
    context = {
        'title': title,
        'text': 'Группы',
    }
    return render(request, template, context)


def post(request, slug):
    return HttpResponse(f'Пост {slug}') 