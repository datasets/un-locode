import zipfile
import sys
import os
import pandas as pd
from titlecase import titlecase
import csv


def process(extracted_files):

    # Process CSV files
    alias_df = pd.DataFrame(columns=['Country', 'Name', 'NameWoDiacritics'])

    for file_name in extracted_files:
        if file_name.endswith('.csv'):
            if 'SubdivisionCodes' in file_name:
                year_term = file_name.split(' ')[0]
                print(f"Edition {year_term}")
                with open(file_name, 'r', encoding='cp1252') as infile, open('tmpsub.csv', 'w', newline='', encoding='cp1252') as outfile:
                    reader = csv.reader(infile)
                    writer = csv.writer(outfile)
                    current_entry = []

                    for row in reader:
                        if len(row) == 4:
                            if current_entry:
                                writer.writerow(current_entry)
                                current_entry = []

                            writer.writerow(row)
                        else:
                            current_entry.extend(row)

                    if current_entry:
                        writer.writerow(current_entry)

                df = pd.read_csv('tmpsub.csv', encoding='cp1252',
                                 dtype=str, header=None, na_filter=False)
                df.columns = ['SUCountry', 'SUCode', 'SUName', 'SUType']
                df_base = pd.read_csv(
                    f"data/subdivision-codes.csv", dtype=str, na_filter=False)
                merged_df = pd.merge(df_base, df[['SUCountry', 'SUCode', 'SUType']], on=[
                                     'SUCountry', 'SUCode'], how='left')
                merged_df = merged_df.drop_duplicates()
                merged_df.to_csv(f"data/subdivision-codes.csv", index=False)
                print(f"Processed {file_name}")
                continue

            unlocode_df = pd.read_csv(
                file_name, encoding='cp1252', header=None, dtype=str)
            unlocode_df.columns = ['Change', 'Country', 'Location', 'Name', 'NameWoDiacritics', 'Subdivision',
                                   'Function', 'Status', 'Date', 'IATA', 'Coordinates', 'Remarks']

            for index, row in unlocode_df.iterrows():
                if pd.isna(row['Location']) or row['Location'] == '':
                    if row['Change'] == '=':  # alias row
                        alias_df.loc[len(alias_df.index)] = row[[
                            'Country', 'Name', 'NameWoDiacritics']]
                    continue
            print(f"Processed {file_name}")

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
        os.remove('tmpsub.csv')
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")
    finally:
        None