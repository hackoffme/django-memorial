from data_admin import models
def create_user_by_id(tg_id: int) -> models.TgUsers:
        tg_user = models.TgUsers(tg_id=tg_id)
        tg_user.save()
        tg_user.tag_settings.set(models.Tags.objects.all())
        tg_user.area_settings.set(models.Areas.objects.all())
        return tg_user