from django.db import models
from django.urls import reverse
from account.models import User
from blog.models import Blog
from appblog.models import MyBlog

class ComentsBlog(models.Model):
    titel = models.CharField(max_length=50)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name= 'coments_user_blog', on_delete=models.CASCADE , default=True)
    likes = models.ManyToManyField(User, related_name= 'coments_likes_blog', blank= True)
    unlikes = models.ManyToManyField(User, related_name= 'coments_unlides_blog', blank= True)
    appblog = models.ForeignKey(MyBlog , related_name= 'coments_myblog', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("blog:list")
    
    def __str__(self):
        return self.titel

class Coments(models.Model):
    choices = (
        ('y' , 'yes'),
        ('i' , 'I do not know'),
        ('n' , 'no'),
    )
    choice = (
        ('0' , '0'),
        ('1' , '1'),
        ('2' , '2'),
        ('3' , '3'),
        ('4' , '4'),
        ('5' , '5'),
    )
    sagestion = models.CharField(max_length=50 , choices=choices)
    score = models.CharField(max_length=50 , choices=choice)
    titel = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField(upload_to='coments_media')
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name= 'coments_user', on_delete=models.CASCADE , default=True)
    likes = models.ManyToManyField(User, related_name= 'coments_likes', blank= True)
    unlikes = models.ManyToManyField(User, related_name= 'coments_unlides', blank= True)
    blog = models.ForeignKey(Blog , related_name= 'coments_blog', on_delete=models.CASCADE)
    bad = models.TextField()
    good = models.TextField()
    def get_absolute_url(self):
        return reverse("blog:list")
    
    def __str__(self):
        return self.titel