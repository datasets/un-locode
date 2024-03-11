#Build release
To build the dataset we use the csv version of the current edition. 

Prerequisites:

```
pip install pandas titlecase
```

Run:
```
python scripts/prepare.py loc232csv.zip
```