from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogApp(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    title = models.CharField(max_length = 150)
    description = models.TextField()
    image = models.ImageField(upload_to="blog_image/")

    # To read models from shell
    # from blog.models import *
    # blog.objects.all()[0]
