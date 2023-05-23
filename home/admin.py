from django.contrib import admin

from .admin_forms import PrivacyPolicyAdminForm, TermsAndConditionAdminForm
from .models import *


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    form = PrivacyPolicyAdminForm

    def has_add_permission(self, request):
        return not PrivacyPolicy.objects.exists()


@admin.register(TermsAndCondition)
class TermsAndConditionAdmin(admin.ModelAdmin):
    form = TermsAndConditionAdminForm

    def has_add_permission(self, request):
        return not TermsAndCondition.objects.exists()
# Register your models here.
from .models import *


@admin.register(AppStoreLink)
class AppStoreLinkAdmin(admin.ModelAdmin):
    pass
    def has_add_permission(self, request):
        data_exists = AppStoreLink.objects.exists()
        return not data_exists
