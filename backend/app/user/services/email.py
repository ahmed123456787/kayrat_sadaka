from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ..token_password import create_deep_link

def send_password_reset_email(user):
    deep_link = create_deep_link(user)
    print("user is", user.first_name,user.last_name)
    subject = "Set Your Password"
    html_message = render_to_string("../templates/email_password.html", {
        "user": user,
        "deep_link": deep_link,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        "noreply@yourdomain.com",
        ["zaterahmed62@gmail.com"],
        html_message=html_message,
    )