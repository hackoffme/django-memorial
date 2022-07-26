# Generated by Django 4.1.1 on 2022-09-20 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data_admin', '0002_alter_areas_title_alter_tags_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(verbose_name='like')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_admin.posts', verbose_name='Пост')),
                ('tg_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_admin.tgusers', to_field='tg_id', verbose_name='Пользователь телеграмм')),
            ],
            options={
                'verbose_name': 'Лайк поста',
                'verbose_name_plural': 'Лайки постов',
            },
        ),
    ]
