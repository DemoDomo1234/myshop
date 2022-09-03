from django import template
from appblog.models import MyBlog , Nums
from django.db.models import Count 

register = template.Library()

@register.simple_tag()
def like_count(myblog):
    likes = MyBlog.objects.filter(id = myblog.id).aggregate(Count('likes'))
    return likes['likes__count']

@register.simple_tag()
def coment_count(myblog):
    coments = MyBlog.objects.filter(id = myblog.id).aggregate(Count('coments_myblog'))
    return coments['coments_myblog__count']

@register.simple_tag()
def view_count(myblog):
    views = Nums.objects.filter(id = myblog.id).aggregate(Count('view'))
    return views['view__count']

@register.simple_tag()
def saveed_count(myblog):
    saveed = MyBlog.objects.filter(id = myblog.id).aggregate(Count('saved'))
    return saveed['saved__count']