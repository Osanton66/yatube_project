from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.group_posts, name='group_posts'),
    path('posts/<slug:slug>/', views.post, name='posts_slug'),
] 