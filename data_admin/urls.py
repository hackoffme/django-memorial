from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from data_admin import views
from data_admin import views_rest

router = DefaultRouter()
router.register(r'tg_users', views_rest.UserTg)
urlpatterns = [
    path('', views.PostsView.as_view(), name='home'),
    path('posts/<slug:post_slug>',views.PostShow.as_view(), name='post_show'),
    path('areas/<slug:areas_slug>/', views.PostsViewAreas.as_view(), name='post_areas'),
    path('create/', views.PostsCreate.as_view(), name='post_create'),

    path('api/v1/', include((router.urls, 'rest_api'),namespace='api')),
    path('api/v1/settings', views_rest.SettingsAdmin.as_view()),
    path('api/v1/settings/areas/<int:tg_id>', views_rest.UserTgSettings.as_view()),
    path('api/v1/settings/areas/', views_rest.Area.as_view()),
    path('api/v1/settings/tags/', views_rest.Tag.as_view()),
    path('api/v1/post/<int:tg_id>/', views_rest.PostForTg.as_view({'get':'retrieve'})),
    path('api/v1/post/<int:tg_id>/get_post_by_coordinates/', views_rest.PostForTg.as_view({'get':'get_post_by_coordinates'})),
    path('api/v1/post/<int:tg_id>/get_post_by_saved_coordinates/', views_rest.PostForTg.as_view({'get':'get_post_by_saved_coordinates'})),
]
