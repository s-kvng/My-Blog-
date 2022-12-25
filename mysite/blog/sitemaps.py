from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap): #defined a custom sitemap by inheriting the Sitemap class of the sitemaps module
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated