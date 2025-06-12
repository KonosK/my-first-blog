from django.urls import path
from . import views
from .views import PostNew, PostList
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', login_required(PostNew.as_view()), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEdit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name="post_remove"),
]