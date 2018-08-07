from django.urls import path

from target_habr import views

# pylint: disable=invalid-name
urlpatterns = [
    path('get_data/', views.habr_loader, name='reddit')
]
