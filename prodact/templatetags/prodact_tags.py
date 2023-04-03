from django import template
from prodact.models import Prodact
from order.models import OrderItem, Order
from base.models import Category
from django.db.models import Count, Sum
from coment.models import Coments
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.utils.safestring import mark_safe
import markdown
register = template.Library()


@register.simple_tag()
def sum_sale(price , discount , num):
    if num == "":
        num = "1"
    dis = discount * price / 100 
    sale = price - dis 
    sale_sum = int(sale) * int(num)
    return sale_sum


@register.simple_tag()
def like_count(blog):
    likes = Prodact.objects.filter(id = blog.id).aggregate(Count('like'))
    return likes['like__count']


@register.simple_tag()
def coment_count(blog):
    coments = Prodact.objects.filter(id = blog.id).aggregate(Count('coments_blog'))
    return coments['coments_blog__count']


@register.simple_tag()
def custion_count(blog):
    custion = Prodact.objects.filter(id = blog.id).aggregate(Count('custion'))
    return custion['custion__count']


@register.simple_tag()
def item_count(user):
    try:
        order = Order.objects.get(user = user , current=True)
    except:
        order = Order.objects.create(user = user , current=True)
        order.save()
    order = Order.objects.get(user = user , current=True)

    item = OrderItem.objects.filter(order = order).aggregate(cart = Count('id'))
    return item["cart"]


@register.inclusion_tag('includes/category-navbar.html')
def category():
    return {'category' : Category.objects.all() ,}


@register.simple_tag()
def score_count(blog):
    count_score = Coments.objects.filter(prodact = blog)
    sum_score = Coments.objects.filter(prodact = blog)
    if count_score.exists() and sum_score.exists() :
        mycount = count_score.aggregate(Count('score'))
        mysum = sum_score.annotate(as_float=Cast('score', FloatField())
        ).aggregate(Sum('as_float'))
        return round(mysum['as_float__sum'] / mycount['score__count'] , 1)
    else:
        return 0


@register.simple_tag()
def sagestion_count(blog):
    count_sagestion = Coments.objects.filter(prodact = blog).aggregate(Count('sagestion'))
    count_sagestion_yes = Coments.objects.filter(prodact = blog , sagestion = 'yes').aggregate(Count('sagestion'))
    if count_sagestion_yes['sagestion__count'] == 0 and count_sagestion['sagestion__count'] == 0 :
        return 0
    else:
        return round(count_sagestion_yes['sagestion__count'] / count_sagestion['sagestion__count'] * 100)


@register.filter()
def show_mark(body):
    return mark_safe(markdown.markdown(body))



@register.simple_tag()
def price(price=10 , discount=10):
    num = round(discount * price / 100)
    return price - num

