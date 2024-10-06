## Build release
This dataset has been adjusted and updated to run on a daily bases.

The dataset creation process only requires `python` and additional libraries to be installed.

Prerequisites:

Install Requirements.txt
```
pip install -r requirements.txt
# if you are running from root folder
pip install -r scripts/requirements.txt
```

Run:
```
python data_generate.py
python table_generate.py
```