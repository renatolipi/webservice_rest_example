from __future__ import unicode_literals

import logging
import requests

logger = logging.getLogger(__name__)

POSTMON_ZIPCODE_URL = 'http://api.postmon.com.br/v1/cep/'


def get_address_from_zipcode(zipcode):
    """
    Given a zipcode, get address from EXTERNAL API
    """
    # TODO: these next 2 lines should be replaced by RegEx
    zipcode = str(zipcode)
    zipcode = zipcode.strip().replace("-", "")

    response = requests.get('%s%s' % (POSTMON_ZIPCODE_URL, zipcode))

    if response.status_code == 404:
        logger.debug("Zipcode not found on Postmon")
        return None

    # TODO: improve error handling
    try:
        result = {'address': response.json()['logradouro'],
                  'neighborhood': response.json()['bairro'],
                  'city': response.json()['cidade'],
                  'state': response.json()['estado'],
                  'zip_code': response.json()['cep']}
    except ValueError as error:
        logger.error("ValueError: %s" % error.message)
        return None

    except Exception as error:
        logger.error("General Exception: %s" % error.message)
        return None

    return result
