from django.shortcuts import redirect, render, get_object_or_404
from .models import Images, Category, List
from .forms import *
from django.contrib.auth.decorators import login_required
from prodact.models import Prodact



@login_required(login_url='account:login')
def create_image(request, id):
    blog = get_object_or_404(Prodact, id=id)
    user = request.user
    if user.is_seller == True:  
        if blog.seller == user:     
            if request.method == "POST":
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                    image = form.cleaned_data['image']
                    images = Images.objects.create(
                        image=image, blog=blog)
                    images.save()
                    return redirect('blog:list')
            else:
                form = ImageForm()
        else:
            return redirect('blog:list')
    else:
        return redirect('blog:list')

    return render(request, 'base/create-image.html', {'form':form})    


@login_required(login_url='account:login')
def update_image(request, id):
    images = get_object_or_404(Images, id=id)
    user = request.user
    if user.is_seller == True:
        if user == images.blog.seller:
            if request.method == 'POST':
                form = ImageForm(request.POST,  request.FILES)
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
    return render(request, 'base/update-image.html', {'form':form})


@login_required(login_url='account:login')
def delete_image(request, id):
    images = get_object_or_404(Images, id=id)
    user = request.user
    if user.is_authenticated:
        if user.is_seller == True:
            if user == images.blog.seller:
                if request.method == 'POST':
                    images.image.delete()
                    images.delete()
                    return redirect('blog:list')
            else:
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request, 'base/delete-image.html')


@login_required(login_url='account:login')
def create_category(request):
    user = request.user
    if user.is_seller == True:
        if request.method == "POST":
            form = CreateCategory(request.POST)
            if form.is_valid():
                titel = form.cleaned_data['titel']
                more = form.cleaned_data['more']
                category = Category.objects.create(titel=titel, more=more)
                category.save()
                return redirect('blog:create')
        else:
            form = CreateCategory()
    else:
        redirect('blog:list')
    return render(request, 'base/createcategory.html', {'form':form})


def category_list(request, id):
    category = get_object_or_404(Category, id=id)
    blog = Prodact.objects.filter(category=category, published=True)
    return render(request, 'base/category-list.html', {'blog':blog})


@login_required(login_url='account:login')
def create_list(request):
    user=request.user
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lists = List.objects.create(titel=cd['titel'],
            user=user, body=cd['body'])
            lists.save()
            return redirect('blog:list')
    else:
        form = ListForm()
    return render(request, 'base/createlist.html', {'form':form})


@login_required(login_url='account:login')
def update_list(request, id):
    lists = get_object_or_404(List, id=id)
    user = request.user
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
    return render(request, 'base/updatelist.html', {'form':form})


@login_required(login_url='account:login')
def detail_list(request, id):
    lists = get_object_or_404(List, id=id)
    user = request.user 
    if user == lists.user:
        blog = Prodact.objects.filter(lists=lists)
        return render(request, 'base/detaillist.html', {'blog':blog, 'lists':lists})
    else :
        return redirect('blog:list')


@login_required(login_url='account:login')
def delete_list(request, id):
    lists = get_object_or_404(List, id=id)
    user = request.user
    if user == lists.user:
        if request.method == 'POST':
            lists.delete()
            return redirect('blog:list')
    else:
        return redirect('blog:list')
    return render(request, 'base/deletelist.html')


@login_required(login_url='account:login')
def list_view(request, id):
    user = request.user
    if request.method == 'POST':
        titel = request.POST.getlist('titel')
        for i in titel:
            titels = get_object_or_404(List, titel=i)
            if user == titels.user:
                blog = get_object_or_404(Prodact, id=id)
                if titels not in blog.lists.all():
                    blog.lists.add(titels)
                    return redirect('blog:detail', id)
            else:
                return redirect('blog:list')


@login_required(login_url='account:login')
def unlist_view(request, id):
    blog = get_object_or_404(Prodact, id=id)
    user=request.user 
    if request.method == 'POST':
        titel = request.POST.getlist('titel')
        for i in titel :
            titels = get_object_or_404(List, titel=i)
            if user == titels.user:
                if titels in blog.lists.all():
                    blog.lists.remove(titels)
                    return redirect('blog:detail', id)
            else:
                return redirect('blog:list')


@login_required(login_url='account:login')
def notifications(request, id):
    blog = get_object_or_404(Prodact, id=id)
    user = request.user
    if user not in blog.notifications.all():
        blog.notifications.add(user)
        return redirect( 'blog:detail', id)
    else:
        blog.notifications.remove(user)
        return redirect( 'blog:detail', id)

