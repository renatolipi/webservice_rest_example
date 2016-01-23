from __future__ import unicode_literals

from django.db import models


class Address(models.Model):
    """
        We could improve on DB, but let's keep it simple (KISS)
    """
    zip_code = models.CharField(max_length=9, primary_key=True)
    address = models.CharField(max_length=150)
    neighborhood = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=100)
