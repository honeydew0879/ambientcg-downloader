import requests
import os
import time
import random
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the base URL of the website
base_url = 'https://ambientcg.com'

# Define the URL of the website list
list_url = urljoin(base_url, '/list')

# Define the parameters for the list URL
list_params = {
    'sort': 'Popular',
    'limit': '180',
    'include': 'displayData,dimensionsData,imageData',
    'offset': '0'
}

#Define user agent
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}

# Define the download directory
download_dir = 'downloads'

# Create the download directory if it doesn't already exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Define a function to download a file given its URL and save it to the specified directory
def download_file(url, dir):
    # Extract the the base name from the link
    filename = url.split('=')[1].split('_')[0]
    # Sets the filename for the zip file
    filename = filename.replace('/', '_') + '.zip'

    # Create the full file path
    file_path = os.path.join(dir, filename)

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f'{filename} already exists, skipping')
        return

    # Download the file
    print(str(i) + f'. Downloading {filename}...')
    response = requests.get(url, headers=HEADERS)
    with open(file_path, 'wb') as f:
        f.write(response.content)
        
   # Add a random delay between 1 and 5 seconds before the next download
    delay = random.randint(1, 5)
    for remaining in range(delay, 0, -1):
        print(f"Waiting {remaining} seconds", end='\r')
        time.sleep(1)
    print(" " * len(f"Waiting {delay} seconds"), end='\r')
    
        

# Open a user-specified number of links
try:
    num_links_to_download = int(input("How many textures do you want to download? (Enter 0 to download all available) "))
except:
    num_links_to_download = 0

if num_links_to_download == 0:
    num_links_to_download = float("inf")  # Set to infinity to download all available

# Scrape links from all pages of the website list
offset = int(list_params['offset'])
page = 1
while True:

    print("page: " + str(page))
    # Add the offset parameter to the list URL parameters
    list_params['offset'] = str(offset)

    # Make a request to the list URL with the parameters and get the HTML content
    list_response = requests.get(list_url, params=list_params)
    list_html_content = list_response.content

    # Create a BeautifulSoup object from the HTML content of the list page
    list_soup = BeautifulSoup(list_html_content, 'html.parser')

    # Find all the links with class "AssetBox"
    links = list_soup.find_all('div', {'class': 'AssetBox'})

    # Download the user-specified number of links from the current page
    for i in range(min(num_links_to_download, len(links))):
        link = urljoin(base_url, links[i].a.get('href'))
        zipfile = link.split("=")[1].split("_")[0]
        download_url = f'{base_url}/get?file={zipfile}_1K-JPG.zip'
        download_file(download_url, download_dir)

    # If downloaded enough links, stop iterating over pages
    num_links_to_download -= len(links)
    if num_links_to_download <= 0:
        break

    # If there are no more links on the current page, stop iterating over pages
    if len(links) == 0:
        break

    # Increment the offset to get the next page
    offset += 180
    page += 1
    
