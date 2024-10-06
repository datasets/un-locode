"""
This script is used to generate the alias code list from the UN/LOCODE data.
It uses BeautifulSoup to scrape the UN/LOCODE website and download the zip file containing the data.
The reason behind this because UN/LOCODE data is constantly updated and the file name changes with each update.
"""

import os
import io
import re
import csv
import chardet
import zipfile
import requests
import pycountry
import pandas as pd

from functools import reduce
from bs4 import BeautifulSoup

extract_path = 'data/'
output_file = 'data/merged.csv'
merged_files = 'data/merged_data.csv'
subdivision_file = 'data/subdivision-codes.csv'
country_file = 'data/country-codes.csv'

def extract_txt_files(zip_file_path, extract_path, value):
    response = requests.get(zip_file_path)
    z = zipfile.ZipFile(io.BytesIO(response.content))
    directory = []
    with z as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.csv') and value in file_info.filename.lower():
                zip_ref.extract(file_info, extract_path)
                directory.append(file_info.filename)
    return directory


def get_zip_source_path(source_path):
    response = requests.get(source_path)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=True):
        # Check if the file is a zip file and contains 'loc' and 'txt' in the name
        if link.get('href').endswith('.zip') and all(substring in link.get('href') for substring in ['loc', 'csv']):
            return link.get('href')

def merge_csv_files(directory):
    header_to_remove = ['Change', 'Country', 'Location', 'Name', 'NameWoDiacritics', 'Subdivision', 'Status', 'Function', 'Date', 'IATA', 'Coordinates', 'Remarks']
    # List to store each DataFrame
    dfs = []

    # Loop over all files in the directory
    for filename in directory:
        # Read each CSV file and append the DataFrame to the list
        df = pd.read_csv(filename, encoding='latin1')
        if df.iloc[0].tolist() == header_to_remove:
            # Drop the first row (which contains the unwanted header)
            df = df.drop(0).reset_index(drop=True)
        
        # If this is the first file, save the column names
        if 'column_names' not in locals():
            column_names = header_to_remove
        
        # Assign column names to the DataFrame
        df.columns = column_names
        
        # Append the DataFrame to the list
        dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file, index=False)

def remove_special_chars(csv_file, output_file):
    charset = chardet.detect(open(csv_file, 'rb').read())['encoding']
    with open(csv_file, 'r', encoding=charset) as infile:
        reader = csv.reader(infile)
        with open(subdivision_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow([re.sub(r'[^\x00-\x7F]+', '', cell) for cell in row])

def download_file(url, file_path):
    print(file_path)
    response = requests.get(url)
    

def process():
    print('Processing UN/LOCODE data')
    source_path = 'https://unece.org/trade/cefact/UNLOCODE-Download'
    zip_source_path = get_zip_source_path(source_path)
    print(f'Downloading {zip_source_path}')
    directory_codelist = extract_txt_files(zip_source_path, extract_path,'codelist')
    directory_codelist = [os.path.join(extract_path, file) for file in directory_codelist]
    directory_subdivision = extract_txt_files(zip_source_path, extract_path,'subdivision')
    merge_csv_files(directory_codelist)
    print('Merging CSV files')
    for fname in directory_codelist:
        if 'codelist' in fname.lower():
            code_list = pd.read_csv(output_file, encoding='utf-8')
            code_list = code_list.astype(object) 
            code_list.fillna('', inplace=True)
            code_list.to_csv('data/code-list.csv', index=False)
            index_list = []
            for i,v in code_list['Name'].items():
                if '=' in v:
                    index_list.append(i)
            alias_temp = code_list.iloc[index_list]
            alias = alias_temp[['Country', 'Name', 'NameWoDiacritics']]
            alias.to_csv('data/alias.csv', index=False)
    print('Extracting subdivision data')
    if 'subdivision' in directory_subdivision[0].lower():
        header_subdiv = ['SUCountry', 'SUCode', 'SUName', 'SUType']
        remove_special_chars(extract_path+directory_subdivision[0], subdivision_file)
        subdivision = pd.read_csv(subdivision_file, encoding='utf-8', names=header_subdiv)
        subdivision = subdivision.astype(object) 
        subdivision.fillna('', inplace=True)
        subdivision.to_csv('data/subdivision.csv', index=False)
    print('Generating country codes')
    
    country_list = subdivision['SUCountry'].unique().tolist()
    country_pycountry = [
        pycountry.countries.get(alpha_2=code).name if pycountry.countries.get(alpha_2=code) else None
        for code in country_list
    ]
    dct = {
        'CountryCode': country_list,
        'CountryName': country_pycountry
    }
    country_df = pd.DataFrame(dct)
    country_df.to_csv(country_file, index=False)
    print('Cleaning up')
    for fname in directory_codelist:
        os.remove(fname)
    os.remove(extract_path+directory_subdivision[0])
    os.remove(output_file)
    os.remove(merged_files)
    print('Done')

if __name__ == '__main__':
    process()

