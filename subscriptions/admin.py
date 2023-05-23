from django.contrib import admin

from home.utils import render_boolean_icon
from .models import *


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'plan_period_type', 'price', 'apple_product_id', 'grace_period', 'created', 'updated']
    autocomplete_fields = ('upgrade_from_plans',)
    search_fields = ['title', 'plan_period_type', 'apple_product_id', ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'plan', 'plan_period_type', 'price', 'display_is_active', 'display_expired',
                    'display_expired_in_days', 'is_cancelled',
                    'started_at', 'ended_at', 'cancelled_at', 'created', ]
    readonly_fields = ['display_expired', 'display_expired_in_days']

    @admin.display(description='Active')
    def display_is_active(self, instance):
        return render_boolean_icon(instance.is_active)

    @admin.display(description='Expired')
    def display_expired(self, instance):
        from home.utils import render_boolean_icon
        return render_boolean_icon(instance.is_expired)

    @admin.display(description='Expired in')
    def display_expired_in_days(self, instance):
        return f'{instance.get_expired_in_days} days'
