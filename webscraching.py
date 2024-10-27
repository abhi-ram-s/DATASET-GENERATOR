import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_wikipedia_data(url):
    # Send a request to the Wikipedia page
    response = requests.get(url)
    response.raise_for_status()  # Check if request was successful
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text content
    paragraphs = soup.find_all('p')
    text_content = ''
    for paragraph in paragraphs:
        text_content += paragraph.get_text() + '\n'
    
    # Display the full extracted text content
    print("Full Text Content Extracted:\n")
    print(text_content)
    
    # Save text content to CSV with line numbers
    lines = text_content.splitlines()
    text_df = pd.DataFrame(lines, columns=["Text"])
    text_df.index += 1  # Start index from 1 for line numbers
    text_df.to_csv("wikipedia_text_data.csv", index_label="Line Number")
    print("\nText content saved to 'wikipedia_text_data.csv'")
    
    # Extract table data
    tables = soup.find_all('table', {'class': 'wikitable'})
    table_data = []
    
    for table in tables:
        headers = []
        rows = []
        
        # Extract headers from the table
        header_row = table.find('tr')
        for th in header_row.find_all('th'):
            headers.append(th.get_text(strip=True))
        
        # Extract rows from the table
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            rows.append(row_data)
        
        # Convert the extracted data into a pandas DataFrame
        if headers and rows:
            df = pd.DataFrame(rows, columns=headers)
            table_data.append(df)
            print("\nExtracted Table:")
            print(df.head())  # Display the first few rows of the table
    
    return text_content, table_data

# Example usage
url = "https://en.wikipedia.org/wiki/Artificial_intelligence"  # Replace with any Wikipedia URL
text_content, table_data = extract_wikipedia_data(url) 

