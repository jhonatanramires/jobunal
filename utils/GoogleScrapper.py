import json
import gspread
from gspread.utils import extract_id_from_url
from gspread.auth import local_server_flow, get_config_dir, oauth, oauth_from_dict

import json
from pathlib import Path
from typing import Union

import gspread
from gspread.auth import local_server_flow, get_config_dir, oauth

class Scraper:
    def __init__(self, config_path: Union[str, Path]):
        # Load configuration
        with open(config_path) as config_file:
            self.config = json.load(config_file)

        # Determine credential paths
        credentials_filename = (
            self.config['g_credentials_path'] or 
            str(get_config_dir() / 'credentials.json')
        )
        
        authorized_user_filename = (
            self.config['g_authorized_user_path'] or 
            str(get_config_dir() / 'authorized_user.json')
        )

        # Define custom flow with fixed port
        def fixed_port_flow(client_config, scopes):
            return local_server_flow(
                client_config,
                scopes,
                port=53067  # Your fixed port
            )

        # Create and store the client instance
        self.client = oauth(
            scopes=self.config['scopes'],
            flow=fixed_port_flow,
            credentials_filename=credentials_filename,
            authorized_user_filename=authorized_user_filename
        )

    def __getattr__(self, name):
      return getattr(self.client, name)

    def get_jobs(self):
        # Open the spreadsheet using its URL
        sheet = self.open_by_url(
            "https://docs.google.com/spreadsheets/d/1H6f8HPDEU102Vzvpy4nxtl3qfKPA3QSnpxew_s54Ars/edit"
        )
        
        # Fetch full grid data from the first sheet
        metadata = sheet.fetch_sheet_metadata(params={"includeGridData": True})
        
        links = []
        # Iterate over all sheets in the metadata (usually one)
        for sheet_info in metadata.get("sheets", []):
            for grid in sheet_info.get("data", []):
                for row in grid.get("rowData", []):
                    # Ensure the row has at least 4 columns (Column D is index 3)
                    if "values" in row and len(row["values"]) > 3:
                        cell = row["values"][3]  # Column D
                        # Check if the cell directly has a hyperlink
                        if "hyperlink" in cell:
                            links.append(cell["hyperlink"])
                        # If not, check if there are rich text runs with hyperlinks
                        elif "textFormatRuns" in cell:
                            for run in cell["textFormatRuns"]:
                                if "format" in run and "link" in run["format"]:
                                    uri = run["format"]["link"].get("uri")
                                    if uri:
                                        links.append(uri)
        print(links)
        return links
    
    def download_pdfs(self):
      # Implement your PDF downloading logic here
      list_of_dicts = self.get_jobs()
      print(len(list_of_dicts))
      for job in list_of_dicts:
        print(job)  
      pass

    
getter = Scraper("./config.json")

jobs = getter.download_pdfs()

# Open your spreadsheet by title
