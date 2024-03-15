#Build release
As the original release files have encoding problems, we need to process both the mdb and the csv release.
To build the dataset we use the csv version of the current edition.

Tools needed: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).
Download the current edition from [UNECE](https://www.unece.org/cefact/codesfortrade/codes_index.html) and put it into the root directory.
Then execute ```bash scripts/prepare_edition_mdb.sh loc{ed}mdb.zip```, where {ed} identify the release.

To integrate the data from the csv then run the python file

Prerequisites:

```
pip install pandas titlecase
```

Run:
```
python scripts/integrate.py loc232csv.zip
```

The provided ```prepare.py``` file would work alone when the original csv file will be fixed upstream.