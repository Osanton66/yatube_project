from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('posts/', views.group_posts),
    path('posts/<slug:slug>/', views.post),
] 