from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import EmailMessage
import os


@shared_task
def send_email(subject, message, recipient_list, attachments=[]):
    email = EmailMessage(
        subject=subject,
        body=message,
        to=recipient_list,
        attachments=[(attachment, open(attachment, 'rb').read(), 'application/pdf') for attachment in attachments]
    )
    email.send()
    # delete the pdfs
    for attachment in attachments:
        os.remove(attachment)