from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path("group/<slug>/", views.group_posts, name="group-posts"),
    path("", views.index, name="index"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('posts/<int:post_id>/', views.post_detail, name="post_detail"),
    path('create/', views.post_create, name="post_create"),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),
    path('api/v1/post/<int:id>', views.get_post, name='get_post'),
    path('api/v1/posts/', views.api_posts),
    path('api/v1/posts/<int:id>/', views.api_posts_detail),
]
