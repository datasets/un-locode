import re
import bs4
import csv
import requests
import pandas as pd 

from bs4 import BeautifulSoup

source_path = 'https://service.unece.org/trade/locode/Service/LocodeColumn.htm'
pattern = r'^"?([^,]+),"([^"]+)"?$'

def get_table_schema(source_path):
    print('Processing UN/LOCODE table description data.')
    response = requests.get(source_path)
    soup = BeautifulSoup(response.text, 'html.parser')
    func_class = {
        "FunctionCode": [],
        "FunctionDescription": []
    }
    status_indicator = {
        "STStatus": [],
        "STDescription": []
    }
    print('Extracting data from the function classifier table.')
    for table in soup.find_all('table')[2]:
        if type(table) is not bs4.element.NavigableString:
            value = table.get_text().split('\n')
            func_class["FunctionCode"].append(value[1].split()[0])
            join = ' '.join(value[1:])
            temp = join.split()
            func_desc = ' '.join(temp)
            func_desc = re.sub(pattern, r'\1,\2', func_desc)
            func_class["FunctionDescription"].append(func_desc)
    print('Extracting data from the status indicator table.')
    for table in soup.find_all('table')[3]:
        if type(table) is not bs4.element.NavigableString:
            value = table.get_text().split('\n')
            status_indicator["STStatus"].append(value[1].split()[0])
            join = ' '.join(value[1:])
            temp = join.split()
            description = ' '.join(temp)
            status_indicator["STDescription"].append(description)
    print('Saving data to CSV files.')
    df_func_class = pd.DataFrame(func_class)
    df_func_class['FunctionDescription'] = df_func_class['FunctionDescription'].str.replace(',', ' ', regex=False).replace('  ', ' ', regex=True)
    df_status_indicator = pd.DataFrame(status_indicator)
    df_func_class.to_csv('data/function-classifiers.csv', index=False,sep=',', quoting=csv.QUOTE_NONE, escapechar='\\')
    df_status_indicator.to_csv('data/status-indicators.csv', index=False,sep=',' ,quoting=csv.QUOTE_NONE, escapechar='\\')
    print('Done')
    
if __name__ == '__main__':
    get_table_schema(source_path)