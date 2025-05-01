import openpyxl

def get_links_from_column_d(file_path, sheet_name=None):
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

# Example usage
file_path = 'exported_spreadsheet.xlsx'
links = get_links_from_column_d(file_path)

# Print the extracted links
for idx, link in enumerate(links, 1):
    print(f"Link {idx}: {link}")