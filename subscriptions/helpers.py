from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_template_email(
    subject: str, template_name: str, context: dict, recipient: str
) -> str | int:
    """
    Sends an email with HTML template.
    """
    html_content = render_to_string(f"emails/{template_name}.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    email.attach_alternative(html_content, "text/html")

    return email.send(fail_silently=False)
