from django.shortcuts import redirect , render , HttpResponse
from .models import *
from django.contrib.postgres.search import TrigramSimilarity
from coment.forms import ComentsForm
from coment.models import Coments
from django.core.mail import send_mail
from account.models import User
from django.contrib.gis.geos import Point
from .forms import *
from django.db.models import Max , Min 
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from .func import timer

def home(request):
    blog = Blog.objects.all()
    num_max = Blog.objects.filter(nums__gt = 1000)
    myblog = Blog.objects.filter(discount__gt = 0)
    category = Category.objects.all()
    if 'search' in request.GET :
        search = request.GET['search']
        blog = blog.annotate(blogsearch=TrigramSimilarity(
        'titel', search),).filter(
        blogsearch__gt=0.3).order_by('-blogsearch')
    return render(request , 'blog/index.html' , {'blog':blog , 
    'myblog':myblog , 'category':category , 'num_max':num_max})

def detail(request , id):
    blog = Blog.objects.get(id = id)
    images = Images.objects.filter(blog = blog)
    size = blog.size.all()
    color = blog.color.all()
    category = blog.category.all()
    user = request.user
    if user.is_authenticated :
        if request.method == 'POST' :
            form = ComentsForm(request.POST , request.FILES)
            if form.is_valid() :
                titel = form.cleaned_data['titel']
                body = form.cleaned_data['body']
                bad = form.cleaned_data['bad']
                good = form.cleaned_data['good']
                image = form.cleaned_data['image']
                sagestion = form.cleaned_data['sagestion']
                score = form.cleaned_data['score']

                text = Coments.objects.create(body = body , user = user ,
                blog = blog , image = image , titel=titel , bad=bad ,
                good=good , sagestion=sagestion , score=score )
                text.save()
        else:
            form = ComentsForm()
    coments = Coments.objects.filter(blog = blog)
    return render(request , 'blog/detail.html' , {'blog':blog , 'form':form ,
    'coments':coments , 'images':images , 'color':color , 'size':size ,
    'category':category})

def create(request):
    colors = Colors.objects.all()
    sizes = Sizes.objects.all()
    category = Category.objects.all()
    if 'search' in request.GET :
        search = request.GET['search']
        category = category.annotate(categorysearch=TrigramSimilarity(
        'titel', search),).filter(
        categorysearch__gt=0.3).order_by('-categorysearch')
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :       
            if request.method == "POST" :
                form = CreateForm(request.POST , request.FILES)
                if form.is_valid():

                    titel = form.cleaned_data['titel']
                    body = form.cleaned_data['body']
                    image = form.cleaned_data['image']
                    price = form.cleaned_data['price']
                    discount = form.cleaned_data['discount']
                    number = form.cleaned_data['number']
                    seller = user

                    blog = Blog.objects.create(
                            titel = titel , body = body ,
                            image = image , number = number ,
                            price = price , seller = seller ,
                            discount = discount)

                    for color in request.POST.getlist('color'):
                        
                        color = Colors.objects.get(color= color)
                        if color not in blog.color.all():

                            blog.color.add(color)
                            
                    
                    for size in request.POST.getlist('size'):
                        
                        size = Sizes.objects.get(size = size)
                        if size not in blog.size.all():
                            blog.size.add(size)
                    
                    
                    for cate in request.POST.getlist('category'):
                        category = Category.objects.get(titel = cate)
                        if category not in blog.category.all():

                            blog.category.add(category)

                    blog.save()
                    return redirect('blog:list')
            else:
                form = CreateForm()
    return render(request , 'blog/create.html' , {'form':form , 'sizes':sizes
    , 'colors':colors , 'category':category})    

def update(request , id):
    blog = Blog.objects.get(id = id)
    mycolors = blog.color.all()
    mysizes = blog.size.all()
    mycategory = blog.category.all()
    id1 = mycolors.values_list('id' , flat=True)
    id2 = mysizes.values_list('id' , flat=True)
    id3 = mycategory.values_list('id' , flat=True)
    colors = Colors.objects.filter(id__gte = 0).exclude(id__in = id1)
    sizes = Sizes.objects.filter(id__gte = 0).exclude(id__in = id2)
    categorys = Category.objects.filter(id__gte = 0).exclude(id__in = id3)
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
                        blog.titel = titel
                        blog.body = body
                        blog.image = image
                        blog.price = price
                        blog.seller = user
                        blog.time = blog.time
                        blog.discount = discount
                        blog.number = number
                        for i in request.POST.getlist('color'):
                            color = Colors.objects.get(color = i)
                            if color not in blog.color.all():
                                blog.color.add(color)
                            
                    
                        for x in request.POST.getlist('size'):
                            size = Sizes.objects.get(size = x)
                            if size not in blog.size.all():
                                blog.size.add(size)

                        for i in request.POST.getlist('colors'):
                            color = Colors.objects.get(color= i)
                            if color in blog.color.all():
                                blog.color.remove(color)
                            
                        for x in request.POST.getlist('sizes'):
                            size = Sizes.objects.get(size = x)
                            if size  in blog.size.all():
                                blog.size.remove(size)

                        for x in request.POST.getlist('category'):
                            category = Category.objects.get(titel = x)
                            if category not in blog.category.all():
                                blog.category.add(category)

                        for i in request.POST.getlist('categorys'):
                            category = Category.objects.get(titel= i)
                            if category in blog.category.all():
                                blog.category.remove(category)
 
                        blog.save()
                        return redirect('blog:list')
                else:
                    form = UpdateForm()
    return render(request , 'blog/update.html' , {'form':form ,
    'sizes':sizes , 'colors':colors , 'mysizes':mysizes , 'mycolors':mycolors ,
    'mycategory':mycategory , 'categorys':categorys})
    
def delete(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == blog.seller :
                if request.method == 'POST' :   
                    blog.image.delete()
                    blog.delete()
                    return redirect('blog:list')
    return render(request , 'blog/delete.html')

def like(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in blog.like.all() :
            blog.like.add(user)
    return redirect( 'blog:detail' , id)

def unlike(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in blog.like.all() :
            blog.like.remove(user)
    return redirect( 'blog:detail' , id)

def cart(request):
    order = Order.objects.get(user = request.user , current=True)
    a = 0
    user = request.user
    numbers = [1 , 2 , 3 , 4 , 5 , 6 , 7]
    address = Address.objects.filter(user =user)
    item = OrderItem.objects.filter(blog=blog[a])
    blog = Blog.objects.filter(cart = user)
    if request.method == 'POST' :
        address = request.POST['ddress']
        order.address = address
        order.save()
        form = Num(request.POST)
        if form.is_valid():
            for i in request.POST.getlist('num'):
                myblog = Blog.objects.get(id = blog[a].id)
                nums = int(i[0]) - item[a].num
                if nums > 0 :
                    myblog.number -= nums
                else:
                    myblog.number += nums
                myblog.save()
                item[a].num = i[0]
                item.save()
                num = Num.objects.get(model=blog[a])
                num.num = item[a].num
                num.save()
                a += 1
            for cart in blog :
                cart.cart.remove(user)
    form = Num()
    return render(request , 'blog/cart.html' , {'blog' : blog , 'form':form , 'address':address , 'numbers':numbers})

def shop(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if blog.number > 0 :
        if user not in blog.cart.all() :
            if request.method == 'POST' :
                try:
                    orders = Order.objects.get(user = user , current=True)
                except:
                    orders = Order.objects.create(user=user)
                    orders.save()
                order = Order.objects.get(user = user , current=True)
                color = request.POST['color']
                size = request.POST['size ']
                form = Num(request.POST)
                if form.is_valid():
                    num = form.cleaned_data['num']
                    nums = Num.objects.create(num=num , model=blog)
                    item = OrderItem.objects.create(blog=blog , num=num , order=order ,
                    color=color , size=size)
                    item.save()
                    blog.number -= num
                    blog.save()
                    blog.cart.add(user)

                form = Num()
            return redirect('blog:detail' , id)
    return redirect('blog:list')

def unshop(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user in blog.cart.all():
        blog.cart.remove(user)
        item = OrderItem.objects.get(blog=blog , order__user=user)
        blog.number += item.num 
        blog.save()
        item.delete()
        return redirect('blog:detail' , id)

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
            fail_silently=False)  
    form = SendEmail()
    return render(request , 'blog/sendmail.html' , {'form':form})

def create_list(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            titel = form.cleaned_data['titel']
            body = form.cleaned_data['body']
            lists = List.objects.create(titel=titel ,
            user=request.user , body = body)
            lists.save()
    form = ListForm()
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
    form = ListForm()
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
    return render(request , 'blog/deletelist.html')

def list_view(request , id):
    listes = List.objects.filter(user = request.user)
    if request.method == 'POST':
        titel = request.POST.getlist('titel')
        for i in titel :
            print(i)
            titels = List.objects.get(titel=i)
            blog = Blog.objects.get(id = id)
            if titels not in blog.lists.all() :
                blog.lists.add(titels)
    return render(request, 'blog/list.html' , {'listes':listes})

def unlist_view(request , id):
    blog = Blog.objects.get(id = id)
    listes = blog.lists.filter(user=request.user)
    if request.method == 'POST':
        titel = request.POST.getlist('titel')
        for i in titel :
            titels = List.objects.get(titel=i)
            if titels in blog.lists.all() :
                blog.lists.remove(titels)
    return render(request, 'blog/unlist.html' , { 'listes':listes})

def notifications(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in blog.notifications.all() :
            blog.notifications.add(user)
    return redirect( 'blog:detail' , id)

def un_notifications(request , id):
    blog = Blog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in blog.notifications.all() :
            blog.notifications.remove(user)
    return redirect( 'blog:detail' , id)

def share_post(request , id):
    blog = Blog.objects.get(id = id)
    if request.method == "POST" :
        form = Share(request.POST)
        if form.is_valid():
            url = request.build_absolute_uri(blog.get_absolute_url())
            email = form.cleaned_data['email'] 
            send_mail(blog.titel , url , 'demodomone@gmail.com' , [email] ,
            fail_silently=False)  
    form = Share()
    return render(request , 'blog/share.html' , {'form':form})

def add_address(request):
        user = request.user
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
                print(request.POST)
        form = AddressForm()
 
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
    form = UpdateAddressForm() 
    return render(request,'blog/updateaddress.html' , {'form':form})

def delete_address(request , id):
    user = request.user
    address = Address.objects.get(id = id)
    if user.is_authenticated : 
        if user == address.user :
            if request.method =='POST':
                address.delete()
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
    return render(request , 'blog/update-image.html' , {'form':form , 'images':images})

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
    return render(request , 'blog/delete-image.html')

def create_category(request):
    form = CreateCategory()
    if request.method == "POST":
        form = CreateCategory(request.POST)
        titel = form.cleaned_data['titel']
        more = form.cleaned_data['more']
        category = Category.objects.create(titel=titel , more=more)
        category.save()
        return redirect('blog:create')
    return render(request, 'blog/createcategory.html' , {'form':form})

def category_list(request , id):
    category = Category.objects.get(id = id)
    blog = Blog.objects.filter(category = category)
    return render(request, 'blog/category-list.html' , {'blog':blog})

def order_pdf(request , id):
    pdf = HttpResponse(content_type='application/pdf')
    pdf["ontent-Dispoxiyions"] = 'attachment;filename=order' +  str(request.user.username)+str(datetime.datetime.now())+'.pdf'
    html_url  = "blog/pdf.html"
    html = get_template(html_url)
    order = Order.objects.get(id = id)
    text = {'order':order}
    my_html = html.render(text)
    pisa.CreatePDF(my_html , dest=pdf)
    return pdf

def create_image_myblog(request , id):
    blog = MyBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :  
            if blog.seller == user :     
                if request.method == "POST" :
                    form = ImageForm(request.POST , request.FILES)
                    if form.is_valid():
                        image = form.cleaned_data['image']
                        images = Images.objects.create(
                            image = image , myblog = blog)
                        images.save()
                        return redirect('blog:list')
                else:
                    form = ImageForm()
    return render(request , 'blog/create-image-myblog.html' , {'form':form})    

def order_detail(request , id):
    order = Order.objects.get(id = id)
    item = OrderItem.objects.filter(order = order)
    return render(request , 'blog/order-detail.htnl' , {'order':order , 'item':item})