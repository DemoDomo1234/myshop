from django.shortcuts import render , redirect , get_object_or_404
from .models import ComentsBlog , Coments , Custion
from .forms import UpdateComentsForm , UpdateComentsBlogForm , CustionForm , UpdateCustionForm
from blog.models import Blog
from django.contrib.auth.decorators import login_required

@login_required(login_url='account:login')
def update(request , id): 
    text = get_object_or_404(ComentsBlog , id = id)
    user = request.user
    if user == text.user :
        if request.method == 'POST' :
            form = UpdateComentsBlogForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                text.titel = cd['titel']
                text.body = cd['body']
                text.save()
                return redirect('appblog:detail' , text.id)        
        else:
            form = UpdateComentsBlogForm()
    else:
        return redirect('appblog:list')        
    return render(request , 'coments/update.html' , {'form':form , 'text':text})

@login_required(login_url='account:login')
def delete(request , id):
    text = get_object_or_404(ComentsBlog , id = id)
    user = request.user
    if user == text.user :
        if request.method == 'POST' :
            text.delete()
            return redirect('appblog:detail' , text.appblog.id )
        else:
            return render(request , 'coments/delete.html')
    else:
        return redirect('appblog:list')
  
@login_required(login_url='account:login')
def likes(request , id):
    text = get_object_or_404(ComentsBlog , id = id)
    user = request.user
    if user in text.unlikes.all() :
        text.unlikes.remove(user)
    if user not in text.likes.all() :
        text.likes.add(user)
        return redirect( 'appblog:detail' , text.appblog.id)
    else:
        text.likes.remove(user)
        return redirect( 'appblog:detail' , text.appblog.id)

@login_required(login_url='account:login')
def unlikes(request , id):
    text = get_object_or_404(ComentsBlog , id = id)
    user = request.user
    if user in text.likes.all() :
        text.likes.remove(user)
    if user not in text.unlikes.all() :
        text.unlikes.add(user)
        return redirect( 'appblog:detail' , text.appblog.id)
    else:
        text.unlikes.remove(user)
        return redirect( 'appblog:detail' , text.appblog.id)

@login_required(login_url='account:login')
def blog_update(request , id):
    text = get_object_or_404(Coments , id = id)
    user = request.user
    if user == text.user :
        if request.method == 'POST' :
            form = UpdateComentsForm(request.POST , request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                text.titel = cd['titel']
                text.body = cd['body']
                text.bad = cd['bad']
                text.good = cd['good']
                text.image = cd['image']
                text.sagestion = cd['sagestion']
                text.score = cd['score']
                text.save()
                return redirect('blog:detail' , text.id)
        else:
            form = UpdateComentsForm()
    else:
        return redirect('appblog:list')        
    return render(request , 'coments/blog-update.html' , {'form':form , 'text':text})

@login_required(login_url='account:login')
def blog_delete(request , id):
    text = get_object_or_404(Coments , id = id)
    user = request.user
    if user == text.user :
        if request.method == 'POST' :
            text.image.delete()
            text.delete()
            return redirect('blog:detail' , text.blog.id )
            
        else:
            return render(request , 'coments/delete.html')
    else:
        return redirect('blog:list')  
    

    return render(request , 'coments/blog-delete.html')

@login_required(login_url='account:login')
def blog_likes(request , id):
    text = get_object_or_404(Coments , id = id)
    user = request.user
    if user  in text.unlikes.all() :
        text.unlikes.remove(user)
    if user not in text.likes.all() :
        text.likes.add(user)
        return redirect( 'blog:detail' , text.blog.id)
    else:
        text.likes.remove(user)
        return redirect( 'blog:detail' , text.blog.id)

@login_required(login_url='account:login')
def blog_unlikes(request , id):
    text = get_object_or_404(Coments , id = id)
    user = request.user
    if user  in text.likes.all() :
        text.likes.remove(user)
    if user not in text.unlikes.all() :
        text.unlikes.add(user)
        return redirect( 'blog:detail' , text.blog.id)
    else:
        text.unlikes.remove(user)
        return redirect( 'blog:detail' , text.blog.id)

@login_required(login_url='account:login')
def custion_update(request , id):
    custion = get_object_or_404(Custion , id = id)
    user = request.user
    if user == custion.user :
        if request.method == 'POST' :
            form = UpdateCustionForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data['body']
                custion.body = body
                custion.save()
                return redirect('blog:detail' , custion.model.id)
        else:
            form = UpdateCustionForm()
    else:
        return redirect('blog:list')        
    return render(request , 'coments/custion-update.html' , {'form':form , 'custion':custion})

@login_required(login_url='account:login')
def custion_delete(request , id):
    custion = get_object_or_404(Custion , id = id)
    user = request.user
    if user == custion.user :
        if request.method == 'POST' :
            custion.delete()
            return redirect('blog:detail' , custion.model.id )
            
        else:
            return render(request , 'coments/custion-delete.html')
    else:
        return redirect('blog:list')  
    

    return render(request , 'coments/delete.html')

@login_required(login_url='account:login')
def custion_likes(request , id):
    custion = get_object_or_404(Custion , id = id)
    user = request.user
    if user in custion.unlikes.all() :
        custion.unlikes.remove(user)
    if user not in custion.likes.all() :
        custion.likes.add(user)
        return redirect( 'blog:detail' , custion.model.id)
    else:
        custion.likes.remove(user)
        return redirect( 'blog:detail' , custion.model.id)

@login_required(login_url='account:login')
def custion_unlikes(request , id):
    custion = get_object_or_404(Custion , id = id)
    user = request.user
    if user in custion.likes.all() :
        custion.likes.remove(user)
    if user not in custion.unlikes.all() :
        custion.unlikes.add(user)
        return redirect( 'blog:detail' , custion.model.id)
    else:
        custion.unlikes.remove(user)
        return redirect( 'blog:detail' , custion.model.id)

@login_required(login_url='account:login')
def detail(request , id):
    custion = get_object_or_404(Custion , id = id)
    user = request.user
    custions = Custion.objects.filter(one_respones = custion , published = True)
    if request.method == 'POST':
        form = UpdateCustionForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            new_custion = Custion.objects.create(body = body ,
            one_respones = custion , user = user , model = custion.model)
            new_custion.save()
            return redirect('coment:detail' , custion.id)
    else :
        form = UpdateCustionForm()  

    return render(request , 'coments/detail.html' , {'form':form , 'custions':custions})

@login_required(login_url='account:login')
def create_custion(request , id):
    custion = get_object_or_404(Custion , id = id)
    user = request.user
    if request.method == 'POST':
        form = UpdateCustionForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            new_custion = Custion.objects.create(body = body , user = user ,
            one_respones = custion.one_respones , tow_respones = custion , model = custion.model)
            new_custion.save()
            return redirect('coment:detail' , custion.one_respones.id)
    else :
        form = UpdateCustionForm()  
    return render(request , 'coments/create-custion2.html' , {'form':form})

@login_required(login_url='account:login')
def create_one_custin(request , id):
    user = request.user
    blog = get_object_or_404(Blog , id = id)
    if request.method == 'POST' :
        form = CustionForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['custion_body']
            new_custion = Custion.objects.create(body = body , user = user , model=blog)
            new_custion.save()
            return redirect('blog:detail' , blog.id)     
    else:
        form = CustionForm()
    return render(request , 'coments/create-one-custion.html' , {'form':form ,})
