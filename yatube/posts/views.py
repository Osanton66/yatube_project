from django.shortcuts import render, get_object_or_404
from .models import Post, Group, User
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context) 


def group_posts(request, slug):
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    return render(request, template, {"group": group, "posts": posts})


def profile(request, username):
    name = User.objects.get(username=username)
    post_filter = Post.objects.filter(author=name)
    paginator = Paginator(post_filter, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_counter = post_filter.count()
    context = {
        'name': name,
        'post_filter': post_filter,
        'post_counter': post_counter,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_det = Post.objects.get(pk=post_id)
    post_counter = Post.objects.filter(author=post_det.author).count()
    group_post = Group.objects.get(id=post_det.group_id)
    context = {
        'post_det': post_det,
        'post_counter': post_counter,
        'group_post': group_post,
    }
    return render(request, 'posts/post_detail.html', context) 