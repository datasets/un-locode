import os
import re
import csv
import glob
import zipfile
import pandas as pd

from titlecase import titlecase

data_file_path = os.path.join('data', 'subdivision-codes.csv')

def fix_multiline_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    merged_lines = []
    temp_line = ''
    inside_quotes = False

    for line in lines:
        if line.count('"') % 2 == 1:
            inside_quotes = not inside_quotes

        if inside_quotes:
            temp_line += line.strip()
        else:
            if temp_line:
                merged_lines.append(temp_line + ' ' + line.strip())
                temp_line = ''
            else:
                merged_lines.append(line.strip())

    with open(file_path, 'w', encoding='utf-8', newline='') as outfile:
        outfile.write('\n'.join(merged_lines) + '\n')

def correct_swapped_function_status(codelist_df):
    function_pattern = r'^[-\dB]+$'
    status_pattern = r'^[A-Z]{0,2}$'

    mask = (
        codelist_df['Function'].str.match(status_pattern, na=False) & codelist_df['Status'].str.match(function_pattern, na=False)
    ) | (
        codelist_df['Status'].str.match(function_pattern, na=False) & codelist_df['Function'].isna()
    )

    codelist_df.loc[mask, ['Function', 'Status']] = codelist_df.loc[mask, ['Status', 'Function']].values
    return codelist_df

def clean_extra_rows(codelist_df):
    codelist_df.dropna(how="all", inplace=True)
    codelist_df.drop_duplicates(subset=['Country', 'Location', 'Name', 'Subdivision', 'Date', 'Coordinates'], inplace=True)

    return codelist_df

def remove_double_quotes(file_path):
    # Read the CSV file and process it row by row
    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = [row for row in reader]  # Read all rows

    # Write the CSV back with minimal quoting (preserving quotes where necessary)
    with open(file_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

def process(extracted_files):
    # Process CSV files
    codelist_df = pd.DataFrame(columns=['Change', 'Country', 'Location', 'Name', 'NameWoDiacritics', 'Subdivision',
                        'Function', 'Status', 'Date', 'IATA', 'Coordinates', 'Remarks'], dtype=str)
    codelist_list = []
    #country_df = pd.DataFrame(columns=['CountryCode', 'CountryName'])
    alias_df = pd.DataFrame(columns=['Country', 'Name', 'NameWoDiacritics'], dtype=str)

    for file_name in extracted_files:
        if file_name.endswith('.csv'):
            if 'subdivisioncodes' in file_name.lower():
                subdivision_df = pd.read_csv(file_name, encoding='cp1252', dtype=str,
                                             usecols=[0, 1, 2, 3], names=['SUCountry', 'SUCode', 'SUName', 'SUType'])
                subdivision_df_main = pd.read_csv(data_file_path, dtype=str)
                subdivision_df_main = pd.merge(subdivision_df_main, subdivision_df[['SUCountry', 'SUCode', 'SUType']],
                               on=['SUCountry', 'SUCode'], how='left')
                subdivision_df_main['SUCode'] = subdivision_df_main['SUCode'].fillna("NA")
                subdivision_df_main['SUCountry'] = subdivision_df_main['SUCountry'].fillna("NA")
                # Trimming whitespaces from the SUName column
                subdivision_df_main = subdivision_df_main.map(lambda x: x.strip() if isinstance(x, str) else x)
                subdivision_df_main.to_csv(data_file_path, index=False)
            else:
                unlocode_df_test = pd.read_csv(file_name, encoding='cp1252', nrows=1, dtype=str)

                if all(unlocode_df_test.iloc[0].str.isalpha()):
                    unlocode_df = pd.read_csv(file_name, encoding='cp1252', dtype=str, keep_default_na=False)
                else:
                    unlocode_df = pd.read_csv(file_name, encoding='cp1252', header=None, dtype=str, keep_default_na=False)
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
    codelist_df  = pd.DataFrame(codelist_list, dtype=str)
    codelist_df = codelist_df.reindex(columns=['Change', 'Country', 'Location', 'Name', 'NameWoDiacritics', 'Subdivision',
                        'Status', 'Function', 'Date', 'IATA', 'Coordinates', 'Remarks'])
    # Keep only rows where 'Country' values are empty, 1 character, or exactly 2 characters
    codelist_df['Country'] = codelist_df['Country'].fillna('NA')
    codelist_df = codelist_df[codelist_df['Country'].str.len().fillna(0).between(0, 2)]
    codelist_df = correct_swapped_function_status(codelist_df)
    codelist_df = clean_extra_rows(codelist_df)
    codelist_df.to_csv(f"data/code-list.csv", index=False)

    alias_df.drop_duplicates(inplace=True)
    alias_df.to_csv(f"data/alias.csv", index=False)
    print("Processed and saved UNLOCODE files")
    return

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))

    cleaned_files = glob.glob('data/*-cleaned.csv')

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


    file_paths = [
        os.path.join('data', 'code-list.csv'),
        os.path.join('data', 'alias.csv'),
        os.path.join('data', 'subdivision-codes.csv'),
        os.path.join('data', 'country-codes.csv'),
        os.path.join('data', 'function-classifiers.csv'),
        os.path.join('data', 'status-indicators.csv')
    ]

    # Loop over the file paths and call remove_double_quotes for each
    for file_path in file_paths:
        remove_double_quotes(file_path)

    fix_multiline_csv(data_file_path)

    for file_path in cleaned_files:
        os.remove(file_path)