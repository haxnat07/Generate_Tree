from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})

from django.contrib.auth.models import User

class People(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    

class Entries(models.Model):
    user = models.ForeignKey(People, on_delete=models.CASCADE)
    year = models.IntegerField()
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000) 
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return self.user.name
    
    class Meta:
        verbose_name = "Entries"
        verbose_name_plural = "Entries"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.CharField(max_length=16)
    def __str__(self):
        return self.user.username