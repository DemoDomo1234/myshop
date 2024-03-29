# Generated by Django 3.2 on 2023-03-06 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prodact', '0001_initial'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_images_model', to='prodact.prodact'),
        ),
        migrations.AddField(
            model_name='category',
            name='more',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='more_categorys', to='base.category'),
        ),
        migrations.AddField(
            model_name='advertising',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertising_brand', to='base.brand'),
        ),
    ]
