from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from driveamerican import settings
from driveamericanapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
