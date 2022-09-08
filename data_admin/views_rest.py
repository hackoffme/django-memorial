from random import randint
from django import http
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, views, generics, mixins, status, decorators

from data_admin import models
from data_admin import serializers
from data_admin import utils


class PostForTg(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_url_kwarg = 'tg_id'
    serializer_class = serializers.PostForTgSerializers

    def get_object(self):
        # Получаем рандомный пост в соответсвии с настройками пользователя
        # и уже просмотренными
        tg_id = self.kwargs.get(self.lookup_url_kwarg, None)
        if tg_id is None:
            raise http.Http404
        obj = utils.get_rnd_post(tg_id)
        self.check_object_permissions(self.request, obj)
        user_settings = models.TgUsers.objects.filter(tg_id=tg_id).first()
        if user_settings:
            user_settings.viewed_posts.add(obj)
        return obj

    @decorators.action(detail=True, serializer_class=serializers.PostForTgSerializers)
    def get_post_by_coordinates(self, request,  tg_id, **kwargs):
        # метод возвращает пост по координатам пользователя
        point = serializers.PointSerializers(data=request.data)
        if not point.is_valid():
            raise http.Http404
        lat = point.validated_data['lat']
        lon = point.validated_data['lon']
        obj = utils.get_post_by_coordinates(tg_id=tg_id,
                                                 lat=lat,
                                                 lon=lon)
        if not obj:
            raise http.Http404
        user_settings = models.TgUsers.objects.filter(tg_id=tg_id).first()
        if not user_settings:
            user_settings = utils.create_user_by_id(tg_id=tg_id)
        user_settings.lat = lat
        user_settings.lon = lon
        user_settings.viewed_posts.add(obj)
        user_settings.save()
        return Response(self.get_serializer(obj).data)

    @decorators.action(detail=True)
    def get_post_by_saved_coordinates(self, request, tg_id, *args, **kwargs):
        user_settings = models.TgUsers.objects.filter(tg_id=tg_id).first()
        if not user_settings:
            raise http.Http404
        obj = utils.get_post_by_coordinates(tg_id, user_settings.lat, user_settings.lon)
        user_settings.viewed_posts.add(obj)
        return Response(self.get_serializer(obj).data)


class UserTg(viewsets.ModelViewSet):
    queryset = models.TgUsers.objects.all()
    serializer_class = serializers.TgUsersSerializers
    lookup_field = 'tg_id'

    def create(self, request, **kwargs):
        try:
            tg_id = int(request.data['tg_id'])
        except ValueError:
            raise http.Http404
        except KeyError:
            raise http.Http404
        tg_user = models.TgUsers.objects.filter(tg_id=tg_id).first()
        if tg_user:
            ret = serializers.TgUsersSerializers(tg_user)
            return Response(ret, status=200)

        # tg_user = models.TgUsers(tg_id=tg_id)
        # tg_user.save()
        # tg_user.tag_settings.set(models.Tags.objects.all())
        # tg_user.area_settings.set(models.Areas.objects.all())
        tg_user = utils.create_user_by_id(tg_id=tg_id)
        ret = serializers.TgUsersSerializers(tg_user)
        return Response(ret.data, status=201)


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
