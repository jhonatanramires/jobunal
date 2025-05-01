from pydrive2.auth import GoogleAuth

# Point to wherever you placed your settings file:
gauth = GoogleAuth(settings_file="./config/config.yaml")
gauth.LocalWebserverAuth()
