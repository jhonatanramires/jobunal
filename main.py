import os
from scraper import Scraper
def get_config_path():
  config_path_relative = input("Enter the path to the config file (default: config.json): ")
  if not config_path_relative:
      config_path_relative = 'config.json'
  config_path = os.path.abspath(config_path_relative)
  print(f"Using config file: {config_path}")
  return config_path

def main():
  print("Hello from jobunal!")
  # Get the config path
  config_path = get_config_path()
  # Initialize the scraper
  scraper = Scraper(config_path)
  # Get the link to download
  link = input("Enter the link of the excel to get the links: ")
  # Get links to the PDFs from the link
  scraper.get_links(link)


if __name__ == "__main__":
    main()
