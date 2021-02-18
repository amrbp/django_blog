from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
