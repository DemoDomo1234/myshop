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
    published = models.BooleanField(default=False)

    class Meta :
        ordering = ['-date']

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
    published = models.BooleanField(default=False)
    
    class Meta :
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse("blog:list")
    
    def __str__(self):
        return self.titel

class Custion(models.Model):
    one_respones = models.ForeignKey('self', related_name="one_custion", on_delete=models.CASCADE , null=True , blank=True , default=None)
    tow_respones = models.ForeignKey('self', related_name="tow_custion", on_delete=models.CASCADE , null=True , blank=True , default=None)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name= 'user_custion', on_delete=models.CASCADE , default=True)
    likes = models.ManyToManyField(User, related_name= 'likes_custion', blank= True)
    unlikes = models.ManyToManyField(User, related_name= 'unlides_custion', blank= True)
    model = models.ForeignKey(Blog , related_name= 'custion', on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    class Meta :
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse("blog:list")
    
    def __str__(self):
        return self.body