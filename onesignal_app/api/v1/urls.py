from django.urls import path

from . import views, viewsets

app_name = 'onesignal'

urlpatterns = [
    path('devices/', views.OneSignalDeviceListAPIView.as_view()),
    path('devices/<int:pk>/', views.OneSignalDeviceDetailAPIView.as_view()),
]
