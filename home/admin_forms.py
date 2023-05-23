from django import forms
from tinymce.widgets import TinyMCE

from home.models import PrivacyPolicy, TermsAndCondition


class PrivacyPolicyAdminForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = PrivacyPolicy
        fields = '__all__'


class TermsAndConditionAdminForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = TermsAndCondition
        fields = '__all__'
