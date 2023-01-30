from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    #template = 'posts/index.html'
    latest = Post.objects.all()[:11]
    return render(request, "posts/index.html", {"posts": latest})


def group_posts(request, slug):
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, template, {"group": group, "posts": posts})