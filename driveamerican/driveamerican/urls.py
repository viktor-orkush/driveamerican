from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from driveamerican import settings
from driveamericanapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('customs/', views.customs, name='customs'),
    path('calculation/', views.calculation, name='calculation'),
    path('faq/', views.faq, name='faq'),
    path('blog/', include('blogapp.urls')),

    # api urls
    path('calculate_customs/', views.CalculateCustomsAPI.as_view(), name='calculate_customs'),
    path('calculate_all_payments/', views.CalculateAllPaymentsAPI.as_view(), name='calculate_all_payments')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
