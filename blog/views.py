from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy 

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.htm', context)


def about(request):
    return render(request, 'blog/about.htm')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.htm'
    context_object_name = 'posts'
    ordering = ['-id']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.htm'


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
