from django.urls import path, include
from django.contrib import admin

# pylint: disable=invalid-name
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('habr/', include('target_habr.urls'), name='habr'),
    path('reddit/', include('target_reddit.urls'), name='reddit'),
]
