import logging
import os
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPRecipientsRefused

import requests
from django.conf import settings
from django.template import loader
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


logger = logging.getLogger(__name__)


def send_email(from_, to, subject, html):
    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = from_
    msg["To"] = to

    with SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)
        return True


def send_text(to, text):
    try:
        client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(to=to, from_=settings.TWILIO_NUMBER, body=text)
        if msg.sid is not None:
            return True
    except TwilioRestException:
        logger.exception("Text Error")
        return None


class Alert(ABC):
    def __init__(self, template, reg, close_template=None):
        t = loader.get_template(template)
        self.text = t.render(
            {
                "course": reg.section.full_code,
                "brand": "Penn Course Alert",
                "auto_resubscribe": reg.auto_resubscribe,
            }
        )
        self.close_text = None
        if close_template:
            t = loader.get_template(close_template)
            self.close_text = t.render(
                {
                    "course": reg.section.full_code,
                    "brand": "Penn Course Alert",
                    "auto_resubscribe": reg.auto_resubscribe,
                }
            )
        self.registration = reg

    @abstractmethod
    def send_alert(self, close_notification=False):
        pass


class Email(Alert):
    def __init__(self, reg):
        super().__init__(
            "alert/email_alert.html", reg, close_template="alert/email_close_alert.html"
        )

    def send_alert(self, close_notification=False):
        """
        Returns False if notification was not sent intentionally,
        and None if notification was attempted to be sent but an error occurred.
        """
        if self.registration.user is not None and self.registration.user.profile.email is not None:
            email = self.registration.user.profile.email
        elif self.registration.email is not None:
            email = self.registration.email
        else:
            return False

        try:
            thread_subject = f"{self.registration.section.full_code} is now open!"
            if close_notification:
                if not self.close_text:
                    # This should be unreachable
                    return None
                alert_subject = f"RE: {thread_subject}"
                alert_text = self.close_text
            else:
                alert_subject = thread_subject
                alert_text = self.text
            return send_email(
                from_="Penn Course Alert <team@penncoursealert.com>",
                to=email,
                subject=alert_subject,
                html=alert_text,
            )
        except SMTPRecipientsRefused:
            logger.exception("Email Error")
            return None


class Text(Alert):
    def __init__(self, reg):
        super().__init__("alert/text_alert.txt", reg, close_template="alert/text_alert_close.txt")

    def send_alert(self, close_notification=False):
        """
        Returns False if notification was not sent intentionally,
        and None if notification was attempted to be sent but an error occurred.
        """
        if self.registration.user is not None and self.registration.user.profile.push_notifications:
            # Do not send text if push_notifications is enabled
            return False
        if self.registration.user is not None and self.registration.user.profile.phone is not None:
            phone_number = self.registration.user.profile.phone
        elif self.registration.phone is not None:
            phone_number = self.registration.phone
        else:
            return False

        if close_notification:
            if not self.close_text:
                # This should be unreachable
                return None
            alert_text = self.close_text
        else:
            alert_text = self.text
        return send_text(phone_number, alert_text)


class PushNotification(Alert):
    def __init__(self, reg):
        super().__init__("alert/push_notif.txt", reg, close_template="alert/push_notif_close.txt")

    def send_alert(self, close_notification=False):
        """
        Returns False if notification was not sent intentionally,
        and None if notification was attempted to be sent but an error occurred.
        """
        if self.registration.user is not None and self.registration.user.profile.push_notifications:
            # Only send push notification if push_notifications is enabled
            pennkey = self.registration.user.username
            bearer_token = os.environ.get("MOBILE_NOTIFICATION_SECRET", "")
            if close_notification:
                if not self.close_text:
                    # This should be unreachable
                    return None
                alert_title = f"{self.registration.section.full_code} just closed."
                alert_body = self.close_text
            else:
                alert_title = f"{self.registration.section.full_code} is now open!"
                alert_body = self.text
            try:
                response = requests.post(
                    "https:/api.pennlabs.org/notifications/send/internal",
                    data={"title": alert_title, "body": alert_body, "pennkey": pennkey,},
                    headers={"Authorization": f"Bearer {bearer_token}"},
                )
                if response.status_code != 200:
                    logger.exception(
                        f"Push Notification {response.status_code} Response: {response.content}"
                    )
                    return None
            except requests.exceptions.RequestException as e:
                logger.exception(f"Push Notification Request Error: {e}")
                return None
            return True
        return False
