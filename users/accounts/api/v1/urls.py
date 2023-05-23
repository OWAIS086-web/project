from dj_rest_auth.registration.views import (VerifyEmailView, ResendEmailVerificationView)
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views, viewsets
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView, UserDetailsView,
)

router = DefaultRouter()
# router.register("signup", viewsets.SignupViewSet, basename="signup")
# router.register("login", viewsets.LoginViewSet, basename="login")

app_name = 'accounts'

urlpatterns = [
    # path("", include(router.urls)),
    path('login/token/', views.AccountTokenLoginAPIView.as_view(), name='token_login'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    # path("", include("dj_rest_auth.urls")),
    path('profile/', views.AccountAuthProfileDetalAPIView.as_view(), name='profile'),
    path('delete/', views.AccountDeleteAPIView.as_view(), name='delete_account'),

    # path("registration/", include("dj_rest_auth.registration.urls")),
    path('registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('registration/resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path(
        r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email',
    ),
    path(
        'registration/account-email-verification-sent/', TemplateView.as_view(),
        name='account_email_verification_sent',
    ),
    #path('registration/doctor/', views.DoctorRegistrationAPIView.as_view(), name='doctor_registration'),
    path('verify-email-exists/', views.VerfiyEmailExistAPIView.as_view(), )
]
