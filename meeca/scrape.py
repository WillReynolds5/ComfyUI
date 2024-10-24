import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import os

# Define a user-agent string
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def scrape_album_images(url, download=False):
    image_links = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        gallery_list = soup.find('ul', class_='list-gallery')
        
        if not gallery_list:
            print(f"Warning: No gallery list found for {url}")
            return image_links
            
        for li in gallery_list.find_all('li'):
            try:
                a_tag = li.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    high_quality_link = a_tag['href']
                    if is_valid_url(high_quality_link):
                        image_links.append(high_quality_link)
                        if download:
                            try:
                                os.makedirs('images', exist_ok=True)
                                image_response = requests.get(high_quality_link, headers=HEADERS, timeout=10)
                                image_response.raise_for_status()
                                
                                image_name = os.path.join('images', os.path.basename(high_quality_link))
                                with open(image_name, 'wb') as f:
                                    f.write(image_response.content)
                            except (requests.RequestException, OSError) as e:
                                print(f"Error downloading image {high_quality_link}: {e}")
                                continue
            except Exception as e:
                print(f"Error processing gallery item: {e}")
                continue
                
    except requests.RequestException as e:
        print(f"Error scraping album {url}: {e}")
    except Exception as e:
        print(f"Unexpected error scraping album {url}: {e}")
    return image_links


def scrape_albums(url, albums_per_model=None, download=False):
    album_data = {}
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        album_list = soup.find('ul', class_='list-gallery has-mobile-menu')
        if album_list:
            albums_scraped = 0
            for li in album_list.find_all('li'):
                if albums_per_model is not None and albums_scraped >= albums_per_model:
                    break
                a_tag = li.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    href = a_tag['href']
                    if not is_valid_url(href):
                        href = urljoin(url, href)
                    if is_valid_url(href):
                        if href == url or base not in href or '/models/' in href:
                            continue
                        print(f"Scraping images from album: {href}")
                        image_links = scrape_album_images(href, download)
                        album_data[href] = image_links
                        albums_scraped += 1
                        time.sleep(1)  # Delay between album image scrapes
    except requests.RequestException as e:
        print(f"Error scraping model page {url}: {e}")
    return album_data


def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_data(data, filename):
    try:
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # Atomic rename to prevent corruption
        os.replace(temp_filename, filename)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")
        # Try to remove temporary file if it exists
        try:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        except:
            pass


def scrape_website(base_url, max_pages=100, models_per_page=None, albums_per_model=None, download=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scraped_data_{timestamp}.json"
    
    all_data = {}
    page_number = 1
    consecutive_errors = 0
    max_consecutive_errors = 3

    while page_number <= max_pages:
        try:
            # Construct the proper URL for the current page
            current_url = f"{base_url}?page={page_number}" if page_number > 1 else base_url
            
            response = requests.get(current_url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            gallery_list = soup.find('ul', class_='list-gallery v1')

            if gallery_list:
                list_items = gallery_list.find_all('li')

                if not list_items:
                    print(f"No more items found on page {page_number}. Stopping.")
                    break

                models_scraped = 0
                for item in list_items:
                    if models_per_page is not None and models_scraped >= models_per_page:
                        break

                    a_tag = item.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        href = a_tag['href']
                        if not is_valid_url(href):
                            href = urljoin(base_url, href)
                        if is_valid_url(href):
                            if href not in all_data:
                                print(f"Scraping albums from: {href}")
                                album_data = scrape_albums(href, albums_per_model, download)
                                all_data[href] = album_data
                                save_data(all_data, filename)  # Save after each model
                                models_scraped += 1
                                time.sleep(1)  # Delay between model page scrapes
                            else:
                                print(f"Skipping already scraped model: {href}")

                if models_per_page is not None and models_scraped < models_per_page:
                    print(f"Only found {models_scraped} new models on page {page_number}. Moving to next page.")
            else:
                print(f"Couldn't find the specified ul element on page {page_number}. Stopping.")
                break
        except requests.RequestException as e:
            print(f"Error scraping page {page_number}: {e}")
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                print(f"Too many consecutive errors ({max_consecutive_errors}). Stopping.")
                break
            time.sleep(5)  # Wait longer after an error
            continue
        except Exception as e:
            print(f"Unexpected error on page {page_number}: {e}")
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                print(f"Too many consecutive errors ({max_consecutive_errors}). Stopping.")
                break
            continue

        page_number += 1
        time.sleep(1)  # Delay between main page scrapes

    return all_data


# Usage
base = "https://www.femjoyhunter.com"
base_url = f"{base}/models"
max_pages = 100
models_per_page = 99
albums_per_model = 100  # New parameter to limit albums per model
download_images = True  # Set to True to download images

scraped_data = scrape_website(base_url, max_pages=max_pages, models_per_page=models_per_page, albums_per_model=albums_per_model, download=download_images)

# Print summary statistics
print("\nSummary Statistics:")
print(f"Total models scraped: {len(scraped_data)}")
print(f"Total albums scraped: {sum(len(albums) for albums in scraped_data.values())}")
print(f"Total images scraped: {sum(sum(len(images) for images in albums.values()) for albums in scraped_data.values())}")
print(f"Pages scraped: {min(max_pages, len(scraped_data) // (models_per_page or len(scraped_data)))}")
