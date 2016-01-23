from __future__ import unicode_literals

from django.db import models


class Address(models.Model):
    """
        We could improve on DB, but let's keep it simple (KISS)
    """
    street = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=9)
