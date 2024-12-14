import os
import requests
from bs4 import BeautifulSoup

# Base URL of the directory containing the year folders
BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02171/Eastern_Arctic/"
DOWNLOAD_DIR = "data"  # Directory to save the downloaded files

# Create the download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_file(file_url, download_dir):
    """Download a single file from the given URL."""
    local_filename = os.path.join(download_dir, file_url.split("/")[-1])
    with requests.get(file_url, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {local_filename}")

def scrape_folder(folder_url):
    """Scrape a year folder for December .tar files."""
    response = requests.get(folder_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links in the year folder
    links = soup.find_all('a', href=True)

    # Filter for December files (YYYYMMDD where MM = 12)
    december_files = [
        link['href'] for link in links 
        if link['href'].endswith('.tar') and len(link['href']) >= 20 and link['href'][16:18] == "12" 
        and 18 <= int(link['href'][18:20]) <= 25
    ]

    return december_files

def scrape_and_download(base_url, download_dir):
    """Scrape the base URL for year folders, then download December files."""
    response = requests.get(base_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links to year folders (assume links ending with "/")
    year_folders = [link['href'] for link in soup.find_all('a', href=True) if link['href'].strip('/').isdigit()]

    print(f"Found {len(year_folders)} year folders.")

    # Iterate through each year folder
    for year_folder in year_folders:
        year_url = base_url + year_folder
        print(f"Checking folder: {year_url}")
        
        # Get December files from the year folder
        december_files = scrape_folder(year_url)
        
        # Download each December file
        for file_name in december_files:
            full_url = year_url + file_name
            download_file(full_url, download_dir)

# Run the script
if __name__ == "__main__":
    scrape_and_download(BASE_URL, DOWNLOAD_DIR)