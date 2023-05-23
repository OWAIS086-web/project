from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe

from modules.admin_mixin import AdminMediaMixin
from users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(AdminMediaMixin, auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (('User', {'fields': ('name', 'user_type')}),) + auth_admin.UserAdmin.fieldsets
    list_display = ['display_user_first_column', 'first_name', 'last_name', 'get_country', 'user_type',
                    'get_button_actions',
                    'date_joined']
    search_fields = ['name', 'first_name', 'last_name', 'email']
    list_select_related = ['doctor_profile', 'patient_profile']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_superuser', 'is_staff',
                       'password1', 'password2'),
        }),
    )

    def get_search_results(self, request, queryset, search_term):
        model_name = request.GET.get('model_name', None)
        if model_name == 'doctorprofile':
            queryset, use_distinct = super().get_search_results(request,
                                                                queryset.filter(user_type=User.USER_TYPE_DOCTOR),
                                                                search_term)
            return queryset, use_distinct
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    @admin.display(description='Email', ordering='email')
    def display_user_first_column(self, instance):
        if instance.email:
            return '%s' % instance.email
        return '%s' % instance.username

    @admin.display(description='Country')
    def get_country(self, instance):
        if instance.user_type == User.USER_TYPE_DOCTOR and instance.doctor_profile:
            return instance.doctor_profile.country
        elif instance.user_type == User.USER_TYPE_PATIENT and instance.patient_profile:
            return instance.patient_profile.country
        else:
            return None

    def get_object_by_id(self, object_id):
        try:
            user = User.objects.select_related('doctor_profile').get(id=object_id)
        except User.DoesNotExist:
            user = None
        return user

    @admin.display(description='Actions')
    def get_button_actions(self, instance):
        html = f'<a href="{instance.id}/profile/" class="btn-admin-primary">View</a>'
        return mark_safe(html)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/profile/', self.admin_site.admin_view(self.user_profile_view),
                 name='user_profile_view'),
        ]
        return custom_urls + urls

    def user_profile_view(self, request, object_id):
        user = self.get_object_by_id(object_id=object_id)
        context = dict(

            self.admin_site.each_context(request),
            user=user,
            title=f'{user}',
        )
        return render(request, 'users/admin/user_detail.html', context)
