from django import template
from appblog.models import MyBlog , Nums
from django.db.models import Count 

register = template.Library()

@register.simple_tag(takes_context=True)
def like_count():
    likes = MyBlog.objects.all().aggregate(Count('likes'))
    return likes

@register.simple_tag(takes_context=True)
def unlike_count():
    unlikes = MyBlog.objects.all().aggregate(Count('unlikes'))
    return unlikes

@register.simple_tag(takes_context=True)
def coment_count():
    coments = MyBlog.objects.all().annotate(Count('coments'))
    return coments

@register.simple_tag(takes_context=True)
def view_count():
    views = Nums.objects.all().aggregate(Count('num'))
    return views