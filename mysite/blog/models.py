from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# from .models import PublishedManager

# Create your models here.


# create a custom manager instance for published
class PublishedManager(models.Manager): 
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status = Post.Status.PUBLISHED)

class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF' , 'draft'
        PUBLISHED = 'PB' , 'published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
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
        return reverse("blog:post_details", args=[self.id])
    
    