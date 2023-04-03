from django.shortcuts import redirect, render, get_object_or_404
from .models import ProdactSeller, ColorNum, CompanySeller, SellerAccount
from account.models import User
from .forms import *
from django.db.models import Sum 
from django.contrib.auth.decorators import login_required
from prodact.models import Prodact
from address.models import Address
from base.models import *


@login_required(login_url='account:login')
def create_seller_account(request):
    user = request.user
    if request.method == "POST":
        form = CreateSellerAccount(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            seller_account = SellerAccount.objects.create(
                    shop_name=cd['shop_name'], shaba_number=cd['shaba_number'],
                    shop_number=cd['shop_number'], shop_type=cd['shop_type'],
                    tax=cd['tax'], national_card=cd['national_card'],
                    user=user
            )
            seller_account.save()
            myuser = get_object_or_404(User, id=user.id)
            myuser.is_seller = True
            myuser.save()
            return redirect('blog:list')
    else:
        form = CreateSellerAccount()
    return render(request, 'seller/create-seller-account.html', {'form':form})  


@login_required(login_url='account:login')
def update_seller_account(request, id):
    seller_account = get_object_or_404(SellerAccount, id=id)
    user = request.user
    if user.is_seller == True:
        if user == seller_account.user:
            if request.method == 'POST':
                form = UpdateSellerAccount(request.POST, request.FILES)
                if form.is_valid():
                    cd = form.cleaned_data
                    seller_account.shop_name = cd['shop_name']
                    seller_account.shaba_number = cd['shaba_number']
                    seller_account.shop_number = cd['shop_number']
                    seller_account.shop_type = cd['shop_type']
                    seller_account.tax = cd['tax']
                    seller_account.national_card = cd['national_card']
                    seller_account.save()
                    return redirect('blog:list')
            else:
                form = UpdateSellerAccount()
        else:
            return redirect('blog:list')
    else:
        return redirect('blog:list')
    return render(request, 'seller/update-seller-account.html', {'form':form})


@login_required(login_url='account:login')
def create_company_seller(request):
    user = request.user
    if request.method == "POST":
        form = CreateCompanySeller(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            company_seller = CompanySeller.objects.create(
                company_name=cd['company_name'], permission_to_sign=cd['permission_to_sign'],
                company_type=cd['company_type'], fixed_number=cd['fixed_number'],
                economic_code=cd['economic_code'], user=user)
            company_seller.save()
            return redirect('account:create_seller')
    else:
        form = CreateCompanySeller()
    return render(request, 'seller/create-company-seller.html', {'form':form})


@login_required(login_url='account:login')
def update_company_seller(request, id):
    company_seller = get_object_or_404(CompanySeller, id=id)
    user = request.user
    if user.is_seller == True:
        if user == company_seller.user:
            if request.method == 'POST':
                form = UpdateCompanySeller(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    company_seller.company_name = cd['company_name']
                    company_seller.company_type = cd['company_type']
                    company_seller.fixed_number = cd['fixed_number']
                    company_seller.economic_code = cd['economic_code']
                    company_seller.permission_to_sign = cd['permission_to_sign']
                    company_seller.save()
                    return redirect('blog:list')
            else:
                form = UpdateCompanySeller()
        else:
            return redirect('blog:list')
    else:
        return redirect('blog:list')
    return render(request, 'seller/update-company-seller.html', {'form':form})


@login_required(login_url='account:login')
def sellers_delete(request, id):
    seller = get_object_or_404(ProdactSeller, id=id)
    user = request.user
    if user == seller.seller:
        if request.method == 'POST':
            seller.delete()
            return redirect('blog:list')
    else :
        return redirect('blog:list')

    return render(request, 'seller/seller-delete.html')


@login_required(login_url='account:login')
def color_num_delete(request, id):
    colors = get_object_or_404(ColorNum, id=id)
    user = request.user
    seller = get_object_or_404(ProdactSeller, blog=colors.blog, seller=user)
    if seller == colors.seller:
        if request.method == 'POST':
            colors.delete()
            return redirect('blog:detail', colors.blog.id)
    else :
        return redirect('blog:list')
    return render(request, 'seller/delete-num.html')


@login_required(login_url='account:login')
def sellers(request, id):
    blog = get_object_or_404(Prodact, id=id)
    user = request.user
    addresses = Address.objects.filter(user=user)
    if request.method == 'POST':
        form = Sellers(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            myaddress = request.POST['address']
            address = get_object_or_404(Address, user=user, name=myaddress)
            seller = ProdactSeller.objects.create(blog=blog, seller=user, address=address,
            number=cd['number'], price=cd['price'], discount=cd['discount'])
            seller.save()
            return redirect('blog:detail', id)
    else:
        form = Sellers()
    return render(request, 'seller/sellers.html', {'form':form, 'addresses':addresses})


@login_required(login_url='account:login')
def sellers_update(request, id):
    seller = get_object_or_404(ProdactSeller, id=id)
    user = request.user
    addresses = Address.objects.filter(user=user)
    if user == seller.seller:
        if request.method == 'POST':
            form = Sellers(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                myaddress = request.POST['address']
                address = get_object_or_404(Address, user=user, name=myaddress)
                seller.price = cd['price']
                seller.number = cd['number']
                seller.discount = cd['discount']
                seller.save()
                return redirect('blog:detail', seller.blogid)
        else:
            form = Sellers()
    else :
        return redirect('blog:list')
    return render(request, 'seller/seller-update.html', {'form':form, 'addresses':addresses})


@login_required(login_url='account:login')
def color_num(request, id):
    blog = get_object_or_404(Prodact, id=id)
    user = request.user
    if request.method == 'POST':
        form = ColorNumForm(request.POST, blog=blog)
        seller = get_object_or_404(ProdactSeller, blog=blog, seller=user)
        if form.is_valid():
            num = form.cleaned_data['num']
            price = form.cleaned_data['price']
            try :
                color = form.cleaned_data['color']
                color = get_object_or_404(Colors, color=color)
                colors = ColorNum.objects.create(blog=blog, seller=seller, num=num,
                color=color, price=price)
            except :
                size = form.cleaned_data['size']
                size = Sizes.objects.get(size=size)
                colors = ColorNum.objects.create(blog=blog, seller=user, num=num,
                size=size, price=price)
            mycolor = ColorNum.objects.filter(seller=seller, blog=blog).aggregate(Sum('num'))
            if mycolor['num__sum'] == None:
                mycolor['num__sum'] = 0
            mynum = mycolor['num__sum'] + int(num)
            if mynum <= seller.number:
                colors.save()
                return redirect('blog:detail', id)
    else:
        form = ColorNumForm(blog=blog)
    return render(request, 'seller/create-num.html', {'form':form})


@login_required(login_url='account:login')
def color_num_update(request, id):
    colors = get_object_or_404(ColorNum, id=id)
    user = request.user
    seller = get_object_or_404(ProdactSeller, blog=colors.blog, seller=user)
    if seller == colors.seller:
        if request.method == 'POST':
            form = ColorNumForm(request.POST, blog=colors.blog)
            if form.is_valid():
                num = form.cleaned_data['num']
                price = form.cleaned_data['price']
                try :
                    color = form.cleaned_data['color']
                    color = get_object_or_404(Colors, color=color)
                    colors.color = color
                    colors.size = None
                except :
                    size = form.cleaned_data['size']
                    size = get_object_or_404(Sizes, size=size)
                    colors.size = size
                    colors.color = None
                colors.num = num 
                colors.price = price
                mycolor = ColorNum.objects.filter(seller=seller, blog=colors.blog).aggregate(Sum('num'))
                if mycolor['num__sum'] == None:
                    mycolor['num__sum'] = 0
                mynum = mycolor['num__sum'] + int(num) - colors.num
                if mynum <= seller.number :
                    colors.save()
                return redirect('seller:detail' , colors.blog.id)
        else:
            form = ColorNumForm(blog=colors.blog)
    else :
        return redirect('blog:list')
    return render(request, 'seller/update-num.html', {'form':form, 'colors':colors})

