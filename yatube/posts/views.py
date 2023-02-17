from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from .models import Post, Group, User
from .serializers import PostSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    return render(request, template, {'group': group, 'posts': posts})


def profile(request, username):
    name = get_object_or_404(User, username=username)
    post_filter = name.posts.all()
    paginator = Paginator(post_filter, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'name': name,
        'post_filter': post_filter,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


@login_required(login_url="users:login")
def post_create(request):
    """Добавления поста."""
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
        )
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']

            instance = form.save(commit=False)
            instance.author_id = request.user.id
            instance.save()

            user_name = request.user.username

            return redirect('posts:profile', user_name)

        return render(request, template, {'form': form})

    form = PostForm()

    return render(request, template, {'form': form})


@login_required(login_url="users:login")
def post_edit(request, post_id):
    """Редактирование поста. Доступно только автору."""

    template = 'posts/create_post.html'

    post = get_object_or_404(Post, pk=post_id)

    # Если редактировать пытается не автор
    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post.pk)

    form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )
    if form.is_valid():
        form.save()

        user_name = request.user.username
        return redirect('posts:profile', user_name)

    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


def get_post(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=id)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)


@api_view(['GET', 'POST'])
def api_posts(request):
    '''if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)'''
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PostSerializer(post)
    return Response(serializer.data)
