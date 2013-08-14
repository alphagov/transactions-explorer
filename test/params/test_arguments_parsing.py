import unittest
from hamcrest import *
from lib.params import parse_args_for_fetch, parse_args_for_create


class FetchArgumentParsing(unittest.TestCase):

    def test_default_secret_and_token_to_data_dir(self):
        argument = parse_args_for_fetch([])

        assert_that(argument.client_secrets, is_('data/client_secrets.json'))
        assert_that(argument.oauth_tokens, is_('data/tokens.dat'))

    def test_parse_secret_and_token_params(self):
        argument = parse_args_for_fetch(['--client-secrets',
                                         '/var/google/secrets.json',
                                         '--oauth-tokens',
                                         '/var/google/token.dat'])

        assert_that(argument.client_secrets, is_('/var/google/secrets.json'))
        assert_that(argument.oauth_tokens, is_('/var/google/token.dat'))



class CreateArgumentParsing(unittest.TestCase):

    def test_default_services_data_file_and_prefix_on_data_dir(self):
        argument = parse_args_for_create([])

        assert_that(argument.services_data, is_('data/services.csv'))
        assert_that(argument.path_prefix, is_('/'))

    def test_parse_services_data_param(self):
        argument = parse_args_for_create(['--services-data', '/var/test.csv'])

        assert_that(argument.services_data, is_('/var/test.csv'))

    def test_parse_path_prefix_parma(self):
        argument = parse_args_for_create(['--path-prefix', '/some/path'])

        assert_that(argument.path_prefix, is_('/some/path'))
