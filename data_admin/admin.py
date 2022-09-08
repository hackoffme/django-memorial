from django.contrib import admin, auth
from django_admin_geomap import ModelAdmin
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join
from django.contrib.auth import get_permission_codename

from data_admin.models import Areas, Tags, Images, Posts, TgUsers, SettingsAdmin
# 'title', 'text', 'lat', 'lon', 'area', 'tag', 'current_user'

admin.site.site_header = '«Панель управления проектом»'
admin.site.site_title = '«Админка»'
admin.site.index_title = 'Добро пожаловать! В разделе посты добавляйте новый контент'


class ImagesAdmin(admin.StackedInline):
    model = Images
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=50")


@admin.register(Posts)
class PostsAdmin(ModelAdmin):
    list_display = ('id', 'is_active', 'title',  'area',
                    'created_at', 'updated_at', 'current_user' )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    
    fields = ('title', 'slug', 'text', 'area', 'tag', 'current_user', ('lat', 'lon'))
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
        ##Дополнительная проверка для пользователей состоящих в группе 
        ##имеющих право редактировать только свои посты
        if request.user.groups.filter(name=self.group_for_editing_your_posts).exists():
            if type(obj)==Posts:
                if request.user == obj.current_user:
                    return True
                else:
                    return False
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

        

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj,  change, **kwargs)
        # if change:
        #     for item in form.base_fields:
        #         print(item)
        #         pass
        #     pass
        if not change:
            form.base_fields['current_user'].initial = request.user
            form.base_fields['current_user'].disabled = True
        return form
 
admin.site.register(SettingsAdmin)
admin.site.register(TgUsers)
admin.site.register(Areas)
admin.site.register(Tags)
admin.site.register(Images)

