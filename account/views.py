from django.shortcuts import redirect, render, get_object_or_404
from .models import User
from .forms import SingupForm, LoginForm, ChangepassForm, UpdateForm
from django.contrib.auth import login, logout, authenticate
from prodact.models import Prodact
from base.models import *
from address.models import Address
from order.models import *
from seller.models import *
import datetime 
from dateutil.relativedelta import relativedelta
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create(
            username=cd['username'], name=cd['name'],
            familie=cd['familie'], email=cd['email'],
            number=cd['number'], gender=cd['gender'],
            date_of_birth=cd['date_of_birth'],
            national_code=cd['national_code'])

            user.set_password(cd['password'])
            user.save()
            return redirect('account:login')
    else:
        form = SingupForm()
    return render(request, 'account/signup.html', {'form':form})


@login_required(login_url='account:login')
def update(request, id):
    user = get_object_or_404(User, id=id)
    karbr = request.user
    if karbr.username == user.username :
        if request.method == 'POST':
            form = UpdateForm(request.POST, user=karbr)
            if form.is_valid():
                cd = form.cleaned_data
                if user.check_password(cd['password']) :
                    user.username = cd['username'] 
                    user.name = cd['name'] 
                    user.familie = cd['familie'] 
                    user.email = cd['email'] 
                    user.number = cd['number'] 
                    user.gender = cd['gender'] 
                    user.date_of_birth = cd['date_of_birth'] 
                    user.national_code = cd['national_code']
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
                    user.set_password(cd['password_one'])
                    user.save()
                    return redirect('account:detail', id)
        else:
            form = UpdateForm(user=karbr)
    else:
        return redirect('blog:list')
    return render(request, 'account/update.html', {'form':form })


@login_required(login_url='account:login')
def detail(request, id):
    user = request.user
    karbr = get_object_or_404(User, id=id)
    content = {}
    if karbr.username == user.username:
        likes = karbr.seller.all() 
        address = karbr.adres_user.all()
        notification = karbr.blog_notifications.all()
        orders = karbr.order_useres.all()
        ordered = karbr.order_useres.filter(received=True)
        lists = karbr.list_user.all()
        noty = karbr.noty_user.all()
        content = {'user':user, 'likes':likes, 'notification':notification,
        'orders':orders, 'ordered':ordered, 'lists':lists, 'address':address,
        'noty':noty}
        if karbr.is_seller :
            try:
                companyseller = karbr.user_seller_company.all()
            except: 
                companyseller = ''
            selleraccount = karbr.user_seller_account.all()
            seller = karbr.blog_seller.all()
            try:
              color = karbr.num_seller.all()
            except:
                color = ''
            content = {'user':user, 'likes':likes, 'notification':notification,
        'orders':orders, 'ordered':ordered, 'lists':lists, 'address':address,
        'noty':noty, 'companyseller':companyseller, 'selleraccount':selleraccount,
        'seller':seller, 'color':color}
        return render(request, 'account/detail.html', content)
    return redirect('blog:list')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    myuser = get_object_or_404(User, id=user.id)
                    if myuser.date_special != None:
                        if myuser.date_special <= datetime.date.today():
                            myuser.is_special = False
                            myuser.save()
                    login(request, user)
                    return redirect('blog:list')

    else:
        form = LoginForm(request=request)
    return render(request, 'account/login.html', {'form':form})


def logout_view(request):
        logout(request)
        return redirect('blog:list')


@login_required(login_url='account:login')
def change_password(request, id):
    user = get_object_or_404(User, id=id)
    karbr = request.user
    if karbr.username == user.username:
        if request.method == 'POST':
            form = ChangepassForm(request.POST)
            if form.is_valid():
                password_one = form.cleaned_data['password_one']
                user.set_password(password_one)
                user.save()
                return redirect('account:detail', id)
        else :
            form = ChangepassForm()
    else:
        return redirect('blog:list')

    return render(request, 'account/changepass.html', {'form':form })


@login_required(login_url='account:login')
def special_view(request):
    myuser = request.user
    user = get_object_or_404(User, id=myuser.id)
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
            raise e
    return render(request, 'account/special.html')


@login_required(login_url='account:login')
def callback_gateway_view(request):
    myuser = request.user
    user = get_object_or_404(User, id=myuser.id)
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
        return redirect('account:detail', user.id)
    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")

