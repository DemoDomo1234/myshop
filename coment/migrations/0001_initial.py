# Generated by Django 4.0.5 on 2022-09-18 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('published', models.BooleanField(default=False)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes_custion', to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custion', to='blog.blog')),
                ('one_respones', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='one_custion', to='coment.custion')),
                ('tow_respones', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tow_custion', to='coment.custion')),
                ('unlikes', models.ManyToManyField(blank=True, related_name='unlides_custion', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_custion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComentsBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('published', models.BooleanField(default=False)),
                ('appblog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coments_myblog', to='appblog.myblog')),
                ('likes', models.ManyToManyField(blank=True, related_name='coments_likes_blog', to=settings.AUTH_USER_MODEL)),
                ('unlikes', models.ManyToManyField(blank=True, related_name='coments_unlides_blog', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='coments_user_blog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sagestion', models.CharField(choices=[('y', 'yes'), ('i', 'I do not know'), ('n', 'no')], max_length=50)),
                ('score', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=50)),
                ('titel', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('image', models.ImageField(upload_to='coments_media')),
                ('date', models.DateField(auto_now_add=True)),
                ('bad', models.TextField()),
                ('good', models.TextField()),
                ('published', models.BooleanField(default=False)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coments_blog', to='blog.blog')),
                ('likes', models.ManyToManyField(blank=True, related_name='coments_likes', to=settings.AUTH_USER_MODEL)),
                ('unlikes', models.ManyToManyField(blank=True, related_name='coments_unlides', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='coments_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
