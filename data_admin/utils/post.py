from random import randint
from geopy.distance import geodesic
from django import http
from data_admin import models


def get_distance(lat_1, lon_1, lat_2, lon_2): 
    # расстояние между двумя точками по географическим координатам
    ret = geodesic((lat_1, lon_1), (lat_2, lon_2)).km
    return ret


def get_post_sorted_by_distance(q, lat, lon):
    #Список отсортированных постов по удаленности от точки
    rate = []
    for item in q:
        dist = get_distance(item.lat, item.lon, lat, lon)
        rate.append({
            'id':item.id,
            'dist': dist
        })
    return sorted(rate, key= lambda x: x['dist'])

def available_posts_for_user(tg_id: int):
    # Доступные посты для пользователя с учетом фильтров
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
        raise http.Http404
    # Возвращаем рандомный пост
    obj = q[randint(0, len(q)-1)]
    return obj


def get_post_by_coordinates(tg_id: int, lat: float, lon: float):
    #возвращает ближайший пост по координатам
    q = available_posts_for_user(tg_id)
    if not q:
        raise http.Http404
    rate = get_post_sorted_by_distance(q, lat, lon)
    id, d = rate.pop(0).values()
    ret = q.filter(id=id).first()
    return ret


