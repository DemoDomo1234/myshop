from django.db import models
from django.contrib.gis.db import models
from account.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from mdeditor.fields import MDTextField
from base.models import Category, List, Brand, Colors, Sizes


class Prodact(models.Model):
    titel = models.CharField(max_length=100)
    body = MDTextField()
    image = models.ImageField(upload_to='image')
    like = models.ManyToManyField(User, related_name='like', blank=True)
    seller = models.ForeignKey(User, related_name='seller', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    lists = models.ManyToManyField(List, related_name='blog_list', blank=True)
    category = models.ManyToManyField(Category, related_name='blog_categorys')
    notifications =  models.ManyToManyField(User, related_name='blog_notifications', blank=True)
    brand = models.ForeignKey(Brand, related_name='blog_brand', on_delete=models.CASCADE, null=True, blank=True)
    tags = TaggableManager()
    weigth = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    published = models.BooleanField(default=False)
    sizes = models.ManyToManyField(Sizes, related_name='blog_size_num', blank=True )
    color = models.ManyToManyField(Colors, related_name='blog_colors_num', blank=True)
    garanty = MDTextField()


    class Meta:
        ordering = ['-time']

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.id])

    def __str__(self):
        return self.titel


class Nums(models.Model):
    num = models.PositiveIntegerField()
    blog = models.OneToOneField(Prodact, related_name="numes_prodact", on_delete=models.CASCADE)

