from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.

def post_list(request):
    
    posts = Post.published.all()
    
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_details(request,pk):
    
    post = get_object_or_404(Post,id=pk,status=Post.Status.PUBLISHED)
    
    return render(request, 'blog/post/details.html', {'post': post})