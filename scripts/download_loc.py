import cloudscraper

from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

source_path = "https://unece.org/trade/cefact/UNLOCODE-Download"

def get_zip_source_path(source_path):
    response = scraper.get(source_path)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        # Check if the file is a zip file and contains 'loc' and 'txt' in the name
        if link.get('href').endswith('.zip') and \
        (all(substring in link.get('href') for substring in ['loc', 'mdb'])) or \
        (all(substring in link.get('href') for substring in ['loc', 'csv'])):
            links.append(link.get('href'))
    return links


def download_zip(url):
    r = scraper.get(url)
    file_name = url.split('/')[-1]
    open(file_name, 'wb').write(r.content)


def process():
    print("Downloading UNLOCODE files")
    zip_source_path = get_zip_source_path(source_path)
    
    for elem in zip_source_path:
        download_zip(elem)
        print(f"Downloaded {elem}")
    print("Downloaded UNLOCODE files")
    
if __name__ == '__main__':
    process()