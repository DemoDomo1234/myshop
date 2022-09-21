from django.db import models
from account.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from mdeditor.fields import MDTextField


class MyBlog(models.Model):
    choices = (
        ('d' , 'draft'),
        ('s' , 'special'),
        ('n' , 'normal'),
    )
    titel = models.CharField(max_length=100)
    body = MDTextField()
    image = models.ImageField(upload_to = 'myblog_image')
    likes = models.ManyToManyField(User , related_name='myblog_likes' , blank = True)
    saved = models.ManyToManyField(User , related_name='myblog_saved' , blank = True)
    author = models.ForeignKey(User , related_name='myblog_seller' , on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now_add=True )
    status = models.CharField(max_length=20 , choices = choices)
    film = models.FileField(upload_to = 'myblog_film' , null = True , blank = True)
    music = models.FileField(upload_to = 'myblog_music' , null = True , blank = True)
    category = models.ManyToManyField('blog.Category' , related_name='myblog_categorys')
    tags = TaggableManager()
    published = models.BooleanField(default=False)

    class Meta :
        ordering = ['-time']

    def get_absolute_url(self):
        return reverse("myblog:list")

    def __str__(self):
        return self.titel

class Nums(models.Model):
    view =  models.ManyToManyField(User , related_name='view' , blank = True)
    model = models.OneToOneField(MyBlog , related_name="nums", on_delete=models.CASCADE)
