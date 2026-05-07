<a className="gh-badge" href="https://datahub.io/core/un-locode"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

The United Nations Code for Trade and Transport Locations is a code list maintained by UNECE, United Nations agency, to facilitate trade.

## Data

Data comes from the [UNECE UN/LOCODE Download page](https://unece.org/trade/cefact/UNLOCODE-Download), released at least once a year.

## Preparation

Data is updated automatically via GitHub Actions on the first of each month. The workflow fetches the latest release from the [UNICC GitLab repository](https://opensource.unicc.org/un/unece/uncefact/vocab-locode), processes it, and commits the result.

To run locally, tools needed: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).

1. Go to [https://unece.org/trade/cefact/UNLOCODE-Download](https://unece.org/trade/cefact/UNLOCODE-Download), find the edition you want, and click its **Download** link. Extract the zip into a `release/` folder in the repo root so it has this structure:

```
release/
  UNLOCODE CodeList.mdb
  csv/
    SubdivisionCodes.csv
    UNLOCODE CodeListPart1.csv
    UNLOCODE CodeListPart2.csv
    UNLOCODE CodeListPart3.csv
```

2. Install Python dependencies and run the pipeline:

```
pip install -r scripts/requirements.txt
make
```

## License

All data is licensed under the [ODC Public Domain Dedication and Licence (PDDL)](http://opendatacommons.org/licenses/pddl/1-0/).
