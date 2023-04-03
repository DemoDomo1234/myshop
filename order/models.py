from django.db import models
from django.contrib.gis.db import models
from account.models import User
from base.models import *
from prodact.models import Prodact
from seller.models import ProdactSeller
from address.models import Address


class Order(models.Model):
    received = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='order_useres',  on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True )
    price = models.PositiveIntegerField(blank=True, null=True)
    address = models.ForeignKey(Address, related_name='order_addresses', on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    online = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    destroyed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    blog = models.ForeignKey(Prodact, related_name='blog',  on_delete=models.CASCADE)
    seller = models.ForeignKey(ProdactSeller, related_name='item_seller', on_delete=models.CASCADE)
    num = models.PositiveIntegerField()
    order = models.ForeignKey(Order, related_name='item',  on_delete=models.CASCADE)
    color = models.ForeignKey(Colors, related_name='colores', blank=True, null=True, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, related_name='sizees', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="item_order_user", on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.titel

