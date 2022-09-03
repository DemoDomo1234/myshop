from django.shortcuts import render , redirect
from .models import ComentsBlog , Coments , Custion
from .forms import UpdateComentsForm , UpdateComentsBlogForm , CustionForm , UpdateCustionForm
from blog.models import Blog

def update(request , id): 
    text = ComentsBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == text.user :
            if request.method == 'POST' :
                form = UpdateComentsBlogForm(request.POST)
                if form.is_valid():
                    titel = form.cleaned_data['titel']
                    body = form.cleaned_data['body']
                    text.titel = titel
                    text.body = body
                    text.user = request.user
                    text.date = text.date
                    text.save()
                    return redirect('appblog:detail' , text.id)        
            else:
                form = UpdateComentsBlogForm()
        else:
            return redirect('appblog:list')        
    else:
        return redirect('account:login')
    return render(request , 'coments/update.html' , {'form':form , 'text':text})

def delete(request , id):
    text = ComentsBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == text.user :
            if request.method == 'POST' :
                text.delete()
                return redirect('appblog:detail' , text.appblog.id )
            else:
                return render(request , 'coments/delete.html')
        else:
            return redirect('appblog:list')
    else:
        return redirect('account:login')   

def likes(request , id):
    text = ComentsBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user in text.unlikes.all() :
            text.unlikes.remove(user)
        if user not in text.likes.all() :
            text.likes.add(user)
            return redirect( 'appblog:detail' , text.appblog.id)
        else:
            text.likes.remove(user)
            return redirect( 'appblog:detail' , text.appblog.id)
    else:
        return redirect('account:login')
  
def unlikes(request , id):
    text = ComentsBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user in text.likes.all() :
            text.likes.remove(user)

        if user not in text.unlikes.all() :
            text.unlikes.add(user)
            return redirect( 'appblog:detail' , text.appblog.id)

        else:
            text.unlikes.remove(user)
            return redirect( 'appblog:detail' , text.appblog.id)
    else:
        return redirect('account:login')
  
def blog_update(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == text.user :
            if request.method == 'POST' :
                form = UpdateComentsForm(request.POST , request.FILES)
                if form.is_valid():
                    titel = form.cleaned_data['titel']
                    body = form.cleaned_data['body']
                    bad = form.cleaned_data['bad']
                    good = form.cleaned_data['good']
                    image = form.cleaned_data['image']
                    sagestion = form.cleaned_data['sagestion']
                    score = form.cleaned_data['score']
                    text.titel = titel
                    text.body = body
                    text.bad = bad
                    text.good = good
                    text.image = image
                    text.sagestion = sagestion
                    text.score = score
                    text.user = request.user
                    text.date = text.date
                    text.save()
                    return redirect('blog:detail' , text.id)
            else:
                form = UpdateComentsForm()
        else:
            return redirect('appblog:list')        
    else:
        return redirect('account:login')
    return render(request , 'coments/blog-update.html' , {'form':form , 'text':text})

def blog_delete(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == text.user :
            if request.method == 'POST' :
                text.image.delete()
                text.delete()
                return redirect('blog:detail' , text.blog.id )
                
            else:
                return render(request , 'coments/delete.html')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')  
    

    return render(request , 'coments/blog-delete.html')

def blog_likes(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in text.unlikes.all() :
            text.unlikes.remove(user)

        if user not in text.likes.all() :
            text.likes.add(user)
            return redirect( 'blog:detail' , text.blog.id)

        else:
            text.likes.remove(user)
            return redirect( 'blog:detail' , text.blog.id)

    else:
        return redirect( 'account:login')
        
def blog_unlikes(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in text.likes.all() :
            text.likes.remove(user)
        
        if user not in text.unlikes.all() :
            text.unlikes.add(user)
            return redirect( 'blog:detail' , text.blog.id)

        else:
            text.unlikes.remove(user)
            return redirect( 'blog:detail' , text.blog.id)

    else:
        return redirect( 'account:login')

def custion_update(request , id):
    custion = Custion.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == custion.user :
            if request.method == 'POST' :
                form = UpdateCustionForm(request.POST)
                if form.is_valid():
                    body = form.cleaned_data['body']
                    custion.body = body
                    custion.save()
                    return redirect('blog:dteail' , custion.model.id)
            else:
                form = UpdateCustionForm()
        else:
            return redirect('blog:list')        
    else:
        return redirect('account:login')
    return render(request , 'coments/custion-update.html' , {'form':form , 'custion':custion})

def custion_delete(request , id):
    custion = Custion.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == custion.user :
            if request.method == 'POST' :
                custion.delete()
                return redirect('blog:detail' , custion.model.id )
                
            else:
                return render(request , 'coments/custion-delete.html')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')  
    

    return render(request , 'coments/delete.html')

def custion_likes(request , id):
    custion = Custion.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user in custion.unlikes.all() :
            custion.unlikes.remove(user)
        if user not in custion.likes.all() :
            custion.likes.add(user)
            return redirect( 'blog:detail' , custion.model.id)
        else:
            custion.likes.remove(user)
            return redirect( 'blog:detail' , custion.model.id)

def custion_unlikes(request , id):
    custion = Custion.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user in custion.likes.all() :
            custion.likes.remove(user)

        if user  in custion.likes.all() :
            custion.likes.remove(user)
            return redirect( 'blog:detail' , custion.model.id)

        else:
            custion.unlikes.remove(user)
            return redirect( 'blog:detail' , custion.model.id)

def detail(request , id):
    custion = Custion.objects.get(id = id)
    user = request.user
    custions = Custion.objects.filter(one_respones = custion , published = True)

    if user.is_authenticated :
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
    else:
        return redirect('account:login')
    return render(request , 'coments/detail.html' , {'form':form , 'custions':custions})

def create_custion(request , id):
    custion = Custion.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
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
    else:
        return redirect('account:login')
    return render(request , 'coments/create-custion2.html' , {'form':form})
