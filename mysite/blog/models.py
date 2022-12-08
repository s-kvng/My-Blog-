from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# from .models import PublishedManager

# Create your models here.


# create a custom manager instance for published
class PublishedManager(models.Manager): 
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status = Post.Status.PUBLISHED)

class Post(models.Model):
    
    tags = TaggableManager()
    
    class Status(models.TextChoices):
        DRAFT = 'DF' , 'draft'
        PUBLISHED = 'PB' , 'published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, 
                              choices=Status.choices, default=Status.DRAFT)
    
     
    objects = models.Manager() # our default manager
    published = PublishedManager() # our custom manager
    
    class Meta:
        ordering = ['-publish'] # arranges the order of objected in decending order(newer published to older )
        indexes = [
            models.Index(fields=['publish']),
        ]
    
       
    
    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("blog:post_details", args=[self.publish.year,
                                                  self.publish.month,
                                                  self.publish.day,
                                                  self.slug])
    
    

class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete= models.CASCADE , related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
    