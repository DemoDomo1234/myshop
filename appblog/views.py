from django.shortcuts import redirect , render , get_object_or_404 
from .models import MyBlog , Nums
from .forms import CreateForm ,  SearchForm 
from django.contrib.postgres.search import TrigramSimilarity
from coment.forms import ComentsBlogForm
from coment.models import ComentsBlog
from django.core.paginator import Paginator
from django.db.models import Count , Max
from taggit.models import Tag 
from blog.models import Images

def home(request):
    blog = MyBlog.objects.all()
    max_view = MyBlog.objects.filter(nums__gt = 1000)
    form = SearchForm()
    if 'search' in request.GET :
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            blog = blog.annotate(blogsearch=TrigramSimilarity('titel', search),).filter(
            blogsearch__gt=0.3).order_by('-blogsearch')
    page = Paginator(blog, 15)
    lists = request.GET.get('page' , 1)
    blog = page.get_page(lists)
    return render(request , 'appblog/index.html' , {'blog':blog ,
     'form':form , 'max_view':max_view})

def detail(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    images = Images.objects.filter(myblog = blog)
    num = Nums.objects.get(model=blog)
    num.num += 1
    num.save()
    tag = blog.tags.values_list('id' , flat = True)
    blogs = MyBlog.objects.filter(tags__in = tag).exclude(id = blog.id)
    appblogs = blogs.annotate(tags_count = Count('tags')).order_by('-tags_count')
    user = request.user
    if user.is_authenticated :
        if request.method == 'POST' :
            form = ComentsBlogForm(request.POST)
            if form.is_valid():
                titel = form.cleaned_data['titel']
                body = form.cleaned_data['body']
                text = ComentsBlog.objects.create(body = body , user = user ,
                appblog = blog , titel=titel  )
                text.save()
        else:
            form = ComentsBlogForm()
    coments = ComentsBlog.objects.filter(appblog = blog)
    return render(request , 'appblog/detail.html' , {'blog':blog ,
    'form':form , 'coments':coments , 'appblogs':appblogs , 'images':images})

def create(request):
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :       
            if request.method == "POST" :
                form = CreateForm(request.POST , request.FILES)
                if form.is_valid():
                        tags = form.cleaned_data['tags']
                        titel = form.cleaned_data['titel']
                        body = form.cleaned_data['body']
                        image = form.cleaned_data['image']
                        music = form.cleaned_data['music']
                        film = form.cleaned_data['film']
                        category = form.cleaned_data['category']
                        author = user
                        blog = MyBlog.objects.create(
                            titel = titel , body = body ,
                            image = image , music = music , film = film , author = author,)
                        blog.category.set(category)
                        blog.save()
                        num = Nums.objects.create(model=blog , num=0)
                        num.save()
                        return redirect('appblog:list')
                        for tag in tags :
                            blog.tags.add(tag)
            else:
                form = CreateForm()

    return render(request , 'appblog/create.html' , {'form':form})    

def update(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    form = CreateForm(request.POST or None , request.FILES or None , instance=blog)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == blog.author :
                if request.method == 'POST' :
                    if form.is_valid():
                        form.save()
                        return redirect('appblog:list')

                        for tag in form.cleaned_data['tags'] :
                            blog.tags.add(tag)
                else:
                    form = CreateForm()
    return render(request , 'appblog/update.html' , {'form':form})

def delete(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == blog.author :
                if request.method == 'POST' :
                    blog.image.delete() 
                    blog.delete()
    return render(request , 'appblog/delete.html')

def like(request , id):
    blog = MyBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in blog.likes.all() :
            blog.likes.add(user)
    return redirect( 'appblog:detail' , id)

def unlike(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    user = request.user
    if user.is_authenticated :
        if user in blog.likes.all() :
            blog.likes.remove(user)
    return redirect( 'appblog:detail' , id)

def likes(request):
    blog = MyBlog.objects.filter(likes = request.user)
    return render(request , 'appblog/likes.html' , {'blog' : blog })

def saved(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    user = request.user
    if user.is_authenticated :
        if user not in blog.saved.all() :
            blog.saved.add(user)
    return redirect( 'appblog:detail' , id)

def unsaved(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    user = request.user
    if user.is_authenticated :
        if user  in blog.saved.all() :
            blog.saved.remove(user)
    return redirect( 'appblog:detail' , id)

def saveds(request):
    blog = MyBlog.objects.filter(saved = request.user)
    return render(request , 'appblog/saveds.html' , {'blog' : blog })
