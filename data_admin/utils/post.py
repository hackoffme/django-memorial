from random import randint
from django import http
from data_admin import models


def available_posts_for_user(tg_id: int):
    # Получаем настройки пользователя
    user_settings = models.TgUsers.objects.filter(tg_id=tg_id ).first()
    # Генерируем фильтры
    filter = {'is_active': True}
    filter_exclude = {}
    if user_settings:
        filter.update({'area__in': user_settings.area_settings.all(),
                       'tag__in': user_settings.tag_settings.all(),
                       })
        filter_exclude.update({'pk__in': user_settings.viewed_posts.all()})
    # Получаем список постов с учетом фильтров и уже просмотренных.
    # Если постов для просмотров нет вызываем исключение
    q = models.Posts.objects.filter(**filter).distinct()
    if not q:
        raise http.Http404
    q = q.exclude(**filter_exclude).distinct()
    return q


def get_rnd_post(tg_id: int):
    q = available_posts_for_user(tg_id)
    if not q:
        return models.Posts()
    # Возвращаем рандомный пост
    obj = q[randint(0, len(q)-1)]
    return obj


def get_post_by_coordinates(tg_id: int, lat: float, lon: float):
    q = available_posts_for_user(tg_id)
    #надо придумать функцию поиска по координатам
    return q.first()


