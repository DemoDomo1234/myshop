from django.db import models
from django.contrib.gis.db import models
from account.models import User
from django.urls import reverse


class Category(models.Model):
    more = models.ForeignKey('self' , related_name="more_categorys", on_delete=models.SET_NULL , blank=True , null=True , default=None)
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

class Address(models.Model):
    user = models.ForeignKey(User, related_name=("adres_user"), on_delete=models.CASCADE)
    floor = models.CharField(max_length=20)
    plaque = models.CharField(max_length=5)
    name = models.CharField(max_length=200 )
    location = models.PointField()
    number = models.CharField(max_length=11)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Order(models.Model):
    received = models.BooleanField(default=False)
    user = models.ForeignKey(User , related_name='order_user' , null=True , on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True , null=True )
    price = models.PositiveIntegerField(blank=True)
    address = models.ForeignKey(Address , related_name='seller' , on_delete = models.CASCADE , blank=True , null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    online = models.BooleanField(default=True)
    save = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    destroyed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.user

class List(models.Model):
    titel = models.CharField(max_length=50 , unique=True)
    user = models.ForeignKey(User, related_name='list_user', on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.titel

class Blog(models.Model) :
    titel = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to = 'image')
    price = models.PositiveIntegerField()
    like = models.ManyToManyField(User , related_name='like' , blank = True)
    seller = models.ForeignKey(User , related_name='seller' , on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now_add=True )
    discount = models.PositiveIntegerField(blank=True)
    cart = models.ManyToManyField(User , related_name='cart' , blank= True)
    lists = models.ManyToManyField(List , related_name='list' , blank= True)
    number = models.PositiveIntegerField()
    category = models.ManyToManyField(Category , related_name='blog_categorys')
    notifications =  models.ManyToManyField(User , related_name='blog_notifications' , blank = True)
    color = models.ManyToManyField(Colors , related_name='colors' , blank= True)
    size = models.ManyToManyField(Sizes , related_name='sizes' , blank= True)

    def get_absolute_url(self):
        return reverse("blog:detail",args=[self.id] )

    def __str__(self):
        return self.titel

class OrderItem(models.Model):
    blog = models.ForeignKey(Blog , related_name='blog' ,  on_delete=models.CASCADE)
    num = models.PositiveIntegerField()
    order = models.ForeignKey(Order , related_name='item' ,  on_delete=models.CASCADE)
    color = models.OneToOneField(Colors , related_name='colores' , blank= True , on_delete = models.CASCADE)
    size = models.OneToOneField(Sizes , related_name='sizees' , blank= True , on_delete = models.CASCADE)

    def __str__(self):
        return self.blog

class Nums(models.Model):
    num = models.PositiveIntegerField()
    model = models.OneToOneField(Blog , related_name="nums", on_delete=models.CASCADE)

class Notifications(models.Model):
    user = models.ForeignKey(User, related_name=("noty_user"), on_delete=models.CASCADE)
    titel = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.titel

class Images(models.Model):
    blog = models.ForeignKey(Blog , related_name="blog_images_model" , on_delete = models.CASCADE , null =  True , blank = True)
    myblog = models.ForeignKey('appblog.MyBlog' , related_name="myblog_images_model" , on_delete = models.CASCADE , null =  True , blank = True)    
    image = models.ImageField( upload_to='media' , null =  True , blank = True)
