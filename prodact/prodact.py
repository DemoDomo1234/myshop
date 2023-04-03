from django.shortcuts import redirect, render , get_object_or_404
from .models import Prodact, Nums
from base.models import *
from seller.models import ProdactSeller
from django.contrib.postgres.search import TrigramSimilarity
from coment.forms import ComentsForm
from coment.models import Coments , Custion
from .forms import *
from django.db.models import Count, Min




class CRUDProdact :
    

    def __init__(self, request, id=None):
        self.request = request
        self.user = request.user
        self.id = id


    def create_prodact(self):
        brands = Brand.objects.all()
        category = Category.objects.all()
        sizes = Sizes.objects.all()
        colors = Colors.objects.all()
        if 'search' in self.request.GET :
            search = self.request.GET['search']
            category = category.annotate(categorysearch=TrigramSimilarity(
            'titel', search),).filter(
            categorysearch__gt=0.3).order_by('-categorysearch')
        if self.user.is_seller :       
            if self.request.method == "POST" :
                form = CreateForm(self.request.POST , self.request.FILES)
                if form.is_valid():
                    cd = form.cleaned_data
                    brand_name = self.request.POST['brand']
                    brand = Brand.objects.get(brand = brand_name)
                    blog = Prodact.objects.create(
                            titel = cd['titel'] , body = cd['body'] ,
                            image = cd['image'] , seller = self.user ,
                            brand = brand , size=cd['size'] ,
                            weigth=cd['weigth'] , garanty = cd['garanty'])
                    for tag in cd['tags'] :
                            blog.tags.add(tag)
                    for cate in self.request.POST.getlist('category'):
                        category = Category.objects.get(titel=cate)
                        if category not in blog.category.all():
                            blog.category.add(category)
                    try :
                        for mycolor in self.request.POST.getlist('color'):
                            color = Colors.objects.get(color=mycolor)
                            if color not in blog.color.all():
                                blog.color.add(color)
                    except :
                        for mysize in self.request.POST.getlist('size'):
                            size = Sizes.objects.get(size=mysize)
                            if size not in blog.sizes.all():
                                blog.sizes.add(size)
                    blog.save()
                    nums = Nums.objects.create(blog=blog, num=0)
                    nums.save()
                    return redirect('blog:detail', blog.id)
            else:
                form = CreateForm()
        else:
            return redirect('blog:list')
        context = {'form':form, 'brands':brands,
                        'category':category, 'sizes':sizes,
                        'colors':colors}
        return render(self.request, 'prodact/create.html', context)    


    def update_prodact(self):
        blog = get_object_or_404(Prodact , id=self.id)
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
        if 'search' in self.request.GET :
            search = self.request.GET['search']
            category = categorys.annotate(categorysearch=TrigramSimilarity(
            'titel', search),).filter(
            categorysearch__gt=0.3).order_by('-categorysearch')
        if self.user.is_seller == True :
            if self.user == blog.seller :
                if self.request.method == 'POST' :
                    form = UpdateForm(self.request.POST , self.request.FILES)
                    if form.is_valid():
                        cd = form.cleaned_data
                        mybrand = self.request.POST['brand']
                        blog.titel = cd['titel']
                        blog.body = cd['body']
                        blog.image = cd['image']
                        blog.garanty = cd['garanty']
                        blog.seller = self.user
                        blog.time = blog.time
                        blog.brand = get_object_or_404(Brand , brand = mybrand)
                        for tag in cd['tags'] :
                            blog.tags.add(tag)
                        for cate in self.request.POST.getlist('category'):
                            category = get_object_or_404(Category , titel = cate)
                            if category not in blog.category.all():
                                blog.category.add(category)
                        for cate in self.request.POST.getlist('categorys'):
                            category = get_object_or_404(Category , titel= cate)
                            if category in blog.category.all():
                                blog.category.remove(category)
                    try:
                        for mycolor in self.request.POST.getlist('color'):
                            color = get_object_or_404(Colors , color = mycolor)
                            if color not in blog.color.all():
                                blog.color.add(color)
                    except :
                        for mysize in self.request.POST.getlist('size'):
                            size = get_object_or_404(Sizes , size = mysize)
                            if size not in blog.size.all():
                                blog.size.add(size)
                    try :
                        for mycolor in self.request.POST.getlist('colors'):
                            color = get_object_or_404(Colors , color = mycolor)
                            if color in blog.color.all():
                                blog.color.remove(color)
                    except :
                        for mysize in self.request.POST.getlist('sizes'):
                            size = get_object_or_404(Sizes , size = mysize)
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
        context = {'form':form,
        'mycategory':mycategory, 'categorys':categorys, 'brands':brands ,
        'mycolor':mycolor, 'colors':colors,'mysize':mysize, 'sizes':sizes}
        return render(self.request, 'prodact/update.html', context)


    def detail_prodact(self):
        blog = get_object_or_404(Prodact , id = self.id)
        coments = Coments.objects.filter(prodact = blog , published = True )
        custion = Custion.objects.filter(prodact = blog , published = True , one_respones = None , tow_respones = None)
        images = Images.objects.filter(blog = blog)
        nums = get_object_or_404(Nums , blog = blog)
        seller = ProdactSeller.objects.get(prodact=blog)
        category = blog.category.all()
        tags = blog.tags.all()
        tag = blog.tags.values_list('id' , flat = True)
        blogs = Prodact.objects.filter(tags__in = tag , published = True).exclude(id = blog.id)
        myblogs = blogs.annotate(tags_count = Count('tags')).order_by('-tags_count')
        lists = List.objects.filter(user=self.user)#.exclude(list = blog)
        if self.request.method == 'POST' :
            form = ComentsForm(self.request.POST , self.request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                text = Coments.objects.create(body=cd['body'], user=self.user,
                        prodact=blog, image=cd['image'], titel=cd['titel'], bad=cd['bad'],
                        good=cd['good'], sagestion=cd['sagestion'], score=cd['score'])
                text.save()
                return redirect('blog:detail' , blog.id)        
        else:
            form = ComentsForm()
        context = {'blog':blog , 'form':form , 
        'coments':coments , 'lists':lists , 'images':images ,'category':category ,
        'myblogs':myblogs ,'custion':custion , 'tags':tags , 'nums':nums , 'seller':seller}
        return render(self.request, 'prodact/detail.html', context)    


    def detail_prodact(self):
        blog = get_object_or_404(Prodact, id=self.id)
        if self.user.is_seller == True:
            if self.user == blog.seller: 
                blog.image.delete()
                blog.delete()
                return redirect('prodact:list')
            else:
                return redirect('prodact:list')
        else:
            return redirect('prodact:list')
        

