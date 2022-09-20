from os import stat
from turtle import down
from rest_framework.views import APIView
from rest_framework.response import Response
from like import serializers
from like import models as like_models


class Vote(APIView):
    def post(self, request, **kwargs):
        data = serializers.Vote(data=request.data)
        if not data.is_valid():
            return Response({'status': 422})

        like = like_models.Vote.objects.filter(
            tg_user=request.data['tg_user'], post=request.data['post']).first()

        if not like:
            data.save()
            status = 201
        else:
            if like.like != request.data['like']:
                like.delete()
                status = 205
            else:
                status = 208
        posts = like_models.Vote.objects.filter(post=request.data['post'])
        up = posts.filter(like=True).count() 
        down = posts.filter(like=False).count() 
        ret = Response({'count_up': up, 'count_down': down}, status=status)
        return ret
