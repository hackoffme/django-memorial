from django.db import models
from django.urls import reverse

from data_admin import models as da_models

class Vote(models.Model):
    post = models.ForeignKey(da_models.Posts, 
                             on_delete=models.CASCADE, 
                             verbose_name='Пост')
    tg_user = models.ForeignKey(da_models.TgUsers, 
                                to_field='tg_id',
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                verbose_name='Пользователь телеграмм')
    like = models.BooleanField(verbose_name='like')
    
    

    class Meta:
        verbose_name = ("Лайк поста")
        verbose_name_plural = ("Лайки постов")

    def __str__(self):
        return f'Лайк поста {self.post.title}, от пользователя {self.tg_user.tg_id}'

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
