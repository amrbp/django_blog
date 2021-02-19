from django.contrib import admin
from .models import Post ,Comment



class BlogsAdmin(admin.ModelAdmin):
    model = Post

class CommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(Post, BlogsAdmin)
admin.site.register(Comment, CommentAdmin)