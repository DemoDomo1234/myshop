from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from .models import Order, OrderItem
from base.models import Colors, Sizes
from address.models import Address
from seller.models import ColorNum, ProdactSeller
from prodact.models import Prodact, Nums
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from django.contrib.gis.db.models.functions import Distance
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required



class OrderClass :

    
    def __init__(self, request, id=None):
        self.request = request
        self.user = request.user
        self.context = None
        self.id = id


    def create_order(self):
        order = get_object_or_404(Order, user=self.user, current=True)
        a = 0
        price = 0
        addresses = Address.objects.filter(user=self.user)
        item = OrderItem.objects.filter(order=order)
        if self.user == order.user :
            if self.request.method == 'POST' :
                address_name = self.request.POST['address']
                time = self.request.POST['time']
                payment = self.request.POST['payment']
                address = get_object_or_404(Address , name = address_name , user = user)
                order.address = address
                order.time = time
                if payment == 'cash' :
                    order.online = False
                for item in item:
                    blog = get_object_or_404(ProdactSeller , blog = item[a].blog , seller__id = item[a].seller.id)
                    try :
                        color = get_object_or_404(ColorNum , blog=item[a].seller.blog , color = item[a].color , seller = item[a].seller)
                    except :
                        color = get_object_or_404(ColorNum , blog=item[a].seller.blog , size = item[a].size , seller = item[a].seller)

                    send = (blog.blog.size * 10 ) + (blog.blog.weigth * 5 ) * int(i)
                    map = Distance(blog.address.location , order.address.location)
                    send += map
                    send *= 5000
                    if self.user.is_special :
                        send = 0
                    price += (blog.price - blog.discount + color.price) * int(i)
                    price += send
                    order.price = price
                    order.ordered = True
                    order.current = False
                    order.save()
                    a += 1
                if order.online == True :
                    return redirect('blog:go_to_gateway')
                else:
                    return redirect('blog:list')
        else:
            return redirect('blog:list')
        self.context = {'item' : item ,
        'address':addresses }


    def shop(self):
        blog = get_object_or_404(Prodact, id=id)
        if self.request.method == 'POST':
            order = get_object_or_404(Order , user = self.user , current=True)
            num = self.request.POST['num']
            seller = self.request.POST['seller']
            try:
                size = self.request.POST['size']
                nums = get_object_or_404(Nums , blog=blog)
                nums.num += int(num)
                nums.save()
                myseller = get_object_or_404(ProdactSeller , id = seller)
                mysize = get_object_or_404(Sizes , size = size)
                item = OrderItem.objects.create(blog=blog , num=num , order=order ,
                size=mysize , seller=myseller ,user=self.user)
                item.save()
                color = get_object_or_404(ColorNum , blog=blog , size=mysize , seller = myseller)
                color.num -= int(num)
                color.nums += int(num)
                color.save()
            except:
                color = self.request.POST['color']
                mycolor = get_object_or_404(Colors , color = color)
                nums = get_object_or_404(Nums , blog=blog)
                nums.num += int(num)
                nums.save()
                myseller = get_object_or_404(ProdactSeller , id = seller)
                item = OrderItem.objects.create(blog=blog , num=num , order=order ,
                color=mycolor , seller=myseller)
                item.save()
                color = get_object_or_404(ColorNum , blog=blog , color=mycolor)
                color.num -= int(num)
                color.nums += int(num)
                color.save()
                myseller.number -= int(num)
                myseller.save() 
            return redirect('blog:detail' , id)
        else:
            return redirect('blog:list')


    def unshop(self):
        item = get_object_or_404(OrderItem , id = id)
        blog = get_object_or_404(Prodact , id = item.blog.id)
        try :
            color = get_object_or_404(ColorNum , blog = blog , color = item.color , seller = item.seller)
        except :
            color = get_object_or_404(ColorNum , blog = blog , size = item.size , seller = item.seller)
        nums = get_object_or_404(Nums , blog=blog)
        user = self.request.user
        if user == item.user :
            seler = get_object_or_404(ProdactSeller , seller = user)
            seler.number += item.num
            seler.save()
            color.num += item.num
            color.nums -= item.num
            color.save()
            nums.num -= item.num 
            nums.save()
            item.delete()
            return redirect('blog:detail' , blog.id)
        else :
            return redirect('blog:list')


    def update_item(self):
        item = get_object_or_404(OrderItem , id = id)
        blog = get_object_or_404(ProdactSeller , blog = item.blog , seller__id = item.seller.id)
        try :
            color = get_object_or_404(ColorNum , blog=item.seller.blog , color = item.color , seller = item.seller)
        except :
            color = get_object_or_404(ColorNum , blog=item.seller.blog , size = item.size , seller = item.seller)
        if self.request.method == 'POST' :
            if self.request.user == item.user : 
                num = self.request.POST['num']
                if int(num) > item.num :
                    nums = int(num) - item.num
                    blog.number += nums
                    item.num += nums
                    color.num += nums
                    color.nums -= nums
                else:
                    nums = item.num - int(num)
                    blog.number -= nums
                    item.num -= nums
                    color.num -= nums
                    color.nums += nums
                blog.save()
                color.save()
                item.save()
            else:
                return redirect('blog:list')
        else:
            self.context = {'item':item}
