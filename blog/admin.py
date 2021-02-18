from django.contrib import admin
from .models import Post



class BlogsAdmin(admin.ModelAdmin):
    model = Post

admin.site.register(Post, BlogsAdmin)