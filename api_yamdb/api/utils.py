import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from reviews.models import User

from api_yamdb.settings import NOREPLY_YAMDB_EMAIL


def confirmation_creater(username):
    user = get_object_or_404(User, username=username)
    subject = 'Код подтверждения для YaMDB'
    confirmation_code = ''.join(
        [random.choice(settings.EMAIL_BACKEND) for x in range(15)]
    )
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        subject,
        confirmation_code,
        NOREPLY_YAMDB_EMAIL,
        [user.email],
        fail_silently=False
    )
