import zipfile
import sys
import os
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
                year_term = file_name.split(' ')[0]
                print(f"Edition {year_term}")
                df = pd.read_csv(file_name, encoding='cp1252', dtype=str)
                df.columns = ['SUCountry', 'SUCode', 'SUName', 'SUType']
                df.to_csv(f"data/subdivision-codes.csv", index=False)
                print(f"Processed {file_name}")
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

    if len(sys.argv) != 2:
        print("Usage: python extract_zip.py <zip_file_path>")
        sys.exit(1)

    zip_path = sys.argv[1]

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
