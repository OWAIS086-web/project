"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView
from allauth.account.views import confirm_email
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("", include("home.urls", namespace='home')),
    path("accounts/", include("allauth.urls")),
    path("modules/", include("modules.urls")),
    path("api/v1/", include("home.api.v1.urls")),
    path("api/", include("api_modules.urls", namespace='api')),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('tinymce/', include('tinymce.urls')),

    # path("rest-auth/", include("dj_rest_auth.urls")),
    # Override email confirm to use allauth's HTML view instead of rest_auth's API view
    # path("rest-auth/registration/account-confirm-email/<str:key>/", confirm_email),
    path("accounts/registration/account-confirm-email/<str:key>/", confirm_email),
    # path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path('implant-types/', include('implant_types.urls', namespace='implant_types')),
]

admin.site.site_header = "PDG Innovations"
admin.site.site_title = "PDG Innovations Admin Portal"
admin.site.index_title = "PDG Innovations Admin"

# swagger
api_info = openapi.Info(
    title="PDG Innnovations API",
    default_version="v1",
    description="API documentation for Analog App",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=[permissions.IsAuthenticated, ],
)

urlpatterns += [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs")
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
                       path('__debug__/', include(debug_toolbar.urls)),
                   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path("", TemplateView.as_view(template_name='index.html'))]
urlpatterns += [re_path(r"^(?:.*)/?$",
                        TemplateView.as_view(template_name='index.html'))]
