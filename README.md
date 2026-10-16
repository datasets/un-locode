<a className="gh-badge" href="https://datahub.io/core/un-locode"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# UN/LOCODE

The United Nations Code for Trade and Transport Locations: five-character codes for ports, airports, rail and road terminals, cities and other places used in international trade and transport. The code list is maintained by UNECE.

Column definitions and types are in `datapackage.json`.

## Data

* `data/code-list.csv`: one row per location entry.
* `data/subdivision-codes.csv`: ISO 3166-2 subdivision codes and names used by the `Subdivision` column.
* `data/country-codes.csv`: country codes and names as used in the code list.
* `data/alias.csv`: alternative names of countries.
* `data/function-classifiers.csv`: the meaning of each position of the `Function` column.
* `data/status-indicators.csv`: the meaning of the `Status` column.

Columns of `data/code-list.csv`:

| Column | Meaning |
|---|---|
| `Change` | Change indicator: `+` newly added, `\|` changed, `#` name changed, `!` US location with a duplicate IATA code, `X` to be removed. Empty for entries that did not change |
| `Country` | ISO 3166 alpha-2 country code, for example `AE`. Defined in `country-codes.csv` |
| `Location` | 3-character location code (letters and the digits 2 to 9), for example `DXB`. With `Country` it forms the 5-character UN/LOCODE |
| `Name` | Name of the location, with diacritics |
| `NameWoDiacritics` | The same name with diacritics replaced by ASCII letters |
| `Subdivision` | ISO 3166-2 subdivision code, for example `DU`. Defined in `subdivision-codes.csv`. May be empty |
| `Status` | Approval or verification status, for example `AI`. Defined in `status-indicators.csv` |
| `Function` | 8-character string, one position for each function (port, rail terminal, airport and so on). A digit or letter means the function is present, a dash means it is not. Defined in `function-classifiers.csv` |
| `Date` | Date of the entry as `YYMM`, for example `2501` is January 2025. May be empty |
| `IATA` | IATA code, only when it differs from the UN/LOCODE location code. May be empty |
| `Coordinates` | Latitude and longitude as degrees and minutes with a letter for the direction, for example `2515N 05516E`. May be empty |
| `Remarks` | Free-text remark. May be empty |

### Known limitations

* The file follows UNECE's "Pre-Release (Latest)", not an official release. UNECE describes it as "for latest codes in between official releases", so it can contain codes approved after the last official biannual publication, and entries can still change.
* `Country` + `Location` is not unique. Some places have two entries, for example an old and a changed name (one with `#` in `Change`). Use `Change` and `Date` to tell them apart.
* Rows with `Change` set to `X` are entries UNECE marks for removal. They stay in the file until a later release drops them.
* The code for Namibia is the two letters `NA` (in `Country` and in `SUCountry`). Many tools read the text `NA` as "missing". Read the files as text and keep empty cells empty: `pd.read_csv("data/code-list.csv", dtype=str, keep_default_na=False)`.
* Codes and `Function` strings are text. `Location` can be made only of digits and letters such as `5MS`, and `Function` starts with digits or dashes. Do not let your tool turn them into numbers.
* `Coordinates` is one text column in degrees and minutes, not two decimal numbers.
* Rows without a location code (country-name rows and alias rows) are not in `code-list.csv`. The aliases are in `alias.csv`.

## Data sources

* [UN/LOCODE, published by UNECE](https://unlocode.unece.org/publications): the code list and its lookup tables. The build uses the file UNECE calls "Pre-Release (Latest)". Licence: unclear (see [License](#license)).

Changes made to the source data: the script reads the release's Access database for the lookup tables and its three CSV parts for the code list. For `code-list.csv` it joins the three parts, moves the alias rows (`Change` set to `=`) to `alias.csv`, drops the country-name rows, swaps `Status` and `Function` where the release has them the wrong way round, removes duplicate rows (same country, location, name, subdivision, date and coordinates), and writes the columns in a fixed order. For `subdivision-codes.csv` it adds the subdivision type from the release's CSV file, collapses extra spaces and removes repeated lines. All files are written with LF line endings.

Not endorsed by, or affiliated with, UNECE or the United Nations.

## Preparation

You need Python 3.12 or greater, `make`, and the tools `mdbtools` and `gawk`. Install them (macOS shown; on Ubuntu use `sudo apt-get install mdbtools gawk`):

```bash
brew install mdbtools gawk
pip install -r scripts/requirements.txt csvkit
```

Download the release into `release/` and build the data:

```bash
./scripts/fetch_release.sh
make
```

`scripts/fetch_release.sh` downloads `https://unlocode.unece.org/downloads/unlocode-latest.zip`. To build from another zip, for example an official release, run `UNLOCODE_URL=<zip url> ./scripts/fetch_release.sh`. The zip must contain this folder layout:

```
release/
  UNLOCODE CodeList.mdb
  csv/
    SubdivisionCodes.csv
    UNLOCODE CodeListPart1.csv
    UNLOCODE CodeListPart2.csv
    UNLOCODE CodeListPart3.csv
```

Set `PYTHON=<path>` if `python3` is not the interpreter that has the requirements installed (`make PYTHON=.venv/bin/python`).

A GitHub workflow (`.github/workflows/update.yml`) runs this on the first day of every month (at 03:00 UTC) and when started by hand. It commits `data/` if something changed.

## License

The licence of the UN/LOCODE data is unclear, because UNECE's own pages say different things. What we checked:

* The [terms of the UN/LOCODE site](https://unlocode.unece.org/terms) say the United Nations grants permission "to download and copy the information, documents and materials ... for the User's personal, non-commercial use, without any right to resell or redistribute them or to compile or create derivative works therefrom", and that this is "subject to ... more specific restrictions that may apply to specific Material".
* The footer of the same site says: "All UN/CEFACT standards are free to use under CC By 4.0 license". UN/LOCODE is published through UN/CEFACT (Recommendation 16). The pages we read do not say whether that sentence covers the code list itself.
* [Recommendation 16](https://unlocode.unece.org/recommendation16) says updated versions of the directory "will be published on the UNECE website free of charge".
* The [source repository](https://opensource.unicc.org/un/unece/uncefact/vocab-locode) has a GPL-3.0 `LICENSE` file for the repository. Its data folder has no licence notice of its own.

We could not establish which of these applies to the data in this package. If you plan to redistribute it or use it commercially, ask UNECE for written confirmation first. We credit UNECE as the source in any case (see [ATTRIBUTION.txt](ATTRIBUTION.txt)).

The maintainers place only their own work (the scripts, the column definitions and the file layout) under the [Public Domain Dedication and License (PDDL)](https://opendatacommons.org/licenses/pddl/1.0/). This does not cover the UN/LOCODE data itself.
