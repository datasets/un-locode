#Build release
To build the dataset we use the mdb version of the current edition. 
Tools needed: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).
Download the current edition in mdb format from [UNECE](https://www.unece.org/cefact/codesfortrade/codes_index.html) and put it into the root directory.
Then execute ```bash scripts/prepare_edition.sh {yyyy}-{r}\ UNLOCODE\ CodeList.mdb```, where {yyyy} and {r} identify the release.
