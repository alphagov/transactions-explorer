import argparse

def parse_args_for_fetch(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--client-secrets',
                        help='Google API client secrets JSON file',
                        default='data/client_secrets.json')
    parser.add_argument('--oauth-tokens',
                        help='Google API OAuth tokens file',
                        default='data/tokens.dat')

    return parser.parse_args(args)


def parse_args_for_create(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--services-data',
                        help='Services CSV datafile',
                        default='data/services.csv')
    parser.add_argument('--path-prefix',
                        help='Prefix for generated URL paths',
                        default='/')

    return parser.parse_args(args)
