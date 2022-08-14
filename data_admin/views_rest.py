from ast import Raise
from random import randint
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, views, generics, mixins, status

from data_admin import models
from data_admin import serializers


class PostForTg(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_url_kwarg = 'tg_id'
    serializer_class = serializers.PostForTgSerializers

    def get_object(self):
        assert self.lookup_url_kwarg in self.kwargs
        # Получаем настройки пользователя
        user_settgins = models.TgUsers.objects.filter(
            tg_id=self.kwargs[self.lookup_url_kwarg]).first()
        # Генерируем фильтры
        filter = {'is_active': True}
        filter_exclude = {}
        if user_settgins:
            filter.update({'area__in': user_settgins.area_settings.all(),
                           'tag__in': user_settgins.tag_settings.all(),
                           })
            filter_exclude.update({'pk__in': user_settgins.viewed_posts.all()})
        # Получаем список постов с учетом фильтров и уже просмотренных.
        # Если постов для просмотров нет вызываем исключение
        q = models.Posts.objects.filter(**filter).distinct()
        if not q:
            raise Http404
        q = q.exclude(**filter_exclude).distinct()
        if not q:
            return models.Posts()
        # Возвращаем рандомный пост
        obj = q[randint(0, len(q)-1)]
        self.check_object_permissions(self.request, obj)
        if user_settgins:
            user_settgins.viewed_posts.add(obj)
        return obj


class UserTg(viewsets.ModelViewSet):
    queryset = models.TgUsers.objects.all()
    serializer_class = serializers.TgUsersSerializers
    lookup_field = 'tg_id'


class Area(views.APIView):
    def get(self, request):
        ret = models.Areas.objects.all().values()
        return Response(ret)


class Tag(views.APIView):
    def get(self, request):
        ret = models.Tags.objects.all().values()
        return Response(ret)


class SettingsAdmin(generics.ListAPIView):
    queryset = models.SettingsAdmin.objects.all()
    serializer_class = serializers.SettingsAdminSerializers


class UserTgSettings(views.APIView):
    def get(self, request, tg_id):
        user = models.TgUsers.objects.filter(tg_id=tg_id).first()
        if user is None:
            ret = [{'slug': item.slug, 'title': item.title}
                   for item in models.Areas.objects.all()]
            return Response(ret)
        ret = [{'slug': item.slug, 'title': item.title}
               for item in user.area_settings.all()]
        return Response(ret)

    def post(self, request, tg_id):
        serializer = serializers.TgUsersSerializers(data=request.data)
        user = models.TgUsers.objects.filter(tg_id=tg_id).first()
        return Response(status=201)
