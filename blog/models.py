from django.db import models
from django.contrib.gis.db import models
from account.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from mdeditor.fields import MDTextField

class Brand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand

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
    name = models.CharField(max_length=200)
    location = models.PointField()
    number = models.CharField(max_length=11)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Order(models.Model):
    received = models.BooleanField(default=False)
    user = models.ForeignKey(User , related_name='order_useres' ,  on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True )
    price = models.PositiveIntegerField(blank=True , null=True)
    address = models.ForeignKey(Address , related_name='order_addresses' , on_delete = models.CASCADE , null=True , blank=True)
    time = models.DateTimeField(null=True , blank=True)
    online = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    destroyed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class List(models.Model):
    titel = models.CharField(max_length=50 , unique=True)
    user = models.ForeignKey(User, related_name='list_user', on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.titel

class Blog(models.Model) :
    titel = models.CharField(max_length=100)
    body = MDTextField()
    image = models.ImageField(upload_to = 'image')
    price = models.PositiveIntegerField()
    like = models.ManyToManyField(User , related_name='like' , blank = True)
    seller = models.ForeignKey(User , related_name='seller' , on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now_add=True )
    discount = models.PositiveIntegerField(blank=True)
    lists = models.ManyToManyField(List , related_name='list' , blank= True)
    number = models.PositiveIntegerField()
    category = models.ManyToManyField(Category , related_name='blog_categorys')
    notifications =  models.ManyToManyField(User , related_name='blog_notifications' , blank = True)
    address = models.ForeignKey(Address , related_name='blog_address' , on_delete = models.PROTECT)
    garanty = MDTextField()
    brand = models.ForeignKey(Brand , related_name='blog_brand' , on_delete = models.CASCADE , null=True , blank=True)
    tags = TaggableManager()
    weigth = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    published = models.BooleanField(default=False)
    sizes = models.ManyToManyField(Sizes , related_name='blog_size_num' , blank= True )
    color = models.ManyToManyField(Colors , related_name='blog_colors_num' , blank= True)


    def get_absolute_url(self):
        return reverse("blog:detail",args=[self.id] )

    def __str__(self):
        return self.titel

class OrderItem(models.Model):
    blog = models.ForeignKey(Blog , related_name='blog' ,  on_delete=models.CASCADE)
    seller = models.ForeignKey(User , related_name='item_seller' , on_delete = models.CASCADE)
    num = models.PositiveIntegerField()
    order = models.ForeignKey(Order , related_name='item' ,  on_delete=models.CASCADE)
    color = models.ForeignKey(Colors , related_name='colores' , blank= True , null=True , on_delete = models.CASCADE)
    size = models.ForeignKey(Sizes , related_name='sizees' , blank= True , null=True , on_delete = models.CASCADE)

    def __str__(self):
        return self.blog.titel

class BlogSeller(models.Model):
    blog = models.ForeignKey(Blog , related_name='seller_blog' ,  on_delete=models.CASCADE)
    seller = models.ForeignKey(User , related_name='blog_seller' , on_delete = models.CASCADE)
    address = models.ForeignKey(Address , related_name='blog_address_seller' , on_delete = models.CASCADE)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True)
    number = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True )
    garanty = MDTextField()
    published = models.BooleanField(default=False)

class Nums(models.Model):
    num = models.PositiveIntegerField()
    blog = models.OneToOneField(Blog , related_name="numes_myblog", on_delete=models.CASCADE)

class Notifications(models.Model):
    user = models.ForeignKey(User, related_name=("noty_user"), on_delete=models.CASCADE)
    titel = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.titel

class Images(models.Model):
    blog = models.ForeignKey(Blog , related_name="blog_images_model" , on_delete = models.CASCADE , null =  True , blank = True)
    image = models.ImageField( upload_to='media' , null =  True , blank = True)

class ColorNum(models.Model):
    size = models.ForeignKey(Sizes , related_name='size_num' , on_delete=models.CASCADE , blank = True , null = True)
    blog = models.ForeignKey(Blog , related_name='blog_num' ,  on_delete=models.CASCADE)
    color = models.ForeignKey(Colors , related_name='colors_num' ,  on_delete=models.CASCADE , blank = True , null = True)
    num = models.PositiveIntegerField()
    nums = models.PositiveIntegerField(blank = True , null = True , default = 0)
    seller = models.ForeignKey(User , related_name='num_seller' , on_delete = models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.color.color

class Advertising(models.Model):
    image = models.ImageField( upload_to='media' , null =  True , blank = True)
    brand = models.ForeignKey(Brand , related_name='advertising_brand' , on_delete = models.CASCADE , null=True , blank=True)
