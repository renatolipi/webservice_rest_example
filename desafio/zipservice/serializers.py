from __future__ import unicode_literals

from rest_framework import serializers
from zipservice.models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('address', 'neighborhood', 'city', 'state', 'zip_code')
