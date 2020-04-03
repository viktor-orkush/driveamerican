from django.urls import path
from core.views import robots_txt, sitemap_xml

urlpatterns = [
    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap_xml),
]
