from __future__ import unicode_literals

import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from zipservice import postmon_tool as pt
from zipservice.models import Address
from zipservice.serializers import AddressSerializer

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request):
    """
    webservice app health check
    TODO: improve
    """
    return Response("OK",
                    status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def handle_zipcode(request, zip_code=None):
    """
    GET success return: 200
    POST success return: 201
    """
    if request.method == 'GET':
        if len(request.query_params) == 1 and request.query_params.get('limit'):
            try:
                limit = int(request.query_params.get('limit'))
            except Exception:
                logger.debug("Invalid query filter value: %s" % request.query_params)
                return Response("Invalid query filter value",
                                status=status.HTTP_400_BAD_REQUEST)

        elif len(request.query_params) == 0:
            limit = 0

        else:
            logger.debug("Invalid query filter: %s" % request.query_params)
            return Response("Invalid query filter",
                            status=status.HTTP_400_BAD_REQUEST)

        if limit:
            addresses = Address.objects.all()[:limit]
        else:
            addresses = Address.objects.all()

        serializer = AddressSerializer(addresses, many=True)
        logger.debug("GET Address - OK (200)")
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    if request.method == 'POST':

        zip_code = request.data.get('zip_code')
        if not zip_code:
            logger.debug("Zip code missing (post parameter)")
            return Response("Zip code missing",
                            status=status.HTTP_400_BAD_REQUEST)

        json_zipcode = pt.get_address_from_zipcode(zip_code)

        if json_zipcode:
            serializer = AddressSerializer(data=json_zipcode)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning("Error while saving: %s" % serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Zip code not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_zipcode(request, zip_code):
    """
    success return: 204
    """
    try:
        address = Address.objects.get(zip_code=zip_code)
    except Address.DoesNotExist:
        logger.debug("zip code not found: %s" % zip_code)
        return Response("Zip code not found",
                        status=status.HTTP_404_NOT_FOUND)

    address.delete()
    return Response("Zip code deleted from database",
                    status=status.HTTP_204_NO_CONTENT)
