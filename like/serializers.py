from rest_framework import serializers
from data_admin import models as da_models
from like import models

class Vote(serializers.ModelSerializer):
    tg_user = serializers.SlugRelatedField(slug_field='tg_id', queryset=da_models.TgUsers.objects)
    
    class Meta:
        model = models.Vote
        fields = ['post', 'tg_user', 'like']