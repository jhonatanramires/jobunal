from gspread.auth import get_config_dir
from typing import Union
from pathlib import Path
from gspread.auth import local_server_flow
import json

def cred_auth_paths(config_path: Union[str, Path]):
  # Determine credential paths
  with open(config_path) as config_file:
    config = json.load(config_file)
  credentials_filename = (
    config.get('g_credentials_path') or 
    str(get_config_dir() / 'credentials.json')
  )
  
  authorized_user_filename = (
      config.get('g_authorized_user_path') or 
      str(get_config_dir() / 'authorized_user.json')
  )
  return credentials_filename, authorized_user_filename

# Define custom flow with fixed port
def fixed_port_flow(client_config, scopes):
  return local_server_flow(
      client_config,
      scopes,
      port=53067  # Your fixed port
  )