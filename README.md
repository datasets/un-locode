# UN-LOCODE datapackage

The United Nations Code for Trade and Transport Locations is a code list mantained by UNECE, United Nations agency, to facilitate trade.

## Data

Data comes from the [UNECE page](http://www.unece.org/cefact/locode/welcome.html), released at least once a year. The files released in this package are extracted from the mdb archive to preserve UTF-8 encoding.

## Build dataset
Tools: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).

- List tables ```mdb-tables {yyyy}-{r}\ UNLOCODE\ CodeList.mdb```
- Extract from mdb file: ```mdb-export {yyyy}-{r}\ UNLOCODE\ CodeList.mdb "{yyyy}-{r} UNLOCODE CodeList" > mdb_codelist.csv```
- Clean resulting csv: ```csvclean mdb_subdivisioncodes.csv```
- Remove country headers in codelist ```script/rmstr.php old_code-list.csv```

Tables:

- "{yyyy}-{r} UNLOCODE CodeList" > code-list.csv
- "CountryCodes" > country-codes.csv
- "FunctionClassifiers" > function-classifiers.csv
- "StatusIndicators" > status-indicators.csv
- "SubdivisionCodes" > subdivision-codes.csv

Note: in the strings above {yyyy} is the full year, {r} is the revision (1 or 2)