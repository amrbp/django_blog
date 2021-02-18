from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.views.generic import ListView,DetailView


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.htm', {'form': form})


@login_required
def profile(request):
    current_user = request.user
    context = {
        'posts': Post.objects.filter(author_id=current_user).order_by('-date_posted')
    }
    return render(request, 'users/profile.htm', context)


