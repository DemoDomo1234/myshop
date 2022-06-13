from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Blog , Notifications
from appblog.models import MyBlog
from django.core.mail import send_mail

@receiver(pre_save, sender=Blog)
def send_notifications(sender, instance, *args , **kwargs):
    notification = instance.notifications.all()
    for user in notification :
        email = user.email
        send_mail(instance.titel ,  'http://127.0.0.1:8000'+instance.get_absolute_url() , 'demodomone@gmail.com' , [email] , fail_silently=False)
        noty = Notifications.objects.create(titel=instance.titel , body= 'http://127.0.0.1:8000'+instance.get_absolute_url() , user=user)
        noty.save()
             
@receiver(pre_save, sender=MyBlog)
def blog_send_notifications(sender, instance, *args , **kwargs):
    notification = instance.notifications.all()
    for user in notification :
        email = user.email
        send_mail(instance.titel ,  'http://127.0.0.1:8000'+instance.get_absolute_url() , 'demodomone@gmail.com' , [email] , fail_silently=False)
        noty = Notifications.objects.create(titel=instance.titel , body= 'http://127.0.0.1:8000'+instance.get_absolute_url() , user=user)
        noty.save()