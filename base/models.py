from django.db import models
from django.contrib.gis.db import models
from account.models import User


class Brand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand


class Category(models.Model):
    more = models.ForeignKey('self', related_name="more_categorys", on_delete=models.SET_NULL, blank=True, null=True, default=None)
    titel = models.CharField(max_length=50)

    def __str__(self):
        return self.titel


class Colors(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.color


class Sizes(models.Model):
    size = models.CharField(max_length=100)

    def __str__(self):
        return self.size


class List(models.Model):
    titel = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, related_name='list_user', on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.titel


class Notifications(models.Model):
    user = models.ForeignKey(User, related_name="noty_user", on_delete=models.CASCADE)
    titel = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.titel


class Images(models.Model):
    blog = models.ForeignKey('prodact.Prodact', related_name="blog_images_model", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField( upload_to='media', null=True, blank=True)


class Advertising(models.Model):
    image = models.ImageField( upload_to='media', null= True, blank=True)
    brand = models.ForeignKey(Brand, related_name='advertising_brand', on_delete=models.CASCADE, null=True, blank=True)


