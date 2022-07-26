from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join

from data_admin.models import Areas, Tags, Images, Posts, TgUsers
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
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'title',  'area',
                    'created_at', 'updated_at', 'current_user',
                    )
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'text')
    
    fields = ('title', 'slug', 'text', 'area', ('lat', 'lon'), 'tag', 'current_user')
    readonly_fields = ('maps',)
    prepopulated_fields = {"slug": ("title",)}

    filter_horizontal = ('tag',)
    inlines = [ImagesAdmin]

    @admin.display(description='Карта')
    def maps(self, object):
        return None
        # return mark_safe(f'<a href="https://yandex.ru/maps/?rtext=~{object.lat}%2C{object.lon}">Построить маршрут</a>')
        # return mark_safe(f"<div style='width: 300px; height: 200px;'> <script type='text/javascript' charset='utf-8' src='https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3A053bd947d462cc1a45aeba4070defff75501905071c0eaf68436ac9976ec698c&amp;width=514&amp;height=326&amp;lang=ru_RU&amp;apikey=<API-ключ>'></script></div>")


admin.site.register(TgUsers)
admin.site.register(Areas)
admin.site.register(Tags)
admin.site.register(Images)
