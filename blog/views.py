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
from django.contrib.gis.db.models.functions import Distance
from .models import ColorNum
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from taggit.models import Tag 
from django.core.paginator import Paginator

def home(request):
    blog = {}
    advertising = Advertising.objects.all()
    category_max = Category.objects.filter(blog_categorys__numes_myblog__num__gt = 1000)
    num_max = Blog.objects.filter(numes_myblog__num__gt = 1000 , published = True)
    brand_max = Brand.objects.filter(blog_brand__numes_myblog__num__gt = 1000)
    myblog = BlogSeller.objects.filter(discount__gt = 30 , published = True)
    try :
        request.session['search']
    except :
        request.session['search'] = ''
    if 'search' in request.GET :
        request.session['search'] = request.GET['search']
    if request.session['search'] :
        blog = Blog.objects.annotate(blogsearch=TrigramSimilarity(
        'titel', request.session['search']),).filter(
        blogsearch__gt=0.3 , published = True).order_by('-blogsearch')
        page = Paginator(blog, 1)
        lists = request.GET.get('page' , 1)
        blog = page.get_page(lists)
    return render(request , 'blog/index.html' , {'blog':blog , 
    'myblog':myblog , 'num_max':num_max , 'brand_max':brand_max ,
    'category_max':category_max ,'advertising':advertising})

def detail(request , id):
    user = request.user
    blog = Blog.objects.get(id = id)
    coments = Coments.objects.filter(blog = blog , published = True )
    custion = Custion.objects.filter(model = blog , published = True , one_respones = None , tow_respones = None)
    images = Images.objects.filter(blog = blog)
    nums = Nums.objects.get(blog = blog)
    category = blog.category.all()
    tags = blog.tags.all()
    tag = blog.tags.values_list('id' , flat = True)
    blogs = Blog.objects.filter(tags__in = tag , published = True).exclude(id = blog.id)
    myblogs = blogs.annotate(tags_count = Count('tags')).order_by('-tags_count')
    if user.is_authenticated :
        lists = List.objects.filter(user=user).exclude(list = blog)
        if request.method == 'POST' :
            form = ComentsForm(request.POST , request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                text = Coments.objects.create(body=cd['body'], user=user,
                        blog=blog, image=cd['image'], titel=cd['titel'], bad=cd['bad'],
                        good=cd['good'], sagestion=cd['sagestion'], score=cd['score'])
                text.save()
                return redirect('blog:detail' , blog.id)        
        else:
            form = ComentsForm()
    else:
        return redirect('account:login')
    return render(request , 'blog/detail.html' , {'blog':blog , 'form':form , 
    'coments':coments , 'lists':lists , 'images':images ,'category':category ,
    'myblogs':myblogs ,'custion':custion , 'tags':tags , 'nums':nums})

def create(request):
    user = request.user
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
                    cd = form.cleaned_data
                    brand_name = request.POST['brand']
                    brand = Brand.objects.get(brand = brand_name)
                    blog = Blog.objects.create(
                            titel = cd['titel'] , body = cd['body'] ,
                            image = cd['image'] , seller = user ,
                            brand = brand , size=cd['size'] ,
                            weigth=cd['weigth'] , garanty = cd['garanty'])
                    for tag in cd['tags'] :
                            blog.tags.add(tag)
                    for cate in request.POST.getlist('category'):
                        category = Category.objects.get(titel = cate)
                        if category not in blog.category.all():
                            blog.category.add(category)
                    try :
                        for mycolor in request.POST.getlist('color'):
                            color = Colors.objects.get(color = mycolor)
                            if color not in blog.color.all():
                                blog.color.add(color)
                    except :
                        for mysize in request.POST.getlist('size'):
                            size = Sizes.objects.get(size = mysize)
                            if size not in blog.sizes.all():
                                blog.sizes.add(size)
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

    return render(request , 'blog/create.html' , {'form':form ,  
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
    mysize = blog.sizes.all()
    id1 = mysize.values_list('id' , flat=True)
    sizes = Sizes.objects.filter(id__gte = 0).exclude(id__in = id1)

    if 'search' in request.GET :
        search = request.GET['search']
        category = categorys.annotate(categorysearch=TrigramSimilarity(
        'titel', search),).filter(
        categorysearch__gt=0.3).order_by('-categorysearch')
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == blog.seller :
                if request.method == 'POST' :
                    form = UpdateForm(request.POST , request.FILES)
                    if form.is_valid():
                        cd = form.cleaned_data
                        mybrand = request.POST['brand']
                        blog.titel = cd['titel']
                        blog.body = cd['body']
                        blog.image = cd['image']
                        blog.garanty = cd['garanty']

                        blog.seller = user
                        blog.time = blog.time
                        blog.brand = Brand.objects.get(brand = mybrand)
                        for tag in cd['tags'] :
                            blog.tags.add(tag)

                        for cate in request.POST.getlist('category'):
                            category = Category.objects.get(titel = cate)
                            if category not in blog.category.all():
                                blog.category.add(category)

                        for cate in request.POST.getlist('categorys'):
                            category = Category.objects.get(titel= cate)
                            if category in blog.category.all():
                                blog.category.remove(category)
                    try:
                        for mycolor in request.POST.getlist('color'):
                            color = Colors.objects.get(color = mycolor)
                            if color not in blog.color.all():

                                blog.color.add(color)
                    except :
                        for mysize in request.POST.getlist('size'):
                            size = Sizes.objects.get(size = mysize)
                            if size not in blog.size.all():

                                blog.size.add(size)
                    try :
                        for mycolor in request.POST.getlist('colors'):
                            color = Colors.objects.get(color = mycolor)
                            if color in blog.color.all():

                                blog.color.remove(color)
                    except :
                        for mysize in request.POST.getlist('sizes'):
                            size = Sizes.objects.get(size = mysize)
                            if size in blog.size.all():

                                blog.size.remove(size)

                    blog.save()
                    return redirect('blog:detail' , blog.id)
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
        if payment == 'cash' :
            order.online = False
        for item in item:
            blog = BlogSeller.objects.get(blog = item[a].blog , seller__id = item[a].seller.id)
            try :
                color = ColorNum.objects.get(blog=item[a].seller.blog , color = item[a].color , seller = item[a].seller)
            except :
                color = ColorNum.objects.get(blog=item[a].seller.blog , size = item[a].size , seller = item[a].seller)

            send = (blog.blog.size * 10 ) + (blog.blog.weigth * 5 ) * int(i)
            map = Distance(blog.address.location , order.address.location)
            send += map
            send *= 5000
            if user.is_special :
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
    return render(request , 'blog/order.html' , {'item' : item ,
    'address':addresses })

def shop(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if request.method == 'POST' :
            order = Order.objects.get(user = user , current=True)
            num = request.POST['num']
            seller = request.POST['seller']
            try:
                size = request.POST['size']
                nums = Nums.objects.get(blog=blog)
                nums.num += int(num)
                nums.save()
                myseller = BlogSeller.objects.get(id = seller)
                mysize = Sizes.objects.get(size = size)
                item = OrderItem.objects.create(blog=blog , num=num , order=order ,
                size=mysize , seller=myseller ,user=user)
                item.save()
                color = ColorNum.objects.get(blog=blog , size=mysize , seller = myseller)
                color.num -= int(num)
                color.nums += int(num)
                color.save()
            except:
                color = request.POST['color']
                mycolor = Colors.objects.get(color = color)
                nums = Nums.objects.get(blog=blog)
                nums.num += int(num)
                nums.save()
                myseller = BlogSeller.objects.get(id = seller)
                item = OrderItem.objects.create(blog=blog , num=num , order=order ,
                color=mycolor , seller=myseller)
                item.save()
                color = ColorNum.objects.get(blog=blog , color=mycolor)
                color.num -= int(num)
                color.nums += int(num)
                color.save()
                myseller.number -= int(num)
                myseller.save() 
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
        if user == item.user :
            seler = BlogSeller.objects.get(seller = user)
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
    else:
        return redirect('account:login')

def send_email(request):
    if request.method == "POST" :
        form = SendEmail(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            massages = '''
                        name : {0}
                        subject : {1}
                        message : {2}
                       '''.format(cd['name'] , cd['massage'] , cd['subject'])
            send_mail('message' , massages , 'demodomone@gmail.com' , [cd['email']] ,
            fail_silently=False , auth_password='moxczeohuhgyowqm')  
            return redirect('blog:list')
    form = SendEmail()
    return render(request , 'blog/sendmail.html' , {'form':form})

def create_list(request):
    user=request.user
    if user.is_authenticated :
        if request.method == 'POST':
            form = ListForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                lists = List.objects.create(titel=cd['titel'] ,
                user=user , body = cd['body'])
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
                    cd = form.cleaned_data
                    lists.titel = cd['titel']
                    lists.body = cd['body']
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
    user = request.user
    if user.is_authenticated :  
        if user == lists.user :
            blog = Blog.objects.filter(lists=lists)
            return render(request, 'blog/detaillist.html' , {'blog':blog , 'lists':lists})
        else :
            return redirect('blog:list')
    else :
        return redirect('blog:list')

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

def unlist_view(request , id):
    blog = Blog.objects.get(id = id)
    user=request.user
    if user.is_authenticated :  
        if request.method == 'POST':
            titel = request.POST.getlist('titel')
            for i in titel :
                titels = List.objects.get(titel=i)
                if titels in blog.lists.all() :
                    blog.lists.remove(titels)
                    return redirect('blog:detail' , id)
    else:
        return redirect('account:login')

def notifications(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in blog.notifications.all() :
            blog.notifications.add(user)
            return redirect( 'blog:detail' , id)
        else:
            blog.notifications.remove(user)
            return redirect( 'blog:detail' , id)
    return redirect('account:login')

def share_post(request , id):
    blog = Blog.objects.get(id = id)
    if request.method == "POST" :
        form = Share(request.POST)
        if form.is_valid():
            url = request.build_absolute_uri(blog.get_absolute_url())
            email = form.cleaned_data['email'] 
            send_mail(blog.titel , url , 'demodomone@gmail.com' , [email] ,
            fail_silently=False , auth_password='moxczeohuhgyowqm')  
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
                cd = form.cleaned_data
                address = Address.objects.create(user=user , 
                location=location , floor=cd['floor'] , plaque=cd['plaque'] , name=cd['name'] ,
                number=cd['number'] , postal_code=cd['postal_code'])
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
                    cd = form.cleaned_data
                    address.floor = cd['floor']
                    address.plaque = cd['plaque']
                    address.name = cd['name']
                    address.number = cd['number']
                    address.postal_code = cd['postal_code']
                    address.location=Point(long,lat,srid=4326) 
                    address.save()
                    return redirect('blog:list')

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
            if user == images.blog.seller :
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
            if user == images.blog.seller :
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
                cd = form.cleaned_data
                myaddress = request.POST['address']
                address = Address.objects.get(user=user , name = myaddress)
                seller = BlogSeller.objects.create(blog = blog , seller = user , address = address , 
                number = cd['number'] , price = cd['price'] , discount = cd['discount'])
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
        if user == seller.seller :
            if request.method == 'POST' :
                form = Sellers(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    myaddress = request.POST['address']
                    address = Address.objects.get(user=user , name = myaddress)
                    seller.price = cd['price']
                    seller.number = cd['number']
                    seller.discount = cd['discount']
                    seller.save()
                    return redirect('blog:detail' , seller.blogid)
            else:
                form = Sellers()
        else :
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'blog/seller-update.html' , {'form':form , 'addresses':addresses})

def color_num(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if request.method == 'POST' :
            form = ColorNumForm(request.POST , blog=blog)
            seller = BlogSeller.objects.get(blog=blog , seller = user)
            if form.is_valid():
                num = form.cleaned_data['num']
                price = form.cleaned_data['price']
                try :
                    color = form.cleaned_data['color']
                    color = Colors.objects.get(color = color)
                    colors = ColorNum.objects.create(blog = blog , seller = seller , num = num ,
                    color = color , price=price)
                except :
                    size = form.cleaned_data['size']
                    size = Sizes.objects.get(size = size)
                    colors = ColorNum.objects.create(blog = blog , seller = user , num = num ,
                    size = size , price=price)
                mycolor = ColorNum.objects.filter(seller = seller , blog=blog).aggregate(Sum('num'))
                if mycolor['num__sum'] == None :
                    mycolor['num__sum'] = 0
                mynum = mycolor['num__sum'] + int(num)
                if mynum <= seller.number :
                    colors.save()
                    return redirect('blog:detail' , id)
        else:
            form = ColorNumForm(blog=blog)
    else:
        return redirect('account:login')

    return render(request , 'blog/create-num.html' , {'form':form})

def color_num_update(request , id):
    colors = ColorNum.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        seller = BlogSeller.objects.get(blog=colors.blog , seller = user)
        if seller == colors.seller :
            if request.method == 'POST' :
                form = ColorNumForm(request.POST , blog=colors.blog)
                if form.is_valid():
                    num = form.cleaned_data['num']
                    price = form.cleaned_data['price']
                    try :
                        color = form.cleaned_data['color']
                        color = Colors.objects.get(color = color)
                        colors.color = color
                        colors.size = None
                    except :
                        size = form.cleaned_data['size']
                        size = Sizes.objects.get(size = size)
                        colors.size = size
                        colors.color = None
                    colors.num = num 
                    colors.price = price
                    mycolor = ColorNum.objects.filter(seller = seller , blog=colors.blog).aggregate(Sum('num'))
                    if mycolor['num__sum'] == None :
                        mycolor['num__sum'] = 0
                    mynum = mycolor['num__sum'] + int(num) - colors.num
                    if mynum <= seller.number :
                        colors.save()
                    return redirect('blog:detail' , colors.blog.id)
            else:
                form = ColorNumForm(blog=colors.blog)
        else :
            return redirect('blog:list')

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
        if user == seller.seller :
            if request.method == 'POST' :
                seller.delete()
                return redirect('blog:list')
        else :
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'blog/seller-delete.html')

def color_num_delete(request , id):
    colors = ColorNum.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        seller = BlogSeller.objects.get(blog=colors.blog , seller = user)
        if seller == colors.seller :
            if request.method == 'POST' :    
                colors.delete()
                return redirect('blog:detail' , colors.blog.id)
        else :
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'blog/delete-num.html')

def brand_list(request , id):
    brand = Brand.objects.get(id = id)
    blog = Blog.objects.filter(brand = brand , published = True)
    return render(request , 'blog/brand-list.html' , {'blog':blog})

def item_update(request , id):
    item = OrderItem.objects.get(id = id)
    blog = BlogSeller.objects.get(blog = item.blog , seller__id = item.seller.id)
    try :
        color = ColorNum.objects.get(blog=item.seller.blog , color = item.color , seller = item.seller)
    except :
        color = ColorNum.objects.get(blog=item.seller.blog , size = item.size , seller = item.seller)
    if request.method == 'POST' :
        if request.user.is_authenticated :
            if request.user == item.user : 
                num = request.POST['num']
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
            return redirect('account:login')
    else:
        return render(request , 'blog/update-item.html' , {'item':item})

def select_seller(request):
    if request.method == 'POST':
        id = request.POST['id']
        blog = Blog.objects.get(id=id)
        try:
            mycolor = request.POST['color']
            color = Colors.objects.get(color=mycolor)
            colors = ColorNum.objects.filter(blog = blog , published = True , color=color)
        except:
            mysize = request.POST['size']
            size = Sizes.objects.get(size=mysize)
            colors = ColorNum.objects.filter(blog = blog , published = True , siez=size)
    return render(request , 'blog/seller-select.html' , {'colors':colors})

def inter_num(request):
    if request.method == 'POST' :
        id = request.POST['id']
        color = ColorNum.objects.get(id=id)
    return render(request , 'blog/inter-num.html' , {'color':color})
