from django import template
from blog.models import Blog, Nums
from django.db.models import Count 
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag()
def like_count(myblog):
    likes = Blog.objects.filter(id = myblog.id).aggregate(Count('likes'))
    return likes['likes__count']


@register.simple_tag()
def coment_count(myblog):
    coments = Blog.objects.filter(id = myblog.id).aggregate(Count('coments_myblog'))
    return coments['coments_myblog__count']


@register.simple_tag()
def view_count(myblog):
    views = Nums.objects.filter(id = myblog.id).aggregate(Count('view'))
    return views['view__count']


@register.simple_tag()
def saveed_count(myblog):
    saveed = Blog.objects.filter(id = myblog.id).aggregate(Count('saved'))
    return saveed['saved__count']


@register.filter()
def show_mark(body):
    return mark_safe(markdown.markdown(body))
