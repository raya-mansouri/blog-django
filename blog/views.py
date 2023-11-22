from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post


def blog_home(request, **kwargs):
    posts = Post.objects.filter(status=1)

    if kwargs.get('category_name') != None:
        posts = posts.filter(category__name=kwargs['category_name'])
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])

    posts = Paginator(posts, 3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts.get_page(1)
    except EmptyPage:
        posts.get_page(1)

    context = {'posts': posts}
    return render(request, 'blog/Blog_home.html', context)


def blog_single(request, p_id):
    post = get_object_or_404(Post, pk=p_id, status=1)
    next_post = Post.objects.filter(pk__gt=post.id).order_by('id').first()
    pre_post = Post.objects.filter(pk__lt=post.id).order_by('id').last()
    post.counted_views += 1
    post.save()
    context = {'post': post, 'next_post': next_post, 'pre_post': pre_post}

    return render(request, 'blog/Blog_single.html', context)


def blog_search(request):
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = Post.objects.filter(status=1, title__contains=s)
    context = {'posts': posts}
    return render(request, 'blog/Blog_home.html', context)
