from django.urls import path
from . import views, viewsets

app_name = 'users'

urlpatterns = [
    # path('check-exist-user-email/', views.CheckUserExistByEmailAPIView.as_view(), name='check_exist_user_email'),
]
