from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', login_required(views.PostNew.as_view()), name='post_new'),
    path('post/<int:pk>/edit/', login_required(views.PostEdit.as_view()), name='post_edit'),
    path('drafts/', login_required(views.PostDraftList.as_view()), name='post_draft_list'),
    path('post/<int:pk>/publish/', login_required(views.PostPublish.as_view()), name='post_publish'),
    path('post/<int:pk>/remove/', login_required(views.PostRemove.as_view()), name="post_remove"),
    path('post/<int:pk>/sendPost', login_required(views.SendPost.as_view()), name="send_post"),
    path('sendEmail', login_required(views.SendEmail.as_view()), name="send_email"),
    path('post/<int:pk>/sendPost/sendEmail', login_required(views.SendEmail.as_view()), name="send_email"),

]