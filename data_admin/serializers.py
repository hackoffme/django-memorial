from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from data_admin import models


class PostForTgSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Posts
        exclude = ['id', 'is_active', 'created_at', 'updated_at', 'current_user' ]

class TgUsersSerializers(serializers.ModelSerializer):
    tag_settings = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=models.Tags.objects)
    area_settings = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=models.Areas.objects)
    # viewed_posts = serializers

    class Meta:
        model = models.TgUsers
        fields = ['tg_id', 'tag_settings', 'area_settings', 'viewed_posts']


class SettingsAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.SettingsAdmin
        fields = '__all__'

class PointSerializers(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
