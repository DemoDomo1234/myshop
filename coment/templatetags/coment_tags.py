from django import template
from coment.models import ComentsBlog , Coments , Custion
from django.db.models import Count 

register = template.Library()

@register.simple_tag()
def one_respones_count(custion):
    one_respones = Custion.objects.filter(one_respones = custion).aggregate(Count('one_respones'))
    return one_respones['one_respones__count']

@register.simple_tag()
def tow_respones_count(custion):
    tow_respones = Custion.objects.filter(tow_respones = custion).aggregate(Count('tow_respones'))
    return tow_respones['tow_respones__count']

@register.simple_tag()
def coment_like_count(coment):
    likes = Coments.objects.filter(id = coment.id).aggregate(Count('likes'))
    return likes['likes__count']

@register.simple_tag()
def coment_unlike_count(coment):
    unlikes = Coments.objects.filter(id = coment.id).aggregate(Count('unlikes'))
    return unlikes['unlikes__count']

@register.simple_tag()
def blog_coment_like_count(blog):
    likes = ComentsBlog.objects.filter(id = blog.id).aggregate(Count('likes'))
    return likes['likes__count']

@register.simple_tag()
def blog_coment_unlike_count(blog):
    unlikes = ComentsBlog.objects.filter(id = blog.id).aggregate(Count('unlikes'))
    return unlikes['unlikes__count']

@register.simple_tag()
def custion_like_count(custion):
    likes = Custion.objects.filter(id = custion.id).aggregate(Count('likes'))
    return likes['likes__count']

@register.simple_tag()
def custion_unlike_count(custion):
    unlikes = Custion.objects.filter(id = custion.id).aggregate(Count('unlikes'))
    return unlikes['unlikes__count']