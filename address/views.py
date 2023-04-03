from django.shortcuts import redirect, render, get_object_or_404
from .models import Address 
from django.contrib.gis.geos import Point
from .forms import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='account:login')
def add_address(request):
    user = request.user
    if request.method =='POST':
        lat=float(request.POST['latitude'])
        long=float(request.POST['longitude'])
        location=Point(long,lat,srid=4326)
        form = AddressForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            address = Address.objects.create(user=user, name=cd['name'],
            location=location, floor=cd['floor'], plaque=cd['plaque'],
            number=cd['number'], postal_code=cd['postal_code'])
            address.save()
            return redirect('account:detail', user.id)
    else:
        form = AddressForm()
    return render(request,'address/addaddress.html', {'form':form})


@login_required(login_url='account:login')
def update_address(request, id):
    user = request.user
    address = get_object_or_404(Address, id=id)
    if user == address.user:
        if request.method == 'POST':
            lat=float(request.POST['latitude'])
            long=float(request.POST['longitude'])
            form = UpdateAddressForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                address.floor = cd['floor']
                address.plaque = cd['plaque']
                address.name = cd['name']
                address.number = cd['number']
                address.postal_code = cd['postal_code']
                address.location=Point(long,lat,srid=4326) 
                address.save()
                return redirect('blog:list')
        else:
            form = UpdateAddressForm()
    else:
        return redirect('blog:list')       
    return render(request,'address/updateaddress.html', {'form':form})


@login_required(login_url='account:login')
def delete_address(request, id):
    user = request.user
    address = get_object_or_404(Address, id=id)
    if user == address.user:
        if request.method =='POST':
            address.delete()
            return redirect('account:detail', user.id)
    else:
        return redirect('blog:list')
    return render(request,'address/deleteaddress.html')

