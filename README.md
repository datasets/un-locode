<a className="gh-badge" href="https://datahub.io/core/un-locode"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

The United Nations Code for Trade and Transport Locations is a code list maintained by UNECE, United Nations agency, to facilitate trade.

## Data

Data comes from the [UNECE UN/LOCODE Download page](https://unece.org/trade/cefact/UNLOCODE-Download), released at least once a year.

## Preparation

Data is updated automatically via GitHub Actions on the first of each month. The workflow fetches the latest release from the [UNICC GitLab repository](https://opensource.unicc.org/un/unece/uncefact/vocab-locode), processes it, and commits the result.

To run locally, install the required tools — on macOS:

```
brew install mdbtools csvkit gawk
pip install -r scripts/requirements.txt
```

Then run the full pipeline (downloads the latest release automatically):

```
make
```

## License

All data is licensed under the [ODC Public Domain Dedication and Licence (PDDL)](http://opendatacommons.org/licenses/pddl/1-0/).
