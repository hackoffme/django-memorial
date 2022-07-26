# Generated by Django 4.0.6 on 2022-07-25 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Район поиска')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Территория нахождения',
                'verbose_name_plural': 'Территории нахождения',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('lat', models.DecimalField(decimal_places=15, max_digits=17, verbose_name='Широта')),
                ('lon', models.DecimalField(decimal_places=14, max_digits=17, verbose_name='Долгота')),
                ('is_active', models.BooleanField(default=True, verbose_name='Пост активен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('area', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_admin.areas', verbose_name='Область')),
                ('current_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Тэги')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TgUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.BigIntegerField(unique=True, verbose_name='ID Telegram')),
                ('viewed_posts', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_admin.posts', verbose_name='Просмотренные посты')),
            ],
            options={
                'verbose_name': 'Пользователь телеграмм',
                'verbose_name_plural': 'Пользователи телеграмм',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='posts',
            name='tag',
            field=models.ManyToManyField(related_name='posts', to='data_admin.tags', verbose_name='Тэги'),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads//%Y/%m/%d/', verbose_name='Фотография')),
                ('tg_id', models.BigIntegerField(blank=True, null=True, verbose_name='ID фото на сервере телеграм')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_admin.posts')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
                'ordering': ['id'],
            },
        ),
    ]
