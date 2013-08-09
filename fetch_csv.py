#!/usr/bin/env python

import httplib2
import os
import sys
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
from lib.params import parse_args_for_fetch
from lib.filesystem import create_directory

arguments = parse_args_for_fetch(sys.argv[1:])

SPREADSHEET = '0AiLXeWvTKFmBdFpxdEdHUWJCYnVMS0lnUHJDelFVc0E'
SERVICES_SHEET = '44'
SERVICES_DATA_OUTPUT = 'data/services.csv'
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

%s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), arguments.client_secrets)


flow = flow_from_clientsecrets(
    arguments.client_secrets,
    scope='https://docs.google.com/feeds/ https://docs.googleusercontent.com/ https://spreadsheets.google.com/feeds/',
    message=MISSING_CLIENT_SECRETS_MESSAGE,
)
storage = Storage(arguments.oauth_tokens)
credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, storage)

http = httplib2.Http()
http = credentials.authorize(http)

service = build("drive", "v2", http=http)
spreadsheet = service.files().get(fileId=SPREADSHEET).execute()
download_url = spreadsheet.get('exportLinks')['application/pdf']
download_url = download_url[:-4] + "=csv"

resp, content = service._http.request(download_url + "&gid=" + SERVICES_SHEET)

create_directory(os.path.dirname(SERVICES_DATA_OUTPUT))
csvFile = open(SERVICES_DATA_OUTPUT, 'w')
csvFile.write(content)
csvFile.close()
