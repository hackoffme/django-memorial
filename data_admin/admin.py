from django.contrib import admin, auth
from django_admin_geomap import ModelAdmin as Model_Admin_Geomap
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join
from django.contrib.auth import get_permission_codename
from django.db.models import Count, Q

from data_admin.models import Areas, Tags, Images, Posts, TgUsers, SettingsAdmin

from like.models import Vote
# 'title', 'text', 'lat', 'lon', 'area', 'tag', 'current_user'

admin.site.site_header = '«Панель управления проектом»'
admin.site.site_title = '«Админка»'
admin.site.index_title = 'Добро пожаловать! В разделе посты добавляйте новый контент'
admin.site.disable_action('delete_selected')

class ImagesAdmin(admin.StackedInline):
    model = Images
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=50")


@admin.register(Posts)
class PostsAdmin(Model_Admin_Geomap):
    #list
    list_display = ('id', 'is_active' , 'likes','likes_up','likes_down', 'title',  'area',
                    'created_at', 'updated_at', 'current_user' )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    list_per_page = 10
    
    #details
    fields = ('title', 'slug', 'text', 'area', 'tag', 'current_user', 'is_active', ('lat', 'lon'))
    readonly_fields = ('current_user',)
    # ordering = ('rating',)
    prepopulated_fields = {"slug": ("title",)}

    # filter_horizontal = ('tag',)
    #inlines
    inlines = [ImagesAdmin]
    
    #geomap
    geomap_default_longitude =  "37.70503313373094"
    geomap_default_latitude = "55.78124553340503"
    geomap_default_zoom = "12"
    geomap_item_zoom = "14"
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"
    geomap_height = "300px"
    
    #permission
    group_for_editing_your_posts='contributor'
    def get_queryset(self, request):
        q = super().get_queryset(request)\
                    .annotate(likes=Count('vote'))\
                    .annotate(up = Count('vote', filter=Q(vote__like=True)))\
                    .annotate(down = Count('vote', filter=Q(vote__like=False)))
        return q
    
    def likes(self, obj):
        return obj.likes
    likes.admin_order_field = 'likes'
    likes.short_description = 'Итого'
    
    def likes_up(self, obj):
        return obj.up
    likes_up.admin_order_field = 'up'
    likes_up.short_description = '👍'
    
    def likes_down(self, obj):
        return obj.down
    likes_down.admin_order_field = 'down'
    likes_down.short_description = '👎🏾'   
    
    # def rating(self, obj):
    #     ret = Vote.objects.filter(post=obj).count()
    #     return ret
    # rating.short_description = 'Рейтинг'
    
    
    
    def has_change_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename("change", opts)
        ##Права contributor. Запрещаем редактировать не свои посты
        if request.user.groups.filter(name=self.group_for_editing_your_posts).exists():
            if type(obj)==Posts:
                if request.user == obj.current_user:
                    return True
                else:
                    return False
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))
    

    def save_model(self, request, obj, form, change):
        #При создании прикрепляем текущего пользователя
        #Права contributor. Пост после изменения становится неактивным
        if not change:
            obj.current_user = request.user
        if request.user.groups.filter(name=self.group_for_editing_your_posts).exists():
            obj.is_active = False
        obj.save()


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            for item in TgUsers.objects.all():
                item.tag_settings.add(obj)


@admin.register(Areas)
class AreasAdmin(admin.ModelAdmin):
    fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            for item in TgUsers.objects.all():
                item.area_settings.add(obj)   


admin.site.register(SettingsAdmin)
admin.site.register(TgUsers)
admin.site.register(Images)

