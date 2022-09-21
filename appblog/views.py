from django.shortcuts import redirect , get_object_or_404  , render 
from .models import MyBlog , Nums
from .forms import CreateForm ,  SearchForm 
from django.contrib.postgres.search import TrigramSimilarity
from coment.forms import ComentsBlogForm
from coment.models import ComentsBlog
from django.core.paginator import Paginator
from django.db.models import Count , Max
from taggit.models import Tag 
from blog.models import Blog , Category
from django.contrib.auth.decorators import login_required

def home(request):
    blog = {}
    max_tag = Tag.objects.filter(myblog__nums__view__gt = 1000)
    max_view = MyBlog.objects.filter(nums__view__gt = 1000 , published = True)
    form = SearchForm()
    try :
        request.session['blogsearch']
    except :
        request.session['blogsearch'] = ''
    if 'search' in request.GET :
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            request.session['blogsearch'] = search
    if request.session['blogsearch'] :
        blog = MyBlog.objects.annotate(blogsearch=TrigramSimilarity('titel', request.session.get('search')),).filter(
        blogsearch__gt=0.3 , published = True).order_by('-blogsearch')
        page = Paginator(blog, 1)
        lists = request.GET.get('page' , 1)
        blog = page.get_page(lists)
    return render(request , 'appblog/index.html' , {'blog':blog ,
     'form':form , 'max_view':max_view , 'max_tag':max_tag})

@login_required(login_url='account:login')
def detail(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    num = Nums.objects.get(model=blog)
    tags = blog.tags.all()
    category = blog.category.all()
    tag = blog.tags.values_list('id' , flat = True)
    blogs = MyBlog.objects.filter(tags__in = tag , published = True).exclude(id = blog.id)
    appblogs = blogs.annotate(tags_count = Count('tags')).order_by('-tags_count')
    prodacts = Blog.objects.filter(tags__in = tag , published = True)
    app_prodacts = prodacts.annotate(tags_count = Count('tags')).order_by('-tags_count')
    user = request.user
    if user not in num.view.all() :
        num.view.add(user)
    if request.method == 'POST' :
        form = ComentsBlogForm(request.POST)
        if form.is_valid():
            titel = form.cleaned_data['titel']
            body = form.cleaned_data['body']
            text = ComentsBlog.objects.create(body = body , user = user ,
            appblog = blog , titel=titel  )
            text.save()
            return redirect('appblog:detail' , id)
    else:
        form = ComentsBlogForm()
    coments = ComentsBlog.objects.filter(appblog = blog , published = True)
    if blog.status == 's' and blog.published == True and user.is_special or user.is_superuser or user == blog.author :
        context = {'blog':blog ,'form':form , 'coments':coments , 'appblogs':appblogs ,
         'tags':tags , 'app_prodacts':app_prodacts , 'category':category}
    elif blog.status == 'n' and blog.published == True  or user == blog.author :
        context = {'blog':blog ,'form':form , 'coments':coments , 'appblogs':appblogs ,
         'tags':tags , 'app_prodacts':app_prodacts , 'category':category}
    elif blog.status == 'd' and user.is_staff or user.is_admin or user.is_superuser :
        context = {'blog':blog ,'form':form , 'coments':coments , 'appblogs':appblogs ,
         'tags':tags , 'app_prodacts':app_prodacts , 'category':category}
    else:
        return redirect('appblog:list')
    return render(request , 'appblog/detail.html' , context)

@login_required(login_url='account:login')
def create(request):
    user = request.user
    if user.is_seller == True :       
        if request.method == "POST" :
            form = CreateForm(request.POST , request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                blog = MyBlog.objects.create(
                        titel = cd['titel'] , body = cd['body'] ,
                        image = cd['image'] , music = cd['music'] , film = cd['film'] , author = user)
                blog.category.set(cd['category'])
                for tag in cd['tags'] :
                    blog.tags.add(tag)
                num = get_object_or_404(Nums , model=blog)
                num.save()
                blog.save()
                return redirect('appblog:detail' , blog.id)
        else:
            form = CreateForm()
    else:
        return redirect('appblog:list')
    return render(request , 'appblog/create.html' , {'form':form})    

@login_required(login_url='account:login')
def update(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    form = CreateForm(request.POST , request.FILES  , instance=blog)
    user = request.user
    if user.is_seller == True :
        if user == blog.author :
            if request.method == 'POST' :
                if form.is_valid():
                    form.save()
                    return redirect('appblog:detail' , id)
            else:
                form = CreateForm()
        else:
            return redirect('appblog:list')
    return render(request , 'appblog/update.html' , {'form':form})

@login_required(login_url='account:login')
def delete(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    user = request.user
    if user.is_seller == True :
        if user == blog.author :
            if request.method == 'POST' :
                blog.image.delete() 
                blog.delete()
                return redirect('appblog:list')
        else:
            return redirect('appblog:list')
    else:
        return redirect('appblog:list')
    return render(request , 'appblog/delete.html')

@login_required(login_url='account:login')
def like(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    user = request.user
    if user not in blog.likes.all() :
        blog.likes.add(user)
        return redirect( 'appblog:detail' , id)
    else :
        blog.likes.remove(user)
        return redirect( 'appblog:detail' , id)

@login_required(login_url='account:login') 
def saved(request , id):
    blog = get_object_or_404(MyBlog , id = id)
    user = request.user
    if user not in blog.saved.all() :
        blog.saved.add(user)
        return redirect( 'appblog:detail' , id)
    else:
        blog.saved.remove(user)
        return redirect( 'appblog:detail' , id)

def tag_list(request , id):
    tags = get_object_or_404(Tag , id = id)
    blog = MyBlog.objects.filter(tags = tags , published = True)
    return render(request , 'appblog/tag-list.html' , {'blog':blog})

def category_list(request , id):
    category = get_object_or_404(Category , id = id)
    blog = MyBlog.objects.filter(category = category , published = True)
    return render(request, 'blog/category-list.html' , {'blog':blog})
