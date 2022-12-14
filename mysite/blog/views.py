from django.shortcuts import render, get_object_or_404
from .models import Post , Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm , CommentForm
from django.core.mail import send_mail 
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


# Create your views here.

def post_list(request, tag_slug=None):
    
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag , slug = tag_slug )
        post_list = post_list.filter(tags__in=[tag])
        
    
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
    
    
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_details(request,year,month,day,post):
    
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    #QuerySet to retrieve all active comments for the post
    comments = post.comments.filter(active=True)
    
    # creating an instance of the comment form
    form = CommentForm()
    
    #List of of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                    .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags'))\
                    .order_by('-same_tags','-publish')[:4]
    
    
    return render(request, 'blog/post/details.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})

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


@require_POST
def post_comment(request,post_id):
    
    post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED )
    comment = None 
    
    
    form = CommentForm(data = request.POST)
    if form.is_valid():
        
        #create a comment object without saving to the database
        comment = form.save(commit=False)
        
        comment.post = post
        
        #save comment object to database
        comment.save()
        
    return render(request, 'blog/post/comment.html', {'post' : post, 'form':form, 'comment':comment})
    