from __future__ import unicode_literals

import requests


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
        return None

    # TODO: improve error handling
    try:
        result = {'address': response.json()['logradouro'],
                  'neighborhood': response.json()['bairro'],
                  'city': response.json()['cidade'],
                  'state': response.json()['estado'],
                  'zip_code': response.json()['cep']}
    except ValueError:
        return None

    except Exception:
        return None

    return result
