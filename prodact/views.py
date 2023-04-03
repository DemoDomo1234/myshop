from django.shortcuts import redirect, render , get_object_or_404
from .models import Prodact
from base.models import *
from seller.models import ProdactSeller
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from .forms import *
from taggit.models import Tag 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .prodact import CRUDProdact


def home(request):
    blog = {}
    advertising = Advertising.objects.all()
    category_max = Category.objects.filter(blog_categorys__numes_prodact__num__gt=1000)
    num_max = Prodact.objects.filter(numes_prodact__gt=1000, published=True)
    brand_max = Brand.objects.filter(blog_brand__numes_prodact__num__gt=1000)
    myblog = ProdactSeller.objects.filter(discount__gt=30, published=True)
    try :
        request.session['search']
    except :
        request.session['search'] = ''
    if 'search' in request.GET :
        request.session['search'] = request.GET['search']
    if request.session['search'] :
        blog = Prodact.objects.annotate(blogsearch=TrigramSimilarity(
        'titel', request.session['search']),).filter(
        blogsearch__gt=0.3 , published = True).order_by('-blogsearch')
        page = Paginator(blog, 1)
        lists = request.GET.get('page' , 1)
        blog = page.get_page(lists)
    return render(request , 'prodact/index.html' , {'blog':blog , 
    'myblog':myblog , 'num_max':num_max , 'brand_max':brand_max ,
    'category_max':category_max ,'advertising':advertising})


@login_required(login_url='account:login')
def detail(request , id):
    prodact = CRUDProdact(request, id)
    prodact.detail_prodact()


@login_required(login_url='account:login')
def create(request):
    prodact = CRUDProdact(request)
    prodact.create_prodact()


@login_required(login_url='account:login')
def update(request, id):
    prodact = CRUDProdact(request, id)
    prodact.update_prodact()


@login_required(login_url='account:login')
def delete(request, id):
    prodact = CRUDProdact(request, id)
    prodact.detail_prodact()




@login_required(login_url='account:login')
def like(request, id):
    blog = get_object_or_404(Prodact, id=id)
    user = request.user
    if user not in blog.like.all():
        blog.like.add(user)
        return redirect( 'prodact:detail', id)
    else:
        blog.like.remove(user)
        return redirect( 'prodact:detail', id)


def send_email(request):
    if request.method == "POST":
        form = SendEmail(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            massages = f'''
                        name : {cd['name']}
                        subject : {cd['massage']}
                        message : {cd['subject']}
                       '''
            send_mail('message', massages, 'demodomone@gmail.com', [cd['email']],
            fail_silently=False, auth_password='moxczeohuhgyowqm')  
            return redirect('prodact:list')
    form = SendEmail()
    return render(request, 'prodact/sendmail.html', {'form':form})


def share_post(request, id):
    blog = get_object_or_404(Prodact, id=id)
    if request.method == "POST":
        form = Share(request.POST)
        if form.is_valid():
            url = request.build_absolute_uri(blog.get_absolute_url())
            email = form.cleaned_data['email'] 
            send_mail(blog.titel, url, 'demodomone@gmail.com', [email],
            fail_silently=False, auth_password='moxczeohuhgyowqm')
            return redirect('prodact:detail', id)
    form = Share()
    return render(request, 'prodact/share.html', {'form':form})


def tag_list(request , id):
    tags = get_object_or_404(Tag, id=id)
    blog = Prodact.objects.filter(tags=tags, published=True)
    return render(request, 'prodact/tag-list.html', {'blog':blog})


def brand_list(request, id):
    brand = get_object_or_404(Brand, id=id)
    blog = Prodact.objects.filter(brand=brand, published=True)
    return render(request, 'prodact/brand-list.html', {'blog':blog})

