from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post , Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy ,reverse
from django.http import HttpResponseRedirect
from .forms import CommentForm 

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.htm', context)

def about(request):
    return render(request, 'blog/about.htm')

def LikeView(request, pk):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.htm'
    context_object_name = 'posts'
    ordering = ['-id']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.htm'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        comments_connected = Comment.objects.filter(post_id=self.get_object()).order_by('-id')
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['total_likes'] = likes_connected.total_likes()
        data['comments'] = comments_connected
        data['post_is_liked'] = liked
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),user=self.request.user,post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content','image']
    template_name = 'blog/post_form.htm'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content','image']
    template_name = 'blog/post_form.htm'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

