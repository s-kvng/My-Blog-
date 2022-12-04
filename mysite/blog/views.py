from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView


# Create your views here.

def post_list(request):
    
    post_list = Post.published.all()
    
    #Pagination with 3 posts per page
    paginator = Paginator(post_list,3) # determine the number of posts to display on a page
    page_number = request.GET.get('page',1)#get the requested page number or default: 1 
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        #if the page_number is out of range deliver the last page of results
        posts = paginator.page(paginator.num_pages)  
    
    
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_details(request,year,month,day,post):
    
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    return render(request, 'blog/post/details.html', {'post': post})

class PostListView(ListView):
    """
    Alternative to post_list view
    """
    
    queryset = Post.published.all()
    context_object_name= 'posts'
    paginate_by= 3
    template_name= 'blog/post/list.html'