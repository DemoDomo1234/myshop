from django.shortcuts import redirect, render
from .models import User
from .forms import SingupForm , LoginForm , ChangepassForm , UpdateForm
from django.contrib.auth import login , logout , authenticate
from blog.models import Blog , List , Order , Address , Notifications

def signup(request):
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            familie = form.cleaned_data['familie']
            email = form.cleaned_data['email']
            number = form.cleaned_data['number']
            password = form.cleaned_data['password']
            is_num = False
            for x in password :
                if x.isdigit() :
                    is_num = True         
            if is_num :
                if len(password) >= 8 :
                    user = User.objects.create(
                    username = username , name = name ,
                    familie = familie , email = email ,
                    number = number ,  password = password )
                    user.set_password(password)
                    user.save()
    else:
        form = SingupForm()
    return render(request , 'account/signup.html' , {'form':form})

def update(request , id):
    user = User.objects.get(id = id)
    karbr = request.user
    if karbr.is_authenticated :
        if karbr.username == user.username :
            if request.method == 'POST':
                form = UpdateForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    name = form.cleaned_data['name']
                    familie = form.cleaned_data['familie']
                    email = form.cleaned_data['email']
                    number = form.cleaned_data['number']
                    password1 = form.cleaned_data['password1']
                    password2 = form.cleaned_data['password2']
                    password3 = form.cleaned_data['password3']
                    is_num = False
                    for x in password2 :
                        if x.isdigit() :
                            is_num = True
                    if user.check_password(password1):
                        if password2 == password3 :
                            if is_num :
                                if len(password2) >= 8 :
                                    user.username = username 
                                    user.name = name 
                                    user.familie = familie 
                                    user.email = email 
                                    user.number = number 
                                    if karbr.is_seller :
                                        user.is_seller = True
                                    if karbr.is_staff :
                                        user.is_staff = True
                                    if karbr.is_admin :
                                        user.is_admin = True
                                    if karbr.is_active :
                                        user.is_active = True

                                    user.set_password(password2)
                                    user.save()
            else :
                form = UpdateForm()
    return render(request , 'account/update.html' , {'form':form })

def detail(request , id):
    user = request.user
    user = User.objects.get(id = id)
    likes = Blog.objects.filter(like = user) 
    address = Address.objects.filter(user= user)
    notification = Blog.objects.filter(notifications = user)
    orders = Order.objects.filter(user = user)
    ordered = Order.objects.filter(user = user , received = True)
    lists = List.objects.filter(user=user)
    noty = Notifications.objects.filter(user=user)
    content = {'user':user , 'likes':likes , 'notification':notification ,
    'orders':orders , 'ordered':ordered , 'lists':lists , 'address':address ,
    'noty':noty}
    karbr = user
    if karbr.is_authenticated :
        if karbr.username == user.username :
            return render(request , 'account/detail.html' , content)
            
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request , username = username , password = password)
            if user is not None :
                if user.is_active :
                    login(request , user)
    else:
        form = LoginForm()
    return render(request , 'account/login.html' , {'form':form})

def logout_view(request):
        logout(request)
        return redirect('blog:list')

def change_password(request , id):
    user = User.objects.get(id = id)
    karbr = request.user
    if karbr.is_authenticated :
        if karbr.username == user.username :
            if request.method == 'POST':
                form = ChangepassForm(request.POST)
                if form.is_valid():
                    password1 = form.cleaned_data['password1']
                    password2 = form.cleaned_data['password2']
                    is_num = False
                    for x in password1 :
                        if x.isdigit() :
                            is_num = True
                    if password1 == password2 :
                        if is_num :
                            if len(password1) >= 8 :
                                user.set_password(password1)
                                user.save()
            else :
                form = ChangepassForm()
    return render(request , 'account/changepass.html' , {'form':form })