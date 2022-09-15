import re
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core import validators

from django_admin_geomap import GeoItem
from tinymce import models as models_tinymce
from PIL import Image
import bleach


def _clear_text_for_model(text):
    text = bleach.clean(text,
                        tags=['bold', 'strong', 'i', 'em', 'code', 's',
                              'strike', 'del', 'u',  'br', 'a', 'br', 'p'],
                        strip=True)
    text = re.sub("^\s+|\n|\r|&nbsp;|\s+$", '', text)
    return text


class SettingsAdmin(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название настройки')
    value = models.TextField(verbose_name='Значение настройки')

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки приложения'
        ordering = ['id']

    def __str__(self):
        return self.name


class Areas(models.Model):
    title = models.CharField(max_length=200,
                             validators=[validators.MinLengthValidator(
                                 5, "Минимум 5 символов")],
                             verbose_name='Район поиска')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    def clean(self):
        self.title = bleach.clean(self.title, strip=True).strip()
        if len(self.title) < 5:
            raise ValidationError(
                'После очистки текста от тэгов html осталось меньше 5 символов.')

    class Meta:
        verbose_name = 'Территория нахождения'
        verbose_name_plural = 'Территории нахождения'
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_areas', kwargs={'areas_slug': self.slug})


class Tags(models.Model):
    title = models.CharField(max_length=200,
                             validators=[validators.MinLengthValidator(
                                 5, 'Минимум 5 символов')],
                             unique=True,
                             verbose_name='Тэги')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    def clean(self):
        self.title = bleach.clean(self.title, strip=True).strip()
        if len(self.title) < 5:
            raise ValidationError(
                'После очистки текста от тэгов html осталось меньше 5 символов.')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['id']

    def __str__(self):
        return self.title


class Posts(models.Model, GeoItem):
    title = models.CharField(max_length=200,
                             verbose_name='Заголовок')
    text = models_tinymce.HTMLField(verbose_name='Текст')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    area = models.ForeignKey(Areas,
                             blank=True,
                             to_field='id',
                             on_delete=models.PROTECT,
                             verbose_name='Область')
    tag = models.ManyToManyField(Tags,
                                 related_name='posts',
                                 verbose_name='Тэги')
    current_user = models.ForeignKey(User,
                                     blank=True,
                                     to_field='id',
                                     on_delete=models.PROTECT,
                                     verbose_name='Автор')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Пост активен')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    def clean(self):
        self.text = _clear_text_for_model(self.text)
        self.title = _clear_text_for_model(self.title)
        if not self.text:
            raise ValidationError('Текст статьи не заполнен')
        if not self.title:
            raise ValidationError('Заголовок не заполнен')

    @property
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property
    def geomap_latitude(self):
        return '' if self.lat is None else str(self.lat)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_show", kwargs={"post_slug": self.slug})


class Images(models.Model):
    post = models.ForeignKey(Posts,
                             on_delete=models.CASCADE,
                             null=True)
    image = models.ImageField(upload_to='uploads//%Y/%m/%d/',
                              verbose_name='Фотография')

    tg_id = models.BigIntegerField(blank=True,
                                   null=True,
                                   verbose_name='ID фото на сервере телеграм')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)
        image.save(self.image.path, quality=80, optimize=True)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.image.delete(save=False)



    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['id']


class TgUsers(models.Model):
    tg_id = models.BigIntegerField(unique=True,
                                   verbose_name='ID Telegram')
    tag_settings = models.ManyToManyField(Tags,
                                          blank=True,
                                          verbose_name='Тэги')
    area_settings = models.ManyToManyField(Areas,
                                           blank=True,
                                           verbose_name='Локации')
    viewed_posts = models.ManyToManyField(Posts,
                                          blank=True,
                                          verbose_name='Просмотренные посты')
    lat = models.FloatField(null=True,
                            blank=True,
                            verbose_name='Широта')
    lon = models.FloatField(null=True,
                            blank=True,
                            verbose_name='Долгота')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Пользователь телеграмм'
        verbose_name_plural = 'Пользователи телеграмм'
        ordering = ['id']

    def __str__(self) -> str:
        return str(self.tg_id)
