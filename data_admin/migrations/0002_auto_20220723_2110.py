import logging
from random import randint
from django.db import migrations
from pytils.translit import slugify
from mimesis import Text
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
        # print(slugify(item))
        Areas(title=item, slug=slugify(item)).save()

    tags = ['объекты и места ГУЛАГа', 'архитектура', 'инженерные сооружения',
            'История Москвы', 'места захоронений', 'исчезнувшие места и здания', 'воспоминания и свидетельства']
    for item in tags:
        Tags(title=item, slug=slugify(item)).save()

    settings_admin = {'hi': 'Привет! Это телеграм бот канала им. Москвы! '
                      'Наш проект был задуман как народная история '
                      'великого памятника эпохи. Для запуска бота '
                      'выберете одну из команд: /stayinghome чтобы '
                      'путешествовать по истории сооружений канала'
                      'не выходя из дома. /walkingaround узнайте '
                      'историю конкретного места, расположенного '
                      'ближе всего к Вам. Используйте команду '
                      '/options чтобы настроить свой поиск. '
                      'Если вам известно что-то из истории канала, '
                      'и вы хотите вписать эти сведения в общий '
                      'кадастр, используйте команду /stories. '}
    for name, value in settings_admin.items():
        SettingsAdmin(name=name, value=value).save()

    Users = get_user_model()
    flatr = Users.objects.get(username='flatr')
    areas = Areas.objects.all()
    tag = Tags.objects.all()
    #home
    # base_lat = 57.951503622198096
    # base_lon = 102.74296108124477
    #moskow
    base_lat = 55.78124553340503
    base_lon = 37.70503313373094

    text = Text('ru')
    for _ in range(30):
        title = text.text(quantity=1)[:80]
        post = Posts(lat=base_lat+randint(-100, 100)/10000,
                    lon=base_lon+randint(-100, 100)/10000, 
                    area=areas[randint(1, len(areas)-1)],
                    slug=slugify(title)+str(randint(10000,100000000)),
                    current_user=flatr,
                    title=title,
                    text=text.text(quantity=4)
                    )
        tags=[]
        for _ in range(randint(2, len(tag)-1)):
            tags.append(tag[randint(1, len(tag)-1)])
        post.save()
        post.tag.set(tags)

        images = []
        
        for _ in range(randint(0, 5)):
            url = f'uploads/img/i ({randint(1,64)}).jpg'
            img = Images(image=url)
            img.save()
            images.append(img)

        post.images_set.set(images)
        post.save()



class Migration(migrations.Migration):

    dependencies=[
        ('data_admin', '0001_initial'),
    ]

    operations=[
        migrations.RunPython(generate_superuser),
        migrations.RunPython(set_data),
    ]
