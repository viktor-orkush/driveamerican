from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from blogapp.models import Post

NUM_OF_POSTS = 5


def all_post(request):
    post_list = Post.objects.all()
    post_list = post_list.order_by('-pub_date')
    paginator = Paginator(post_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog.html', {'posts': post_list})


def post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'post.html', {'post': post})
