import os
import re
from tempfile import NamedTemporaryFile

import requests
from django.core.files import File

from member.models import MyUser


class GmailBackend():
    def authenticate(self, gmail_address, extra_fields=None):

        defaults = {
            'first_name': extra_fields.get('given_name', ''),
            'last_name': extra_fields.get('family_name', ''),
        }
        user, user_created = MyUser.objects.get_or_create(
            username=gmail_address,
            defaults=defaults,

        )

        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
