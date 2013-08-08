import unittest
from hamcrest import *
from lib.params import parse_args


class test_arguments_parsing(unittest.TestCase):

    def test_default_secret_and_token_to_data_dir(self):
        argument = parse_args([])

        assert_that(argument.client_secrets, is_('data/client_secrets.json'))
        assert_that(argument.oauth_tokens, is_('data/tokens.dat'))

    def test_parse_secret_and_token_params(self):
        argument = parse_args(['--client-secrets', '/var/google/secrets.json',
                              '--oauth-tokens', '/var/google/token.dat'])

        assert_that(argument.client_secrets, is_('/var/google/secrets.json'))
        assert_that(argument.oauth_tokens, is_('/var/google/token.dat'))
