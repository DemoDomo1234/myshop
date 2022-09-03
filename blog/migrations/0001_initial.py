# Generated by Django 4.0.5 on 2022-09-01 14:41

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(max_length=20)),
                ('plaque', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=200)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('number', models.CharField(max_length=11)),
                ('postal_code', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adres_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=100)),
                ('body', mdeditor.fields.MDTextField()),
                ('image', models.ImageField(upload_to='image')),
                ('price', models.PositiveIntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('discount', models.PositiveIntegerField(blank=True)),
                ('number', models.PositiveIntegerField()),
                ('garanty', mdeditor.fields.MDTextField()),
                ('weigth', models.PositiveIntegerField()),
                ('size', models.PositiveIntegerField()),
                ('published', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='blog_address', to='blog.address')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('online', models.BooleanField(default=True)),
                ('ordered', models.BooleanField(default=False)),
                ('cancel', models.BooleanField(default=False)),
                ('destroyed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('current', models.BooleanField(default=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_addresses', to='blog.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_useres', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField()),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog', to='blog.blog')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colores', to='blog.colors')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='blog.order')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_seller', to=settings.AUTH_USER_MODEL)),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizees', to='blog.sizes')),
            ],
        ),
        migrations.CreateModel(
            name='Nums',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField()),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='numes_myblog', to='blog.blog')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noty_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=50, unique=True)),
                ('body', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_images_model', to='blog.blog')),
            ],
        ),
        migrations.CreateModel(
            name='ColorNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField()),
                ('nums', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('published', models.BooleanField(default=False)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_num', to='blog.blog')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colors_num', to='blog.colors')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='num_seller', to=settings.AUTH_USER_MODEL)),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='size_num', to='blog.sizes')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=50)),
                ('more', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='more_categorys', to='blog.category')),
            ],
        ),
        migrations.CreateModel(
            name='BlogSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField(blank=True)),
                ('number', models.PositiveIntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('garanty', mdeditor.fields.MDTextField()),
                ('published', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_address_seller', to='blog.address')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_blog', to='blog.blog')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_brand', to='blog.brand'),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ManyToManyField(related_name='blog_categorys', to='blog.category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='color',
            field=models.ManyToManyField(blank=True, related_name='blog_colors_num', to='blog.colors'),
        ),
        migrations.AddField(
            model_name='blog',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='lists',
            field=models.ManyToManyField(blank=True, related_name='list', to='blog.list'),
        ),
        migrations.AddField(
            model_name='blog',
            name='notifications',
            field=models.ManyToManyField(blank=True, related_name='blog_notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='sizes',
            field=models.ManyToManyField(blank=True, related_name='blog_size_num', to='blog.sizes'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Advertising',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertising_brand', to='blog.brand')),
            ],
        ),
    ]
