from django.shortcuts import render

from home.models import PrivacyPolicy, TermsAndCondition


def home(request):
    packages = [
        {'name': 'django-allauth', 'url': 'https://pypi.org/project/django-allauth/0.38.0/'},
        {'name': 'django-bootstrap4', 'url': 'https://pypi.org/project/django-bootstrap4/0.0.7/'},
        {'name': 'djangorestframework', 'url': 'https://pypi.org/project/djangorestframework/3.9.0/'},
    ]
    context = {
        'packages': packages
    }
    return render(request, 'home/index.html', context)


def page_privacy_policy(request):
    page = PrivacyPolicy.objects.first()
    data = {
        'head_title': 'Privacy Policy | PDG Innovations',
        'page': page
    }
    return render(request, 'home/privacy_policy.html', data)


def page_terms_and_condition(request):
    page = TermsAndCondition.objects.first()
    data = {
        'head_title': 'Terms & Conditions | PDG Innovations',
        'page': page
    }
    return render(request, 'home/terms_and_conditions.html', data)
