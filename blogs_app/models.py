from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title=models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title=models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title=models.CharField(max_length=255)
    date=models.DateTimeField(null=True,blank=True)
    slug=models.SlugField(null=True, blank=True)
    image=models.ImageField(upload_to='posts',null=True,blank=True)
    content=models.TextField()
    author=models.ForeignKey(User , on_delete=models.SET_NULL ,null=True,related_name='posts')
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    tags=models.ManyToManyField(Tag,related_name='posts')
    likes=models.ManyToManyField(User,related_name='post_liked')
    
    def __str__(self):
        return self.title
    
    


class Comment(models.Model):
    username=models.CharField(max_length=255)
    email=models.EmailField(null=True,blank=True)
    text=models.TextField()
    post=models.ForeignKey(Post, on_delete=models.CASCADE ,related_name='comments')      
    is_approved=models.BooleanField(default=True)
    









