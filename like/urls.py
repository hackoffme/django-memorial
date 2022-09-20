from django.urls import path


from like import views
urlpatterns = [
    path('api/v1/vote/', views.Vote.as_view()),
]