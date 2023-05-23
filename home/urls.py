from django.urls import path
from .views import home, page_privacy_policy, page_terms_and_condition

app_name = 'home'

urlpatterns = [
    # path("", home, name="home"),
    path('privacy-policy/', page_privacy_policy, name='page_privacy_policy'),
    path('terms-and-conditions/', page_terms_and_condition, name='page_terms_and_condition'),
]
