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

Run the pipeline — it downloads the latest edition automatically and regenerates all data files:

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
