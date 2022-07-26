import logging
from random import randint
from django.db import migrations
from pytils.translit import slugify
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from data_admin.models import *


def generate_superuser(apps, schema_editor):
    # env = environ.Env()
    # USERNAME = env.str("ADMIN_USERNAME")
    # PASSWORD = env.str("ADMIN_PASSWORD")
    # EMAIL = env.str("ADMIN_EMAIL")

    # env = environ.Env()
    USERNAME = 'flatr'
    PASSWORD = 'flatr'
    EMAIL = 'flatron.88@mail.ru'
    user = get_user_model()

    if not user.objects.filter(username=USERNAME, email=EMAIL).exists():
        admin = user.objects.create_superuser(
            username=USERNAME, password=PASSWORD, email=EMAIL
        )
        admin.save()


def set_data(apps, schema_editor):
    logging.debug('START edeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    areas = ['Савелево', 'от 0 - 18 км', 'от 19 - 35 км',
             'от 36 - 55 км', 'от 56 - 69 км', 'от 70 - 80 км',
             'от 81 - 97 км', 'Мытищи', 'от 98 - 110 км',
             'от 111 - 120 км', 'от 121 - 127 км', 'Троице-Лыково',
             'с. Шелепиха', 'с. Перерва', 'другие сооружения', ]
    for item in areas:
        print(slugify(item))
        Areas(title=item, slug=slugify(item)).save()

    tags = ['объекты и места ГУЛАГа', 'архитектура', 'инженерные сооружения',
            'История Москвы', 'места захоронений', 'исчезнувшие места и здания', 'воспоминания и свидетельства']
    for item in tags:
        Tags(title=item, slug=slugify(item)).save()

    Users = get_user_model()
    d = {'title': 'Идейные соображения высшего порядка, а также консультация с широким активом требует анализа существующий финансовых и административных условий',
         'text': '<p>Прежде всего повышение уровня гражданского сознания играет важную роль в формировании прогресса профессионального общества. Таким образом управление и развитие структуры играет важную роль в формировании поставленных обществом и правительством задач. Следует отметить, что сложившаяся структура организации напрямую зависит от существующий финансовых и административных условий.</p>',
         'lat': 1,
         'lon': 1,
         'current_user_id': 1
         }




class Migration(migrations.Migration):

    dependencies = [
        ('data_admin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
        migrations.RunPython(set_data),
    ]
