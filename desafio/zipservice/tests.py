from __future__ import unicode_literals

import mock

from django.test import TestCase
from django.test import Client

from zipservice.models import Address


def _postmon_tools_mocked_return_none(zip_code):
    return None


def _postmon_tools_mocked_return_values(zip_code):
    return {'address': 'test street',
            'neighborhood': 'test neighborhood',
            'city': 'test city',
            'state': 'test state',
            'zip_code': '12345678'}


class ZipserviceGetTests(TestCase):

    def setUp(self):
        self.address1 = Address()
        self.address1.zip_code = '12345000'
        self.address1.address = 'Spam and Eggs street'
        self.address1.neighborhood = 'Flying Circus'
        self.address1.city = 'Xpto'
        self.address1.state = 'AC'
        self.address1.save()

        self.address2 = Address()
        self.address2.zip_code = '12345999'
        self.address2.address = 'Spam and Eggs avenue'
        self.address2.neighborhood = 'Swimming Circus'
        self.address2.city = 'Foobar'
        self.address2.state = 'RO'
        self.address2.save()

    def tearDown(self):
        self.address = Address.objects.all()
        self.address.delete()

    # SUCCESS scenarios

    def test_health_check(self):
        client = Client()
        response = client.get('/health/')

        self.assertEqual(response.status_code, 200)

    def test_get_all_addresses(self):
        client = Client()

        response = client.get('/zipcode/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_limited_addresses(self):
        client = Client()

        response = client.get('/zipcode/?limit=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # ERROR scenarios

    def test_get_addresses_with_wrong_query_string(self):
        client = Client()

        response = client.get('/zipcode/?state=sp')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid query filter', response.content)

    def test_get_addresses_with_one_extra_query_string(self):
        client = Client()

        response = client.get('/zipcode/?limit=1&state=sp')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid query filter', response.content)

    def test_get_addresses_with_wrong_query_string_value(self):
        client = Client()

        response = client.get('/zipcode/?limit=char')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid query filter value', response.content)


class ZipservicePostTests(TestCase):

    def tearDown(self):
        self.address = Address.objects.all()
        self.address.delete()

    # SUCCESS scenarios

    @mock.patch("zipservice.postmon_tool.get_address_from_zipcode", _postmon_tools_mocked_return_values)
    def test_input_address_given_a_correct_zipcode(self):
        client = Client()

        response = client.get('/zipcode/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        client = Client()

        response2 = client.post('/zipcode/', {'zip_code': '14020260'})

        self.assertEqual(response2.status_code, 201)

        response3 = client.get('/zipcode/')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 1)

    # ERROR scenarios

    @mock.patch("zipservice.postmon_tool.get_address_from_zipcode", _postmon_tools_mocked_return_values)
    def test_input_address_given_a_valid_zipcode_twice(self):
        client = Client()

        response = client.get('/zipcode/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        response2 = client.post('/zipcode/', {'zip_code': '14020260'})

        self.assertEqual(response2.status_code, 201)

        response2 = client.get('/zipcode/')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 1)

        response3 = client.post('/zipcode/', {'zip_code': '14020260'})

        self.assertEqual(response3.status_code, 400)

        response4 = client.get('/zipcode/')
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(len(response4.data), 1)


    @mock.patch("zipservice.postmon_tool.get_address_from_zipcode", _postmon_tools_mocked_return_none)
    def test_input_address_given_an_invalid_zipcode(self):
        client = Client()

        response = client.get('/zipcode/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        response2 = client.post('/zipcode/', {'zip_code': '140202'})

        self.assertEqual(response2.status_code, 404)

        response3 = client.get('/zipcode/')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 0)

    def test_post_missing_zipcode(self):
        client = Client()

        response = client.get('/zipcode/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        response2 = client.post('/zipcode/')

        self.assertEqual(response2.status_code, 400)
        self.assertIn('Zip code missing', response2.content)

        response3 = client.get('/zipcode/')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 0)

    # TODO: implement this scenario
    # def test_input_address_error_while_saving(self):
    #     pass

    @mock.patch("zipservice.postmon_tool.get_address_from_zipcode", _postmon_tools_mocked_return_none)
    def test_input_address_when_zipcode_not_found(self):
        client = Client()

        response = client.get('/zipcode/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        response2 = client.post('/zipcode/', {'zip_code': '13730999'})

        self.assertEqual(response2.status_code, 404)

        response3 = client.get('/zipcode/')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 0)


class ZipserviceDeleteTests(TestCase):

    def setUp(self):
        self.address1 = Address()
        self.address1.zip_code = '12345000'
        self.address1.address = 'Spam and Eggs street'
        self.address1.neighborhood = 'Flying Circus'
        self.address1.city = 'Xpto'
        self.address1.state = 'AC'
        self.address1.save()

        self.address2 = Address()
        self.address2.zip_code = '12345999'
        self.address2.address = 'Spam and Eggs avenue'
        self.address2.neighborhood = 'Swimming Circus'
        self.address2.city = 'Foobar'
        self.address2.state = 'RO'
        self.address2.save()

    def tearDown(self):
        self.address = Address.objects.all()
        self.address.delete()

    # SUCCESS scenarios

    def test_delete_existing_address(self):
        client = Client()

        response = client.get('/zipcode/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response2 = client.delete('/zipcode/12345999/')

        self.assertEqual(response2.status_code, 204)

        response3 = client.get('/zipcode/')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 1)

    # ERROR scenarios

    def test_delete_inexistent_zipcode(self):
        client = Client()

        response = client.get('/zipcode/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response2 = client.delete('/zipcode/99999000/')

        self.assertEqual(response2.status_code, 404)
        self.assertIn('Zip code not found', response2.content)

        response3 = client.get('/zipcode/')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 2)
