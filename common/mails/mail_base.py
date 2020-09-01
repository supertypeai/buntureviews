from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings


class EmailHandler:
    def __init__(self, subject, mail_body, to_mail):
        self.from_mail = settings.EMAIL_HOST_USER
        self.mail_subject = subject
        self.mail_body = mail_body
        self.to_mail = to_mail

    def user_password_reset_email(self):
        try:
            # plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
            subject = render_to_string("mails/password_reset_sub.txt", self.mail_body)
            text_body = render_to_string(
                "mails/password_reset_body.txt", self.mail_body
            )
            html_body = render_to_string(
                "mails/user_password_reset.html", self.mail_body
            )
            # send_mail(self.mail_subject, message, self.from_mail, self.to_mail)
            msg = EmailMultiAlternatives(
                subject=self.mail_subject,
                from_email=self.from_mail,
                to=self.to_mail,
                body=text_body,
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            return True
        except:
            return False

    def customer_login_email(self):
        try:
            # plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
            subject = render_to_string("mails/message_subject.txt", self.mail_body)
            text_body = render_to_string("mails/message_body.txt", self.mail_body)
            html_body = render_to_string(
                "mails/customer_login_mail.html", self.mail_body
            )
            # send_mail(self.mail_subject, message, self.from_mail, self.to_mail)
            msg = EmailMultiAlternatives(
                subject=self.mail_subject,
                from_email=self.from_mail,
                to=self.to_mail,
                body=text_body,
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            return True
        except:
            return False
