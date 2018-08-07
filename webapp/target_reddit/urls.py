from django.urls import path

from target_reddit import views

# pylint: disable=invalid-name
urlpatterns = [
    path('get_data/', views.reddit_loader, name='reddit')
]
