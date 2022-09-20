from dataclasses import fields
import bleach
from rest_framework import serializers
from data_admin import models

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = '__all__'

class PostForTgSerializers(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    images_set = ImageSerializers(many=True)
    def get_text(self, obj):
        text = obj.text
        text = bleach.clean(obj.text, tags=['bold', 'strong', 'i', 'em', 'code', 's', 'strike', 'del', 'u',  'br'], strip=True)
        text = text.replace('<br>', '\n')
        return text
    class Meta:
        model = models.Posts
        exclude = ['is_active', 'created_at', 'updated_at', 'current_user' ]
        # depth =1 



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
