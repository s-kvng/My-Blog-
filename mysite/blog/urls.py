from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list , name='post_list'), #function based view 
    path('tag/<slug:tag_slug>/', views.post_list , name = 'list_post_by_tag'),
    #path('', views.PostListView.as_view(), name='post_list'), #class based view , that uses the generic ListView
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_details , name='post_details'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
