from django.contrib import admin, auth
from django_admin_geomap import ModelAdmin as Model_Admin_Geomap
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join
from django.contrib.auth import get_permission_codename

from data_admin.models import Areas, Tags, Images, Posts, TgUsers, SettingsAdmin
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
    # actions = []
    list_display = ('id', 'is_active', 'title',  'area',
                    'created_at', 'updated_at', 'current_user' )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    
    fields = ('title', 'slug', 'text', 'area', 'tag', 'current_user', 'is_active', ('lat', 'lon'))
    readonly_fields = ('current_user',)
    prepopulated_fields = {"slug": ("title",)}

    # filter_horizontal = ('tag',)
    inlines = [ImagesAdmin]
    list_per_page = 10
    geomap_default_longitude =  "37.70503313373094"
    geomap_default_latitude = "55.78124553340503"
    geomap_default_zoom = "12"
    geomap_item_zoom = "14"
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"
    geomap_height = "300px"
    
    group_for_editing_your_posts='contributor'

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

