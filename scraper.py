import json
from pathlib import Path
from typing import Union
from gspread.utils import extract_id_from_url, ExportFormat
from gspread.auth import oauth
from utils.google import cred_auth_paths, fixed_port_flow
import openpyxl

class Scraper:
    def __init__(self, config_path: Union[str, Path]):
        # Load configuration
        with open(config_path) as config_file:
            self.config = json.load(config_file)

        # Determine credential and token paths
        self.credentials_filename, self.authorized_user_filename = cred_auth_paths(config_path)

        # Create and store the client instance
        self.client = oauth(
            scopes=self.config['scopes'],
            flow=fixed_port_flow,
            credentials_filename=self.credentials_filename,
            authorized_user_filename=self.authorized_user_filename
        )

    def __getattr__(self, name):
      return getattr(self.client, name)
    
    def get_desc_link(self,file_path, sheet_name=None):
      # Load the workbook
      workbook = openpyxl.load_workbook(file_path)
      
      # Select the active sheet or a specific sheet
      if sheet_name:
          sheet = workbook[sheet_name]
      else:
          sheet = workbook.active
      
      links = []
      
      # Iterate through all cells in column D (column index 4)
      for row in sheet.iter_rows(min_col=4, max_col=4):
          for cell in row:
              # Check if the cell has a hyperlink
              if cell.hyperlink:
                  links.append(cell.hyperlink.target)
              # Check if the cell contains a plain text URL
              elif isinstance(cell.value, str) and cell.value.startswith(('http://', 'https://')):
                  links.append(cell.value)
      
      return links
  
    def get_links(self,link):
      response = self.export(extract_id_from_url(link), ExportFormat.EXCEL)
      # Save the content to a local file
      with open('exported_spreadsheet.xlsx', 'wb') as f:
          f.write(response)
      list_of_links = self.get_desc_link('exported_spreadsheet.xlsx')
      print(f"Found {len(list_of_links)} links:")
      for link in list_of_links:
          print(link)
      pass
    

if __name__ == "__main__":
  scraper = Scraper("./config/config.json")
  scraper.get_links("https://docs.google.com/spreadsheets/d/1H6f8HPDEU102Vzvpy4nxtl3qfKPA3QSnpxew_s54Ars/edit?gid=351433209#gid=351433209")