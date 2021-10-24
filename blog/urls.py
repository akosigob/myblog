from .import views
from django.urls import path
from .views import delete_comment, add_post, update_post

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
	path('<slug:slug>/', views.post_detail, name='post_detail'),
	path(r'^delete_comment/(?P<comment_id>\d+)$', delete_comment, name='delete-comment'),
	path(r'^add_post$', add_post, name='add-post'),
	path(r'^update_post/(?P<post_id>\d+)$', update_post, name='update-post'),	
]