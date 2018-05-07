from unittest2 import TestCase
from src.generator import split_filter, get_template_keys_from_string, generate_cmdb_param_names, \
    generate_template_with_secrets, extract_data
from jinja2 import Template
from src.APIException import Exception_400
from flask import request
from app import app


class GeneratorTests(TestCase):
    def test_split_filter(self):
        self.assertEqual(split_filter("I|like|apple", '|'), ["I", "like", "apple"])

    def test_split_filter_wrong_delimiter(self):
        self.assertEqual(split_filter("I|like|apple", ','), ["I|like|apple"])

    def test_split_filter_with_None(self):
        self.assertEqual(split_filter(None, '|'), None)

    def test_generate_cmdb_param_names_with_prefix(self):
        template_keys = ["postgres_user", "my__product_my__service__id"]
        prefix = "client/staging"
        expected_keys = {
            "postgres_user": "/client/staging/postgres/user",
            "my__product_my__service__id": "/client/staging/my-product/my-service-id"
        }

        self.assertEqual(generate_cmdb_param_names(template_keys, prefix), expected_keys)

    def test_generate_cmdb_param_names_without_prefix(self):
        template_keys = ["postgres_user", "my__product_my__service__id"]
        prefix = None
        expected_keys = {
            "postgres_user": "/postgres/user",
            "my__product_my__service__id": "/my-product/my-service-id"
        }

        self.assertEqual(generate_cmdb_param_names(template_keys, prefix), expected_keys)

    def test_get_template_keys_from_string(self):
        template_string = '''
            "host" : "{{ postgres_host__0123456789 }}",
            {{ my__product_my__service__id }}
            "host" : {{ rds_host|split(',') }}
        '''
        expected_keys = ["postgres_host__0123456789", "my__product_my__service__id", "rds_host"]

        self.assertEqual(get_template_keys_from_string(template_string), expected_keys)

    def test_generate_template_with_secrets(self):
        template_without_secret = '''
            "postgres_host" : "{{ postgres_host }}",
            {{ my__product_my__service__id }}
        '''
        template = Template(template_without_secret)

        secret_dict = {
            "postgres_host": "postgres_secret_host",
            "my__product_my__service__id": "another_secret",
        }

        expected_template_with_secrets = '''
            "postgres_host" : "postgres_secret_host",
            another_secret
        '''

        self.assertEqual(generate_template_with_secrets(template, secret_dict), expected_template_with_secrets)

    def test_extract_data_with_body_and_prefix(self):
        expected_extracted_data = {"data": '{"foo": "bar"}', "parameters": {"key_prefix": "client/env"}}

        with app.test_request_context("/generate-conf?key_prefix=client/env",
                                      method='POST',
                                      data='{"foo": "bar"}',
                                      headers={"Content-Type": "application/json"}):
            data = extract_data(request)
            self.assertEqual(data, expected_extracted_data)

    def test_extract_data_with_body_and_no_prefix(self):
        expected_extracted_data = {"data": '{"foo": "bar"}', "parameters": {"key_prefix": None}}

        with app.test_request_context("/generate-conf",
                                      method='POST',
                                      data='{"foo": "bar"}',
                                      headers={"Content-Type": "application/json"}):
            data = extract_data(request)
            self.assertEqual(data, expected_extracted_data)

    def test_extract_data_with_no_body_and_prefix(self):
        with app.test_request_context("/generate-conf",
                                      method='POST',
                                      headers={"Content-Type": "application/json"}):
            with self.assertRaises(Exception_400) as context:
                extract_data(request)
                self.assertTrue('request body is missing', context.api_message)

    def test_extract_data_with_no_body_and_no_prefix(self):
        with app.test_request_context("/generate-conf",
                                      method='POST',
                                      headers={"Content-Type": "application/json"}):
            with self.assertRaises(Exception_400) as context:
                extract_data(request)
                self.assertTrue('request body is missing', context.api_message)
