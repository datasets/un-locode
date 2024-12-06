<a className="gh-badge" href="https://datahub.io/core/un-locode"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

The United Nations Code for Trade and Transport Locations is a code list mantained by UNECE, United Nations agency, to facilitate trade.

## Data

Data comes from the [UNECE page](http://www.unece.org/cefact/locode/welcome.html), released at least once a year.

## Preparation

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

## License

All data is licensed under the [ODC Public Domain Dedication and Licence (PDDL)](http://opendatacommons.org/licenses/pddl/1-0/).
