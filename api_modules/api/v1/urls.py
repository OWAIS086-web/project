from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('', include('home.api.v1.urls', namespace='home')),
    path('users/', include('users.api.v1.urls', namespace='users')),
    path('onesignal/', include('onesignal_app.api.v1.urls', namespace='onesignal')),
    path('subscriptions/', include('subscriptions.api.v1.urls', namespace='subscriptions')),
    path('stripe/', include('stripe_app.api.v1.urls', namespace='stripe')),
    path('accounts/', include('users.accounts.api.v1.urls', namespace='accounts')),
""" path('doctors/', include('doctors.api.v1.urls', namespace='doctors')),
    path('patients/', include('patients.api.v1.urls', namespace='patients')),
    path('notifications/', include('notifications.api.v1.urls', namespace='notifications')),
    path('feedbacks/', include('feedbacks.api.v1.urls', namespace='feedbacks')),
    path('implant-types/', include('implant_types.api.v1.urls', namespace='implant_types')),
    path('implants/', include('implants.api.v1.urls', namespace='implants')),
    path('payments/', include('payments.api.v1.urls', namespace='payments')),  """
] 
