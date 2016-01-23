from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from zipservice import postmon_tool as pt
from zipservice.serializers import AddressSerializer


@api_view(['GET'])
def health_check(request):
    """
    webservice app health check
    TODO: improve
    """
    return HttpResponse(status=200,
                        content="OK")


@api_view(['GET', 'POST'])
def handle_zipcode(request, zip_code=None):
    """
    GET success return: 200
    POST success return: 201
    """

    if request.method == 'GET':
        return HttpResponse(status=200,
                            content="OK - GET - zip: %s" % zip_code)

    if request.method == 'POST':

        zip_code = request.data.get('zip_code')
        # TODO: zip_code = _validate_zip_code(zip_code)
        if not zip_code:
            return HttpResponse(status=404,
                                content="ERROR - POST - zip: %s NOT VALID ZIPCODE" % zip_code)

        json_zipcode = pt.get_address_from_zipcode(zip_code)

        serializer = AddressSerializer(data=json_zipcode)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_zipcode(request, zip_code=None):
    """
    success return: 204
    error return: 
    """

    return HttpResponse(status=204,
                        content="OK - DELETE - zip: %s" % zip_code)
