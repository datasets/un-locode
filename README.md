# UN-LOCODE datapackage

The United Nations Code for Trade and Transport Locations is a code list mantained by UNECE, United Nations agency, to facilitate trade.

## Data

Data comes from the [UNECE page](http://www.unece.org/cefact/locode/welcome.html), released at least once a year. The files released in this package are extracted from the mdb archive to preserve UTF-8 encoding.

## Build dataset
Tools: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).

- List tables ```mdb-tables 2014-2\ UNLOCODE\ CodeList.mdb```
- Extract from mdb file: ```mdb-export 2014-2\ UNLOCODE\ CodeList.mdb "2014-2 UNLOCODE CodeList" > mdb_codelist.csv```
- Clean resulting csv: ```csvclean mdb_subdivisioncodes.csv```
- Remove country headers in codelist (see script/rmstr.php)

Tables:

- "2014-2 UNLOCODE CodeList" > codeList.csv
- "CountryCodes" > countryCodes.csv
- "FunctionClassifiers" > functionClassifiers.csv
- "StatusIndicators" > statusIndicators.csv
- "SubdivisionCodes" > subdivisionCodes.csv

