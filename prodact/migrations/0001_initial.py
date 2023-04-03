# Generated by Django 3.2 on 2023-03-06 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prodact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=100)),
                ('body', mdeditor.fields.MDTextField()),
                ('image', models.ImageField(upload_to='image')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('weigth', models.PositiveIntegerField()),
                ('size', models.PositiveIntegerField()),
                ('published', models.BooleanField(default=False)),
                ('garanty', mdeditor.fields.MDTextField()),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_brand', to='base.brand')),
                ('category', models.ManyToManyField(related_name='blog_categorys', to='base.Category')),
                ('color', models.ManyToManyField(blank=True, related_name='blog_colors_num', to='base.Colors')),
                ('like', models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL)),
                ('lists', models.ManyToManyField(blank=True, related_name='blog_list', to='base.List')),
                ('notifications', models.ManyToManyField(blank=True, related_name='blog_notifications', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
                ('sizes', models.ManyToManyField(blank=True, related_name='blog_size_num', to='base.Sizes')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
        migrations.CreateModel(
            name='Nums',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField()),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='numes_prodact', to='prodact.prodact')),
            ],
        ),
    ]
