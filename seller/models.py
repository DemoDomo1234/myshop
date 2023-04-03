from django.db import models
from django.contrib.gis.db import models
from account.models import User
from prodact.models import Prodact
from address.models import Address
from base.models import *


class ProdactSeller(models.Model):
    prodact = models.ForeignKey(Prodact, related_name='seller_blog',  on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='blog_seller', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, related_name='blog_address_seller', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True)
    number = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True )
    published = models.BooleanField(default=False)

    class Meta :
        ordering = ['-price']


class ColorNum(models.Model):
    size = models.ForeignKey(Sizes, related_name='size_num', on_delete=models.CASCADE, blank=True, null=True)
    prodact = models.ForeignKey(Prodact, related_name='log_num', on_delete=models.CASCADE)
    color = models.ForeignKey(Colors, related_name='colors_num', on_delete=models.CASCADE, blank=True, null=True)
    num = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    nums = models.PositiveIntegerField(blank=True, null=True, default=0)
    seller = models.ForeignKey(ProdactSeller, related_name='num_seller', on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.color.color


class CompanySeller(models.Model):
    choices = (
        ('d', 'تجاری'),
        ('s', 'قیر تجاری'),
        ('n', 'شخصی'),
    )
    user = models.OneToOneField(User, related_name='user_seller_company' , on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=200, choices=choices)
    fixed_number = models.CharField(max_length=11)
    economic_code = models.CharField(max_length=11)
    permission_to_sign = models.CharField(max_length=11)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class SellerAccount(models.Model):
    choices = (
        ('1', '1-10'),
        ('2', '10-100'),
        ('3', '100-1000'),
    )
    choice = (
        ('hko', 'خوراکی'),
        ('kha', 'خانگی'),
        ('b', 'برقی'),
        ('e', 'الکترونیکی'),
        ('gh', 'قیره'),
    )
    user = models.OneToOneField(User , related_name='user_seller_account' , on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    shaba_nmber = models.CharField(max_length=24)
    shop_number = models.CharField(max_length=200, choices=choices)
    shop_type = models.CharField(max_length=200, choices=choice)
    tax = models.DateField(null=True, blank=True)
    national_card = models.ImageField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name
    
    