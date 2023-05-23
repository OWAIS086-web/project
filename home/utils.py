from django.template.loader import render_to_string, get_template
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe


def render_boolean_icon(status):
    if status:
        icon = static('admin/img/icon-yes.svg')
        html = f'<img src="{icon}" alt="{status}">'
        return mark_safe(html)

    icon = static('admin/img/icon-no.svg')
    html = f'<img src="{icon}" alt="{status}">'
    return mark_safe(html)


def send_app_invitation_email(email, current_site, request):
    subject = 'PDG Innovations - Download our APP'
    app_link_android = None
    app_link_ios = None
    http_protocol = 'http://'
    if request.is_secure():
        http_protocol = 'https://'

    from home.models import AppStoreLink
    try:
        app_store_links = AppStoreLink.objects.first()

    except AppStoreLink.DoesNotExist:
        app_store_links = None

    if app_store_links:
        app_link_android = app_store_links.google_play_store_link
        app_link_ios = app_store_links.apple_store_link

    gs_bucket_name = settings.GS_BUCKET_NAME

    context = {
        'subject': subject,
        'current_site': current_site,
        'gs_bucket_name': gs_bucket_name,
        'request': request,
        'http_protocol': http_protocol,
        'app_link_android': app_link_android,
        'app_link_ios': app_link_ios,
    }

    from_email = f'PDG Innovations <{settings.DEFAULT_FROM_EMAIL}>'
    reply_email = 'noreply@pdginnovation.com'
    # html_message = render_to_string('home/email/app_invitation_link.html', context)
    message = get_template('home/email/app_invitation_link.html').render(context)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        reply_to=[reply_email],
        to=[email],
    )
    mail.content_subtype = "html"
    # return send_mail(
    #     subject=subject,
    #     message=html_message,
    #     from_email=from_email,
    #     recipient_list=[email]
    # )
    return mail.send()
