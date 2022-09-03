from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog , Notifications
from django.core.mail import send_mail


@receiver(post_save, sender=Blog)
def send_notifications(sender, instance, created , *args , **kwargs):
    notification = instance.notifications.all()
    if created == False :
        for user in notification :
            email = user.email
            send_mail(instance.titel ,  'http://127.0.0.1:8000'+instance.get_absolute_url() , 'demodomone@gmail.com' , [email] , fail_silently=False , auth_password='g b r m d o g r x l s p u d j t')
            noty = Notifications.objects.create(titel=instance.titel , body= 'http://127.0.0.1:8000'+instance.get_absolute_url() , user=user)
            noty.save()
             