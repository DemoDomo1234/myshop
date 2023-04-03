from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from .models import Order, OrderItem
from base.models import Colors, Sizes
from address.models import Address
from seller.models import ColorNum, ProdactSeller
from prodact.models import Prodact, Nums
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from django.contrib.gis.db.models.functions import Distance
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .order import OrderClass


@login_required(login_url='account:login')
def order(request):
    order = OrderClass(request)
    order.create_order()
    return render(request, 'order/order.html', order.context)


@login_required(login_url='account:login')
def shop(request, id):
    order = OrderClass(request, id)
    order.shop()


@login_required(login_url='account:login')
def unshop(request, id):
    order = OrderClass(request, id)
    order.create_order()


@login_required(login_url='account:login')
def order_pdf(request, id):
    order = get_object_or_404(Order, id=id)
    user = request.user
    if user == order.user :
        pdf = HttpResponse(content_type='application/pdf')
        pdf["ontent-Dispoxiyions"] = 'attachment;filename=order' +  str(request.user.username)+str(datetime.datetime.now())+'.pdf'
        html_url  = "order/pdf.html"
        html = get_template(html_url)
        text = {'order':order}
        my_html = html.render(text)
        pisa.CreatePDF(my_html , dest=pdf)
        return pdf
    else:
        return redirect('blog:list')


@login_required(login_url='account:login')
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    user = request.user
    if user == order.user :
        item = OrderItem.objects.filter(order = order)
        return render(request , 'order/order-detail.html' , {'order':order , 'item':item})
    else:
        return redirect('blog:list')


@login_required(login_url='account:login')
def go_to_gateway_view(request):
    user = request.user
    order = get_object_or_404(Order , user = user , current=True)
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = order.price
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = user.number  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('blog:callback_gateway'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


@login_required(login_url='account:login')
def callback_gateway_view(request):
    user = request.user
    order = get_object_or_404(Order , user = user , current=True)
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
        order.received = True
        order.save()
        return redirect('blog:order_detail' , order.id)


    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")


@login_required(login_url='account:login')
def item_update(request , id):
    order = OrderClass(request, id)
    order.update_item()
    return render(request, 'order/order.html', order.context)


def select_seller(request, id):
    if request.method == 'POST':
        blog = get_object_or_404(Prodact, id=id)
        try:
            mycolor = request.POST['color']
            color = get_object_or_404(Colors, color=mycolor)
            colors = ColorNum.objects.filter(blog=blog, published=True, color=color)
        except:
            mysize = request.POST['size']
            size = get_object_or_404(Sizes, size=mysize)
            colors = ColorNum.objects.filter(blog=blog, published=True, siez=size)
    return render(request, 'order/seller-select.html', {'colors':colors})


def inter_num(request, id):
    if request.method == 'POST' :
        color = get_object_or_404(ColorNum, id=id)
    return render(request, 'order/inter-num.html', {'color':color})
