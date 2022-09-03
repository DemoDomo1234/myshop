from django.shortcuts import redirect, render
from .models import User , CompanySeller , SellerAccount
from .forms import (SingupForm , LoginForm , ChangepassForm , UpdateForm ,
                    CreateCompanySeller , CreateSellerAccount , UpdateCompanySeller ,
                    UpdateSellerAccount)
from django.contrib.auth import login , logout , authenticate
from blog.models import *
import datetime 
from dateutil.relativedelta import relativedelta
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
    
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
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            national_code = form.cleaned_data['national_code']
            user = User.objects.create(
            username = username , name = name ,
            familie = familie , email = email ,
            number = number ,  password = password ,
            gender = gender , date_of_birth = date_of_birth ,
            national_code = national_code)
            user.set_password(password)
            user.save()
            return redirect('account:login')
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
                    gender = form.cleaned_data['gender']
                    date_of_birth = form.cleaned_data['date_of_birth']
                    national_code = form.cleaned_data['national_code']
                    password = form.cleaned_data['password']
                    password_one = form.cleaned_data['password_one']
                    if user.check_password(password) :
                        user.username = username 
                        user.name = name 
                        user.familie = familie 
                        user.email = email 
                        user.number = number 
                        user.gender = gender 
                        user.date_of_birth = date_of_birth 
                        user.national_code = national_code
                        if karbr.is_seller :
                            user.is_seller = True
                        if karbr.is_staff :
                            user.is_staff = True
                        if karbr.is_admin :
                            user.is_admin = True
                        if karbr.is_active :
                            user.is_active = True
                        if karbr.is_special :
                            user.is_special = True
                        user.set_password(password_one)
                        user.save()
                        return redirect('account:detail' , id)
            else :
                form = UpdateForm()
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request , 'account/update.html' , {'form':form })

def detail(request , id):
    user = request.user
    karbr = User.objects.get(id = id)
    content = {}
    if user.is_authenticated :
        if karbr.username == user.username :
            likes = Blog.objects.filter(like = user) 
            address = Address.objects.filter(user = user)
            notification = Blog.objects.filter(notifications = user)
            orders = Order.objects.filter(user = user)
            ordered = Order.objects.filter(user = user , received = True)
            lists = List.objects.filter(user=user)
            noty = Notifications.objects.filter(user=user)
            content = {'user':user , 'likes':likes , 'notification':notification ,
            'orders':orders , 'ordered':ordered , 'lists':lists , 'address':address ,
            'noty':noty}
            if karbr.is_seller :
                try:
                    companyseller = CompanySeller.objects.get(user = user)
                except: 
                    companyseller = ''
                selleraccount = SellerAccount.objects.get(user = user)
                seller = BlogSeller.objects.filter(seller = user)
                color = ColorNum.objects.filter(seller = user)
                content = {'user':user , 'likes':likes , 'notification':notification ,
            'orders':orders , 'ordered':ordered , 'lists':lists , 'address':address ,
            'noty':noty , 'companyseller':companyseller , 'selleraccount':selleraccount ,
            'seller':seller , 'color':color}
            return render(request , 'account/detail.html' , content)
        return redirect('blog:list')
    return redirect('account:login')
           
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request , username = username , password = password)
            if user is not None :
                if user.is_active :
                    myuser = User.objects.get(id = user.id)
                    if myuser.date_special != None :
                        if myuser.date_special <= datetime.date.today() :
                            myuser.is_special = False
                            myuser.save()
                    login(request , user)
                    return redirect('blog:list')

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
                    password_one = form.cleaned_data['password_one']
                    user.set_password(password_one)
                    user.save()
                    return redirect('account:detail' , id)
            else :
                form = ChangepassForm()
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'account/changepass.html' , {'form':form })

def special_view(request):
    myuser = request.user
    user = User.objects.get(id = myuser.id)
    if user.is_authenticated :
        if request.method == 'POST':
            special = request.POST['special']
            if special == '1':
                date_after_month = datetime.date.today()+ relativedelta(months=1)
                amount = 100000
                
            elif special == '3':
                date_after_month = datetime.date.today()+ relativedelta(months=3)
                amount = 300000
                
            elif special == '12':
                date_after_month = datetime.date.today()+ relativedelta(months=12)
                amount = 1200000
                
            user.date_special = date_after_month
            user.save()
            user_mobile_number = user.number
            factory = bankfactories.BankFactory()
            try:
                bank = factory.auto_create()
                bank.set_request(request)
                bank.set_amount(amount)
                bank.set_client_callback_url(reverse('account:callback_gateway'))
                bank.set_mobile_number(user_mobile_number)  
                bank_record = bank.ready()
                return bank.redirect_gateway()
            except AZBankGatewaysException as e:
                logging.critical(e)
                # TODO: redirect to failed page.
                raise e
    return render(request , 'account/special.html')

def callback_gateway_view(request):
    myuser = request.user
    user = User.objects.get(id = myuser.id)
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        user.special = True
        user.save()
        return redirect('account:detail' , user.id)


    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")

def create_seller_account(request):
    user = request.user
    if user.is_authenticated :     
        if request.method == "POST" :
            form = CreateSellerAccount(request.POST , request.FILES)
            if form.is_valid():

                shop_name = form.cleaned_data['shop_name']
                shaba_number = form.cleaned_data['shaba_number']
                shop_number = form.cleaned_data['shop_number']
                shop_type = form.cleaned_data['shop_type']
                tax = form.cleaned_data['tax']
                national_card = form.cleaned_data['national_card']

                seller_account = SellerAccount.objects.create(
                        shop_name = shop_name , shaba_number = shaba_number ,
                        shop_number = shop_number , shop_type = shop_type ,
                        tax = tax , national_card = national_card ,
                        user = user
                )
                seller_account.save()

                myuser = User.objects.get(id = user.id)
                myuser.is_seller = True
                myuser.save()
                return redirect('blog:list')
        else:
            form = CreateSellerAccount()
    else:
        return redirect('account:login')

    return render(request , 'account/create-seller-account.html' , {'form':form})  

def update_seller_account(request , id):
    seller_account = SellerAccount.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == seller_account.user :
                if request.method == 'POST' :
                    form = UpdateSellerAccount(request.POST , request.FILES)
                    if form.is_valid():

                        shop_name = form.cleaned_data['shop_name']
                        shaba_number = form.cleaned_data['shaba_number']
                        shop_number = form.cleaned_data['shop_number']
                        shop_type = form.cleaned_data['shop_type']
                        tax = form.cleaned_data['tax']
                        national_card = form.cleaned_data['national_card']

                        seller_account.shop_name = shop_name
                        seller_account.shaba_number = shaba_number
                        seller_account.shop_number = shop_number
                        seller_account.shop_type = shop_type
                        seller_account.tax = tax
                        seller_account.national_card = national_card
                        seller_account.save()

                        return redirect('blog:list')
                else:
                    form = UpdateSellerAccount()
            else:
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')

    return render(request , 'account/update-seller-account.html' , {'form':form})

def create_company_seller(request):
    user = request.user
    if user.is_authenticated :     
        if request.method == "POST" :
            form = CreateCompanySeller(request.POST)
            if form.is_valid():
                company_name = form.cleaned_data['company_name']
                company_type = form.cleaned_data['company_type']
                fixed_number = form.cleaned_data['fixed_number']
                economic_code = form.cleaned_data['economic_code']
                permission_to_sign = form.cleaned_data['permission_to_sign']
                company_seller = CompanySeller.objects.create(
                        company_name = company_name ,
                        company_type = company_type , fixed_number = fixed_number ,
                        economic_code = economic_code , permission_to_sign = permission_to_sign ,
                        user = user)
                company_seller.save()
                return redirect('account:create_seller')
        else:
            form = CreateCompanySeller()
    else:
        return redirect('account:login')

    return render(request , 'account/create-company-seller.html' , {'form':form})

def update_company_seller(request , id):
    company_seller = CompanySeller.objects.get(id = id)
    user = request.user
    if user.is_authenticated :
        if user.is_seller == True :
            if user == company_seller.user :
                if request.method == 'POST' :
                    form = UpdateCompanySeller(request.POST)
                    if form.is_valid():
                        company_name = form.cleaned_data['company_name']
                        company_type = form.cleaned_data['company_type']
                        fixed_number = form.cleaned_data['fixed_number']
                        economic_code = form.cleaned_data['economic_code']
                        permission_to_sign = form.cleaned_data['permission_to_sign']

                        company_seller.company_name = company_name
                        company_seller.company_type = company_type
                        company_seller.fixed_number = fixed_number
                        company_seller.economic_code = economic_code
                        company_seller.permission_to_sign = permission_to_sign
                        company_seller.save()
                        return redirect('blog:list')
                else:
                    form = UpdateCompanySeller()
            else:
                return redirect('blog:list')
        else:
            return redirect('blog:list')
    else:
        return redirect('account:login')
    return render(request , 'account/update-company-seller.html' , {'form':form})
