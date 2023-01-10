from django.urls import path, include

from .views import WebScraping


urlpatterns = [
    path('get_app_data/', WebScraping.as_view(), name='Home'),
]
