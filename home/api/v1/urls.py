from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views, viewsets

router = DefaultRouter()
app_name = 'home'

urlpatterns = [
    path("", include(router.urls)),
    path('send-app-link/', views.SendEmailInvitationAPIView.as_view()),
    path('app-store-links/', views.AppStoreLinkAPIView.as_view()),
    path('db/', views.DBUrlTest.as_view()),
]
