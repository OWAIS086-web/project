from django.urls import path
from . import views

app_name = 'stripe'

urlpatterns = [
    path('payment-methods/', views.PaymentMethodAPIView.as_view(), ),
    path('payment-methods/<int:pk>/', views.PaymentMethodDetailAPIView.as_view(), ),
]
