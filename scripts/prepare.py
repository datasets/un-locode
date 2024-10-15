import os
import re
import sys
import zipfile
import pandas as pd

from titlecase import titlecase

def process(extracted_files):

    # Process CSV files
    codelist_df = pd.DataFrame(columns=['Change', 'Country', 'Location', 'Name', 'NameWoDiacritics', 'Subdivision',
                        'Function', 'Status', 'Date', 'IATA', 'Coordinates', 'Remarks'])
    codelist_list = []
    #country_df = pd.DataFrame(columns=['CountryCode', 'CountryName'])
    alias_df = pd.DataFrame(columns=['Country', 'Name', 'NameWoDiacritics'])

    for file_name in extracted_files:
        if file_name.endswith('.csv'):
            if 'SubdivisionCodes' in file_name:
                ## Skip SubdivisionCodes.csv file getting source from mdb file instead
                continue

            unlocode_df = pd.read_csv(file_name, encoding='cp1252', header=None, dtype=str)
            unlocode_df.columns = ['Change', 'Country', 'Location', 'Name', 'NameWoDiacritics', 'Subdivision',
                        'Function', 'Status', 'Date', 'IATA', 'Coordinates', 'Remarks']

            for index, row in unlocode_df.iterrows():
                if pd.isna(row['Location']) or row['Location'] == '':
                    if row['Change'] == '=': #alias row
                        alias_df.loc[len(alias_df.index)] = row[['Country', 'Name', 'NameWoDiacritics']]
                    #else: #country name row
                    #    row['Name'] = str(row['Name']).replace('.', '')
                    #    row['Name'] = titlecase(row['Name'])
                    #    country_df.loc[len(country_df.index)] = row[['Country', 'Name']]
                    continue
                #codelist_df.loc[len(codelist_df)] = row
                codelist_list.append(row)
            print(f"Processed {file_name}")

    # Save the merged DataFrame back to a CSV file
    codelist_df  = pd.DataFrame(codelist_list) #)=pd.concat(codelist_list)
    codelist_df = codelist_df.reindex(columns=['Change', 'Country', 'Location', 'Name', 'NameWoDiacritics', 'Subdivision',
                        'Status', 'Function', 'Date', 'IATA', 'Coordinates', 'Remarks'])
    codelist_df.to_csv(f"data/code-list.csv", index=False)
    #country_df.to_csv(f"data/country-codes.csv", index=False)
    alias_df.to_csv(f"data/alias.csv", index=False)
    print("Processed and saved UNLOCODE files")
    return

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    # Search for loc zip file
    pattern = re.compile(r'loc\d+csv\.zip')

    zip_path = ''
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Check if the file name matches the pattern
            if pattern.match(file):
                zip_path = os.path.join(root, file)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        print(f"Successfully extracted {zip_path}")

        extracted_files = zip_ref.namelist()
        process(extracted_files)

        # Remove the extracted files
        for file_name in extracted_files:
            os.remove(file_name)
            print(f"Removed {file_name}")

    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")
