from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail 


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

class PostListView(ListView): #class based view , inherited from ListView
    """
    Alternative to post_list view
    """
    
    queryset = Post.published.all()
    context_object_name= 'posts'
    paginate_by= 3
    template_name= 'blog/post/list.html'
    
    
    
def post_share(request, post_id):
    
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    sent = False
    
    
    if request.method == 'POST':
        #form was submitted
        
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form feilds passed validation
            cd = form.cleaned_data # captures the inputed data in a dictionary form (fields as keys and input as values)
            
            #send mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = f"{cd['name']} recommended you read" \
                        f' "{post.title}"'
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comment']}"
                      
            send_mail(subject, message , 'dproject8420@gmail.com', [cd['to']])
            
            sent=True
            
    else:
        form = EmailPostForm()
        
    return render(request, 'blog/post/share.html', {'post': post, 'form': form , 'sent': sent})
    