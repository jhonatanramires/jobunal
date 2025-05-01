import requests
import json
import urllib.parse
from gspread import oauth
from gspread.auth import local_server_flow, get_config_dir

with open("config.json") as config_file:
  config = json.load(config_file)

credentials_filename = (
    config.get('g_credentials_path') or 
    str(get_config_dir() / 'credentials.json')
)

authorized_user_filename = (
    config.get('g_authorized_user_path') or 
    str(get_config_dir() / 'authorized_user.json')
)

def fixed_port_flow(client_config, scopes):
    return local_server_flow(
        client_config,
        scopes,
        port=53067  # Your fixed port
    )

client = oauth(
            scopes=config['scopes'],
            flow=fixed_port_flow,
            credentials_filename=credentials_filename,
            authorized_user_filename=authorized_user_filename
        )

sht2 = client.open_by_url('docs.google.com/spreadsheets/d/1H6f8HPDEU102Vzvpy4nxtl3qfKPA3QSnpxew_s54Ars/edit?gid=351433209#gid=351433209')

import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

# Authenticate and create an authorized session
creds = Credentials.from_authorized_user_file(authorized_user_filename, scopes=config['scopes'])
authed_session = AuthorizedSession(creds)

# Specify the file ID of the Google Spreadsheet
file_id = '1H6f8HPDEU102Vzvpy4nxtl3qfKPA3QSnpxew_s54Ars'

# Define the export URL for XLSX format
export_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

# Make the request to export the file
response = authed_session.get(export_url)

# Save the content to a local file
with open('exported_spreadsheet.xlsx', 'wb') as f:
    f.write(response.content)
