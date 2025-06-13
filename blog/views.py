from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.views import View
from django.core.mail import send_mail

class PostList(View):
    def get(self, request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})

class PostNew(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form' : form})
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, 'blog/post_edit.html', {'form': form})

class PostEdit(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form = PostForm(instance = post)
        return render(request, 'blog/post_edit.html', {'form' : form})
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, 'blog/post_edit.html', {'form': form})
class PostDraftList(View):
    def get(self, request):
        posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        return render(request, 'blog/post_draft_list.html', {'posts' : posts})

class PostPublish(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.publish()
        return redirect("post_detail", pk=self.kwargs['pk'])

class PostRemove(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.delete()
        return redirect('post_list')

class SendPost(View):
    def get(self, request, *args, **kwargs):
        return redirect("send_email", pk = self.kwargs['pk'])

class SendEmail(View):
    def get(self, request, *args, **kwargs):
        message = ""
        subject = ""
        if self.kwargs:
            message = get_object_or_404(Post, pk=self.kwargs['pk']).text
            subject = get_object_or_404(Post, pk=self.kwargs['pk']).title
        return render(request, "blog/send_email.html", {'result': "", 'subject' : subject, 'message' : message})
    def post(self, request, *args, **kwargs):
        result = "All fields are required"
        address = request.POST.get('address')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        if address and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                result = 'Email sent successfully'
            except Exception as e:
                result = "Something went wrong. Please check if the email address you provided is valid."
        return render(request, "blog/send_email.html", {'result': result, 'subject' : "", 'message' : ""})
