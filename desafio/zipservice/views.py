from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def health_check(request):
    """
    webservice app health health check
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
        return HttpResponse(status=201,
                            content="OK - POST - zip: %s" % zip_code)


@api_view(['DELETE'])
def delete_zipcode(request, zip_code=None):
    """
    success return: 204
    error return: 
    """

    return HttpResponse(status=204,
                        content="OK - DELETE - zip: %s" % zip_code)
