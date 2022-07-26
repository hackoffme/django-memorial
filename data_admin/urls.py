from django.urls import path
from data_admin import views

urlpatterns = [
    path('', views.PostsView.as_view(), name='home'),
    path('posts/<slug:post_slug>',views.PostShow.as_view(), name='post_show'),
    path('areas/<slug:areas_slug>/', views.PostsViewAreas.as_view(), name='post_areas'),
    path('create/', views.PostsCreate.as_view(), name='post_create'),
    
]
