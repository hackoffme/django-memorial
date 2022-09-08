from django.db import models
from tinymce import models as models_tinymce
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django_admin_geomap import GeoItem
import bleach


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
                             verbose_name='Район поиска')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

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
                             unique=True,
                             verbose_name='Тэги')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

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
