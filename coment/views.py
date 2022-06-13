from cgitb import text
from django.shortcuts import render , redirect
from .models import ComentsBlog , Blog
from .forms import UpdateComentsForm , UpdateComentsBlogForm
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
            else:
                form = UpdateComentsBlogForm()
    return render(request , 'coments/update.html' , {'form':form , 'text':text})

def delete(request , id):
    text = ComentsBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == text.user :
            if request.method == 'POST' :
                text.delete()
    return render(request , 'coments/delete.html')

def likes(request , id):
    text = ComentsBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in text.likes.all() :
            text.likes.add(user)
        else:
            text.likes.remove(user)
    return redirect( 'blog:list')

def unlikes(request , id):
    text = ComentsBlog.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in text.likes.all() :
            text.likes.remove(user)
        else:
            text.unlikes.remove(user)
    return redirect( 'blog:list')

def blog_update(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == text.user :
            if request.method == 'POST' :
                form = UpdateComentsForm(request.POST)
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
            else:
                form = UpdateComentsForm()
    return render(request , 'coments/update.html' , {'form':form , 'text':text})

def blog_delete(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user == text.user :
            if request.method == 'POST' :
                text.image
                text.delete()
    return render(request , 'coments/delete.html')

def blog_likes(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user not in text.likes.all() :
            text.likes.add(user)
        else:
            text.likes.remove(user)
    return redirect( 'blog:list')

def blog_unlikes(request , id):
    text = Coments.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user  in text.likes.all() :
            text.likes.remove(user)
        else:
            text.unlikes.remove(user)
    return redirect( 'blog:list')
