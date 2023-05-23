from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('plans/', views.SubscriptionPlanListAPIView.as_view(), name='plans'),
    path('plans/<int:pk>/available-upgrade-plans/', views.AvailableUpgradePlanListAPIView.as_view(),name='available_upgrade_plans'),
    path('active/', views.AccountActiveSubScriptionDetailAPIView.as_view(), name='active_subscription'),
    path('cancel/', views.AccountCancelSubScriptionAPIView.as_view(), name='cancel_subscription'),
    path('create/', views.SubscriptionCreateAPIView.as_view(), name='create_subscription'),
    path('upgrade/', views.UpgradeSubscriptionAPIView.as_view(), name='upgrade_subscription'),
    path('calculate-upgrade-price/', views.CalculateUpgradePlanPriceAPIView.as_view(),name='calculate_upgrade_plan_price'),

]
