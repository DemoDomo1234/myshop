from django.shortcuts import redirect , render , HttpResponse
from .models import (Brand , Images , ColorNum , Category , Colors ,
                    Sizes , Address , Order , List , Blog , OrderItem ,
                    BlogSeller , Nums , Notifications , Advertising)
from django.contrib.postgres.search import TrigramSimilarity
from coment.forms import ComentsForm , CustionForm
from coment.models import Coments , Custion
from django.core.mail import send_mail
from account.models import User
from django.contrib.gis.geos import Point
from .forms import *
from django.db.models import Count , Sum
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from .func import timer
# from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance
from .models import ColorNum
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from taggit.models import Tag 

def home(request):
    blog = {}
    advertising = Advertising.objects.all()
    category_max = Category.objects.filter(blog_categorys__numes_myblog__num__gt = 1000)
    num_max = Blog.objects.filter(numes_myblog__num__gt = 1000 , published = True)
    brand_max = Brand.objects.filter(blog_brand__numes_myblog__num__gt = 1000)
    myblog = Blog.objects.filter(discount__gt = 30 , published = True)
    if 'search' in request.GET :
        search = request.GET['search']
        blog = Blog.objects.annotate(blogsearch=TrigramSimilarity(
        'titel', search),).filter(
        blogsearch__gt=0.3 , published = True).order_by('-blogsearch')
    return render(request , 'blog/index.html' , {'blog':blog , 
    'myblog':myblog , 'num_max':num_max , 'brand_max':brand_max ,
    'category_max':category_max ,'advertising':advertising})

def detail(request , id):
    user = request.user
    blog = Blog.objects.get(id = id)
    coments = Coments.objects.filter(blog = blog , published = True )
    custion = Custion.objects.filter(model = blog , published = True , one_respones = None , tow_respones = None)
    images = Images.objects.filter(blog = blog)
    nums = Nums.objects.filter(blog = blog)
    colors = ColorNum.objects.filter(blog = blog , published = True)
    category = blog.category.all()
    sellers = BlogSeller.objects.filter(blog=blog , published = True)
    tags = blog.tags.all()
    tag = blog.tags.values_list('id' , flat = True)
    blogs = Blog.objects.filter(tags__in = tag , published = True).exclude(id = blog.id)
    myblogs = blogs.annotate(tags_count = Count('tags')).order_by('-tags_count')
    if user.is_authenticated :
        lists = List.objects.filter(user=user)
        order = Order.objects.get(user = user , current=True)
        item = OrderItem.objects.filter(order = order)
        if request.method == 'POST' :
            form1 = ComentsForm(request.POST , request.FILES)
            form2 = CustionForm(request.POST)
            if form1.is_valid():
                titel = form1.cleaned_data['titel']
                body = form1.cleaned_data['body']
                bad = form1.cleaned_data['bad']
                good = form1.cleaned_data['good']
                image = form1.cleaned_data['image']
                sagestion = form1.cleaned_data['sagestion']
                score = form1.cleaned_data['score']

                text = Coments.objects.create(body = body , user = user ,
                        blog = blog , image = image , titel=titel , bad=bad ,
                        good=good , sagestion=sagestion , score=score )
                text.save()
                return redirect('blog:detail' , blog.id)

            if form2.is_valid():
                body = form2.cleaned_data['custion_body']
                new_custion = Custion.objects.create(body = body , user = user , model=blog)
                new_custion.save()
                return redirect('blog:detail' , blog.id)

                
        else:
            form1 = ComentsForm()
            form2 = CustionForm()

    else:
        return redirect('account:login')

    return render(request , 'blog/detail.html' , {'blog':blog , 'form1':form1 , 'form2':form2 ,
    'coments':coments , 'lists':lists , 'colors':colors , 'images':images  ,
    'category':category , 'sellers':sellers , 'myblogs':myblogs , 'items':item ,
    'custion':custion , 'tags':tags , 'nums':nums})

def create(request):
    user = request.user
    addresses = Address.objects.filter(user = user)
    brands = Brand.objects.all()
    category = Category.objects.all()
    sizes = Sizes.objects.all()
    colors = Colors.objects.all()

    if 'search' in request.GET :
        search = request.GET['search']
        category = category.annotate(categorysearch=TrigramSimilarity(
        'titel', search),).filter(
        categorysearch__gt=0.3).order_by('-categorysearch')
    if user.is_authenticated :
        if user.is_seller :       
            if request.method == "POST" :
                form = CreateForm(request.POST , request.FILES)
                if form.is_valid():

                    titel = form.cleaned_data['titel']
                    body = form.cleaned_data['body']
                    image = form.cleaned_data['image']
                    price = form.cleaned_data['price']
                    discount = form.cleaned_data['discount']
                    number = form.cleaned_data['number']
                    garanty = form.cleaned_data['garanty']
                    brand_name = request.POST['brand']
                    tags = form.cleaned_data['tags']
                    size = form.cleaned_data['size']
                    weigth = form.cleaned_data['weigth']
                    address_name = request.POST['address']

                    brand = Brand.objects.get(brand = brand_name)
                    address = Address.objects.get(name = address_name)

                    blog = Blog.objects.create(
                            titel = titel , body = body ,
                            image = image , number = number ,
                            price = price , seller = user ,
                            discount = discount , garanty = garanty ,
                            brand = brand , tags = tags , size=size ,
                            weigth=weigth , address = address)
                    
                    for cate in request.POST.getlist('category'):
                        category = Category.objects.get(titel = cate)
                        if category not in blog.category.all():

                            blog.category.add(category)

                    for mycolor in request.POST.getlist('color'):
                        color = Colors.objects.get(color = mycolor)
                        if color not in blog.color.all():

                            blog.color.add(color)

                    for mysize in request.POST.getlist('size'):
                        size = Sizes.objects.get(size = mysize)
                        if size not in blog.size.all():

                            blog.size.add(size)

                    blog.save()
                    nums = Nums.objects.create(blog=blog , num = 0)
                    nums.save()
                    return redirect('blog:detail' , blog.id)
                    
            else:
                form = CreateForm()
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'blog/create.html' , {'form':form , 'addresses':addresses , 
    'brands':brands , 'category':category , 'sizes':sizes , 'colors':colors})    

def update(request , id):
    blog = Blog.objects.get(id = id)
    brands = Brand.objects.all()
    mycategory = blog.category.all()
    id1 = mycategory.values_list('id' , flat=True)
    categorys = Category.objects.filter(id__gte = 0).exclude(id__in = id1)
    mycolor = blog.color.all()
    id1 = mycolor.values_list('id' , flat=True)
    colors = Colors.objects.filter(id__gte = 0).exclude(id__in = id1)
    mysize = blog.size.all()
    id1 = mysize.values_list('id' , flat=True)
    sizes = Sizes.objects.filter(id__gte = 0).exclude(id__in = id1)

    if 'search' in request.GET :
        search = request.GET['search']
        categorys = categorys.annotate(categorysearch=TrigramSimilarity(
        'titel', search),).filter(
        categorysearch__gt=0.3).order_by('-categorysearch')
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == blog.seller :
                if request.method == 'POST' :
                    form = UpdateForm(request.POST , request.FILES)
                    if form.is_valid():
                        titel = form.cleaned_data['titel']
                        body = form.cleaned_data['body']
                        image = form.cleaned_data['image']
                        price = form.cleaned_data['price']
                        discount = form.cleaned_data['discount']
                        number = form.cleaned_data['number']
                        garanty = form.cleaned_data['garanty']
                        mybrand = request.POST['brand']
                        tags = form.cleaned_data['tags']
                        brand = Brand.objects.get(brand = mybrand)
                        blog.titel = titel
                        blog.body = body
                        blog.image = image
                        blog.price = price
                        blog.seller = user
                        blog.time = blog.time
                        blog.discount = discount
                        blog.number = number
                        blog.granty = garanty
                        blog.brand = brand
                        blog.tags = tags

                        for cate in request.POST.getlist('category'):
                            category = Category.objects.get(titel = cate)
                            if category not in blog.category.all():
                                blog.category.add(category)

                        for cate in request.POST.getlist('categorys'):
                            category = Category.objects.get(titel= cate)
                            if category in blog.category.all():
                                blog.category.remove(category)

                    for mycolor in request.POST.getlist('color'):
                        color = Colors.objects.get(color = mycolor)
                        if color not in blog.color.all():

                            blog.color.add(color)

                    for mysize in request.POST.getlist('size'):
                        size = Sizes.objects.get(size = mysize)
                        if size not in blog.size.all():

                            blog.size.add(size)

                    for mycolor in request.POST.getlist('colors'):
                        color = Colors.objects.get(color = mycolor)
                        if color in blog.color.all():

                            blog.color.remove(color)

                    for mysize in request.POST.getlist('sizes'):
                        size = Sizes.objects.get(size = mysize)
                        if size in blog.size.all():

                            blog.size.remove(size)

                        blog.save()
                        return redirect('blog:list')
                else:
                    form = UpdateForm()
            else:
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request , 'blog/update.html' , {'form':form ,
    'mycategory':mycategory , 'categorys':categorys , 'brands':brands ,
    'mycolor':mycolor , 'colors':colors ,'mysize':mysize , 'sizes':sizes})
    
def delete(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == blog.seller :
                if request.method == 'GET' :   
                    blog.image.delete()
                    blog.delete()
                    return redirect('blog:list')
            else:
                 return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')

def like(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in blog.like.all() :
            blog.like.add(user)
            return redirect( 'blog:detail' , id)
    else:
        return redirect('account:login')

def unlike(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in blog.like.all() :
            blog.like.remove(user)
            return redirect( 'blog:detail' , id)
    else:
        return redirect('account:login')

def order(request):
    user = request.user
    order = Order.objects.get(user = user , current=True)
    a = 0
    price = 0
    addresses = Address.objects.filter(user =user)
    item = OrderItem.objects.filter(order = order)
    if request.method == 'POST' :
        address_name = request.POST['address']
        time = request.POST['time']
        payment = request.POST['payment']
        address = Address.objects.get(name = address_name , user = user)
        order.address = address
        order.time = time
        if payment == 'online' :
            order.online = True
        for i in request.POST.getlist('num'):
            blog = Blog.objects.get(id = item[a].blog.id)
            if item[a].seller == blog.seller :
                num = Nums.objects.get(blog=item[a].blog)
                try :
                    color = ColorNum.objects.get(blog=item[a].blog , color = item[a].color , seller = item[a].seller)
                except :
                    color = ColorNum.objects.get(blog=item[a].blog , size = item[a].size , seller = item[a].seller)

                if int(i) > item[a].num :
                    nums = int(i) - item[a].num
                    blog.number += nums
                    num.num += nums
                    item[a].num += nums
                    color.num += nums
                    color.nums -= nums
                else:
                    nums = item[a].num - int(i)
                    blog.number -= nums
                    num.num -= nums
                    item[a].num -= nums
                    color.num -= nums
                    color.nums += nums
                blog.save()
                num.save()
                color.save()
                item[a].save()
                send = (blog.size * 10 ) + (blog.weigth * 5 ) * int(i)
                map = Distance(blog.address.location , order.address.location)
                send += map
                send *= 5000
                if user.is_special :
                    send = 0
                price += (blog.price - blog.discount) * int(i)
                price += send
                order.price = price
                order.ordered = True 
                order.current = False
                order.save()
                print(price)
            else:
                blog = BlogSeller.objects.get(blog = item[a].blog , seller = item[a].seller)
                try :
                    color = ColorNum.objects.get(blog=item[a].item_seller.blogseller.blog , color = item[a].color , seller = item[a].seller)
                except :
                    color = ColorNum.objects.get(blog=item[a].item_seller.blogseller.blog , size = item[a].size , seller = item[a].seller)

                if int(i) > item[a].num :
                    nums = int(i) - item[a].num
                    blog.number += nums
                    blog.num += nums
                    item[a].num += nums
                    color.num += nums
                    color.nums -= nums
                else:
                    nums = item[a].num - int(i)
                    blog.number -= nums
                    blog.num -= nums
                    item[a].num -= nums
                    color.num -= nums
                    color.nums += nums

                blog.save()
                color.save()
                item.save()
                send = (blog.size * 10 ) + (blog.weigth * 5 ) * int(i)
                map = Distance(blog.address.location , order.address.location)
                send += map
                send *= 5000
                if user.is_special :
                    send = 0
                price += (blog.price - blog.discount) * int(i)
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
    return render(request , 'blog/order.html' , {'item' : item ,
    'address':addresses })

def shop(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if blog.number > 0 :
            if request.method == 'POST' :
                order = Order.objects.get(user = user , current=True)
                try:
                    color = request.POST['color']
                except:
                    size = request.POST['size']
                    seller = request.POST['seller']
                    num = request.POST['num']
                    nums = Nums.objects.get(blog=blog)
                    nums.num = num
                    nums.save()
                    myseller = User.objects.get(username = seller)
                    mysize = Sizes.objects.get(size = size)
                    item = OrderItem.objects.create(blog=blog , num=num , order=order ,
                    size=mysize , seller=myseller)
                    item.save()
                    color = ColorNum.objects.get(blog=blog , size=mysize , seller = myseller)
                    color.num -= int(num)
                    color.nums += int(num)
                    color.save()
                try:
                    size = request.POST['size']
                except:
                        color = request.POST['color']
                        mycolor = Colors.objects.get(color = color)
                        seller = request.POST['seller']
                        num = request.POST['num']
                        nums = Nums.objects.get(blog=blog)
                        nums.num = num
                        nums.save()
                        myseller = User.objects.get(username = seller)
                        item = OrderItem.objects.create(blog=blog , num=num , order=order ,
                        color=mycolor , seller=myseller)
                        item.save()
                        color = ColorNum.objects.get(blog=blog , color=mycolor)
                        color.num -= int(num)
                        color.nums += int(num)
                        color.save()
                if myseller != blog.seller :
                    seler = BlogSeller.objects.get(seller = myseller)
                    seler.number -= int(num)
                    seler.save()
                else:
                    blog.number -= int(num)
                    blog.save()      
                return redirect('blog:detail' , id)
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')

def unshop(request , id):
    item = OrderItem.objects.get(id = id)
    blog = Blog.objects.get(id = item.blog.id)
    try :
        color = ColorNum.objects.get(blog = blog , color = item.color , seller = item.seller)
    except :
        color = ColorNum.objects.get(blog = blog , size = item.size , seller = item.seller)
    nums = Nums.objects.get(blog=blog)
    user = request.user
    if user.is_authenticated :
        if user != blog.seller :
            seler = BlogSeller.objects.get(seller = user)
            seler.number += int(num)
            seler.save()
        else:
            blog.number += item.num 
        blog.number += item.num 
        color.num += item.num
        color.nums -= item.num
        color.save()
        blog.save()
        nums.num -= item.num 
        nums.save()
        item.delete()
        return redirect('blog:detail' , blog.id)
    else:
        return redirect('account:login')

def send_email(request):
    if request.method == "POST" :
        form = SendEmail(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            massage = form.cleaned_data['massage']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email'] 
            massages = '''
                        name : {0}
                        subject : {1}
                        message : {2}
                       '''.format(name , subject , massage)
            send_mail('message' , massages , 'demodomone@gmail.com' , [email] ,
            fail_silently=False , auth_password='g b r m d o g r x l s p u d j t')  
            return redirect('blog:list')
    form = SendEmail()
    return render(request , 'blog/sendmail.html' , {'form':form})

def create_list(request):
    user=request.user
    if user.is_authenticated :
        if request.method == 'POST':
            form = ListForm(request.POST)
            if form.is_valid():
                titel = form.cleaned_data['titel']
                body = form.cleaned_data['body']
                lists = List.objects.create(titel=titel ,
                user=user , body = body)
                lists.save()
                return redirect('blog:list')
        else:
            form = ListForm()
    else:
        return redirect('account:login')
    
    return render(request, 'blog/createlist.html' , {'form':form})

def update_list(request , id):
    lists = List.objects.get(id = id)
    user = request.user
    if user.is_authenticated :  
        if user == lists.user :
            if request.method == 'POST':
                form = ListForm(request.POST)
                if form.is_valid():
                    titel = form.cleaned_data['titel']
                    body = form.cleaned_data['body']
                    lists.titel = titel
                    lists.body = body
                    lists.save()
                    return redirect('blog:list')

            else:
                form = ListForm()
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request, 'blog/updatelist.html' , {'form':form})

def detail_list(request , id):
    lists = List.objects.get(id = id)
    blog = Blog.objects.filter(lists=lists)
    return render(request, 'blog/detaillist.html' , {'blog':blog})

def delete_list(request , id):
    lists = List.objects.get(id = id)
    user = request.user
    if user.is_authenticated :  
        if user == lists.user :
            if request.method == 'POST':
                lists.delete()
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('blog:list')
    return render(request , 'blog/deletelist.html')

def list_view(request , id):
    user = request.user
    listes = List.objects.filter(user = user)
    if user.is_authenticated :  
        if request.method == 'POST':
            titel = request.POST.getlist('titel')
            for i in titel :
                print(i)
                titels = List.objects.get(titel=i)
                blog = Blog.objects.get(id = id)
                if titels not in blog.lists.all() :
                    blog.lists.add(titels)
                    return redirect('blog:detail' , id)
    else:
        return redirect('account:login')
    return render(request, 'blog/list.html' , {'listes':listes})

def unlist_view(request , id):
    blog = Blog.objects.get(id = id)
    user=request.user
    if user.is_authenticated :  
        listes = blog.lists.filter(user=request.user)
        if request.method == 'POST':
            titel = request.POST.getlist('titel')
            for i in titel :
                titels = List.objects.get(titel=i)
                if titels in blog.lists.all() :
                    blog.lists.remove(titels)
                    return redirect('blog:detail' , id)
    else:
        return redirect('account:login')
    return render(request, 'blog/unlist.html' , { 'listes':listes})

def notifications(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in blog.notifications.all() :
            blog.notifications.add(user)
            return redirect( 'blog:detail' , id)
    return redirect('account:login')

def un_notifications(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in blog.notifications.all() :
            blog.notifications.remove(user)
            return redirect( 'blog:detail' , id)
    else:
        return redirect('account:login')

def share_post(request , id):
    blog = Blog.objects.get(id = id)
    if request.method == "POST" :
        form = Share(request.POST)
        if form.is_valid():
            url = request.build_absolute_uri(blog.get_absolute_url())
            email = form.cleaned_data['email'] 
            send_mail(blog.titel , url , 'demodomone@gmail.com' , [email] ,
            fail_silently=False , auth_password='g b r m d o g r x l s p u d j t')  
            return redirect('blog:detail' , id)
    form = Share()
    return render(request , 'blog/share.html' , {'form':form})

def add_address(request):
    user = request.user
    if user.is_authenticated :  
        if request.method =='POST':
            lat=float(request.POST['latitude'])
            long=float(request.POST['longitude'])
            location=Point(long,lat,srid=4326)
            form = AddressForm(request.POST)
            if form.is_valid():
                floor = form.cleaned_data['floor']
                plaque = form.cleaned_data['plaque']
                name = form.cleaned_data['name']
                number = form.cleaned_data['number']
                address = Address.objects.create(user=user , 
                location=location , floor=floor , plaque=plaque , name=name ,
                number=number)
                address.save()
                return redirect('account:detail' , user.id)
        else:
            form = AddressForm()
    else:
        return redirect('account:login')
    return render(request,'blog/addaddress.html' , {'form':form})

def update_address(request , id):
    user = request.user
    address = Address.objects.get(id = id)
    if user.is_authenticated : 
        if user == address.user :
            if request.method =='POST':
                lat=float(request.POST['latitude'])
                long=float(request.POST['longitude'])
                form = UpdateAddressForm(request.POST)
                if form.is_valid():
                    address.floor = form.cleaned_data['floor']
                    address.plaque = form.cleaned_data['plaque']
                    address.name = form.cleaned_data['name']
                    address.number = form.cleaned_data['number']
                    address.location=Point(long,lat,srid=4326) 
                    address.save()
            else:
                form = UpdateAddressForm()
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')        
    return render(request,'blog/updateaddress.html' , {'form':form})

def delete_address(request , id):
    user = request.user
    address = Address.objects.get(id = id)
    if user.is_authenticated : 
        if user == address.user :
            if request.method =='POST':
                address.delete()
                return redirect('account:detail' , user.id)
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request,'blog/deleteaddress.html')

def create_image(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :  
            if blog.seller == user :     
                if request.method == "POST" :
                    form = ImageForm(request.POST , request.FILES)
                    if form.is_valid():
                        image = form.cleaned_data['image']
                        images = Images.objects.create(
                            image = image , blog = blog)
                        images.save()
                        return redirect('blog:list')
                else:
                    form = ImageForm()
            else:
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request , 'blog/create-image.html' , {'form':form})    

def update_image(request , id):
    images = Images.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == images.blog.seller or user == images.myblog.author :
                if request.method == 'POST' :
                    form = ImageForm(request.POST ,  request.FILES)
                    if form.is_valid():
                        image = form.cleaned_data['image']
                        images.image = image
                        images.save()
                        return redirect('blog:list')
                else:
                    form = ImageForm()
            else:
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request , 'blog/update-image.html' , {'form':form})

def delete_image(request , id):
    images = Images.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == images.blog.seller or user == images.myblog.author :
                if request.method == 'POST' :   
                    images.image.delete()
                    images.delete()
                    return redirect('blog:list')
            else:
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request , 'blog/delete-image.html')

def create_category(request):
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if request.method == "POST":
                form = CreateCategory(request.POST)
                if form.is_valid():
                    titel = form.cleaned_data['titel']
                    more = form.cleaned_data['more']
                    category = Category.objects.create(titel=titel , more=more)
                    category.save()
                    return redirect('blog:create')
            else:
                form = CreateCategory()
        else:
            redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request, 'blog/createcategory.html' , {'form':form})

def category_list(request , id):
    category = Category.objects.get(id = id)
    blog = Blog.objects.filter(category = category , published = True)
    return render(request, 'blog/category-list.html' , {'blog':blog})

def order_pdf(request , id):
    order = Order.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == order.user :
            pdf = HttpResponse(content_type='application/pdf')
            pdf["ontent-Dispoxiyions"] = 'attachment;filename=order' +  str(request.user.username)+str(datetime.datetime.now())+'.pdf'
            html_url  = "blog/pdf.html"
            html = get_template(html_url)
            text = {'order':order}
            my_html = html.render(text)
            pisa.CreatePDF(my_html , dest=pdf)
            return pdf
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')

def order_detail(request , id):
    order = Order.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == order.user :
            item = OrderItem.objects.filter(order = order)
            return render(request , 'blog/order-detail.html' , {'order':order , 'item':item})
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')

def sellers(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    addresses = Address.objects.filter(user =user)
    if user.is_authenticated :
        if request.method == 'POST' :
            form = Sellers(request.POST)
            if form.is_valid():
                price = form.cleaned_data['price']
                discount = form.cleaned_data['discount']
                number = form.cleaned_data['number']
                garanty = form.cleaned_data['garanty']
                myaddress = request.POST['address']
                address = Address.objects.get(user=user , name = myaddress)
                seller = BlogSeller.objects.create(blog = blog , seller = user , address = address , 
                number = number , price = price , discount = discount , 
                garanty = garanty)
                seller.save()
                return redirect('blog:detail' , id)
        else:
            form = Sellers()
    else:
        return redirect('account:login')

    return render(request , 'blog/sellers.html' , {'form':form , 'addresses':addresses})

def sellers_update(request , id):
    seller = BlogSeller.objects.get(id = id)
    user = request.user
    addresses = Address.objects.filter(user = user)
    if user.is_authenticated :
        if request.method == 'POST' :
            form = Sellers(request.POST)
            if form.is_valid():
                price = form.cleaned_data['price']
                discount = form.cleaned_data['discount']
                number = form.cleaned_data['number']
                myaddress = request.POST['address']
                garanty = form.cleaned_data['garanty']
                address = Address.objects.get(user=user , name = myaddress)
                seller.price = price
                seller.number = number
                seller.discount = discount
                seller.garanty = garanty
                seller.save()
                return redirect('blog:detail' , id)
        else:
            form = Sellers()
    else:
        return redirect('account:login')

    return render(request , 'blog/seller-update.html' , {'form':form , 'addresses':addresses})

def color_num(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if blog.number > 0 :
            if request.method == 'POST' :
                form = ColorNumForm(request.POST)
                if form.is_valid():
                    num = form.cleaned_data['num']
                    color = form.cleaned_data['color']
                    size = form.cleaned_data['size']

                    color = Colors.objects.get_or_create(color = color)
                    size = Sizes.objects.get_or_create(size = size)
                    color = form.cleaned_data['color']
                    size = form.cleaned_data['size']
                    color = Colors.objects.get(color = color)
                    size = Sizes.objects.get(size = size)


                    colors = ColorNum.objects.create(blog = blog , seller = user , num = num ,
                    color = color , size = size)
                    seller = BlogSeller.objects.get(blog=blog , seller = user)
                    mycolor = ColorNum.objects/filter(seller = user , blog=blog).aggregate(Sum('num'))
                    mynum = mycolor + num
                    if mynum <= seller.number :
                        colors.save()
                        return redirect('blog:detail' , id)
            else:
                form = ColorNumForm()
        else:   
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'blog/create-num.html' , {'form':form})

def color_num_update(request , id):
    colors = ColorNum.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if request.method == 'POST' :
            form = ColorNumForm(request.POST)
            if form.is_valid():
                num = form.cleaned_data['num']
                mycolor = form.cleaned_data['color']
                mysize = form.cleaned_data['size']
                color = Colors.objects.get_or_create(color = mycolor)
                size = Sizes.objects.get_or_create(size = mysize)
                colors.num = num 
                colors.color = color
                colors.size = size
                seller = BlogSeller.objects.get(blog=blog , seller = user)
                mycolor = ColorNum.objects/filter(seller = user , blog=blog).aggregate(Sum('num'))
                mynum = mycolor + num - colors.num
                if mynum <= seller.number :
                    colors.save()
                    return redirect('blog:detail' , id)
        else:
            form = ColorNumForm()
    else:
        return redirect('account:login')

    return render(request , 'blog/update-num.html' , {'form':form , 'colors':colors})

def go_to_gateway_view(request):
    user = request.user
    order = Order.objects.get(user = user , current=True)
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = order.price
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = user.number  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('blog:callback_gateway'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e

def callback_gateway_view(request):
    user = request.user
    order = Order.objects.get(user = user , current=True)
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        order.received = True
        order.save()
        return redirect('blog:order_detail' , order.id)


    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")

def tag_list(request , id):
    tags = Tag.objects.get(id = id)
    blog = Blog.objects.filter(tags = tags , published = True)
    return render(request , 'blog/tag-list.html' , {'blog':blog})

def sellers_delete(request , id):
    seller = BlogSeller.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if request.method == 'POST' :
            seller.delete()
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'blog/seller-delete.html')

def color_num_delete(request , id):
    colors = ColorNum.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if request.method == 'POST' :    
            colors.delete()
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'blog/delete-num.html')

def brand_list(request , id):
    brand = Brand.objects.get(id = id)
    blog = Blog.objects.filter(brand = brand , published = True)
    return render(request , 'blog/brand-list.html' , {'blog':blog})
