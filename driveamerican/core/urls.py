from django.urls import path
from core.views import robots_txt

urlpatterns = [
    path("robots.txt", robots_txt),
]
