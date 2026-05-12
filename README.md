<a className="gh-badge" href="https://datahub.io/core/un-locode"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

The United Nations Code for Trade and Transport Locations is a code list maintained by UNECE, United Nations agency, to facilitate trade.

## Data

Data comes from the [UNECE UN/LOCODE Download page](https://unece.org/trade/cefact/UNLOCODE-Download), released at least once a year.

## Updating the data

When UNECE publishes a new edition, update the data by running the pipeline locally and committing the result.

Install the required tools (macOS):

```
brew install mdbtools csvkit gawk
pip install -r scripts/requirements.txt
```

Download the latest edition from [https://unece.org/trade/cefact/UNLOCODE-Download](https://unece.org/trade/cefact/UNLOCODE-Download) — click the **Download** link on the new release row. Extract the zip into a `release/` folder in the repo root so it has this structure:

```
release/
  UNLOCODE CodeList.mdb
  csv/
    SubdivisionCodes.csv
    UNLOCODE CodeListPart1.csv
    UNLOCODE CodeListPart2.csv
    UNLOCODE CodeListPart3.csv
```

> **Note:** the scripts assume this folder structure and file naming. If UNECE changes the release packaging in a future edition, the scripts may need to be adjusted before running.

Then run:

```
make
```

Then commit the updated files:

```
git add data/
git commit -m "Update to edition YYYY-N"
git push
```

## License

All data is licensed under the [ODC Public Domain Dedication and Licence (PDDL)](http://opendatacommons.org/licenses/pddl/1-0/).
