import argparse
from lib import filters


def _create_parser():
    return argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)


def parse_args_for_fetch(args):
    parser = _create_parser()
    parser.add_argument('--client-secrets',
                        help='Google API client secrets JSON file',
                        default='data/client_secrets.json')
    parser.add_argument('--oauth-tokens',
                        help='Google API OAuth tokens file',
                        default='data/tokens.dat')

    return parser.parse_args(args)


def parse_args_for_create(args):
    parser = _create_parser()
    parser.add_argument('--services-data',
                        help='Services CSV datafile',
                        default='data/services.csv')
    parser.add_argument('--path-prefix',
                        help='Prefix for generated URL paths',
                        default=filters.path_prefix)
    parser.add_argument('--asset-prefix',
                        help='Prefix for generated asset URLs',
                        default=filters.asset_prefix)

    return parser.parse_args(args)
