from django import template
from blog.models import Blog

register = template.Library()

@register.simple_tag(takes_context=True)
def sum_sale(price , discount , num):
    sale = price - discount
    sale_sum = sale * num
    return sale_sum

@register.simple_tag(takes_context=True)
def like_count():
    likes = Blog.objects.all().aggregate(likes)
    return likes

@register.simple_tag(takes_context=True)
def unlike_count():
    unlikes = Blog.objects.all().aggregate(unlikes)
    return unlikes

@register.simple_tag(takes_context=True)
def coment_count():
    coments = Blog.objects.all().annotate(coments)
    return coments