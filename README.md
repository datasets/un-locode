# UN-LOCODE datapackage

The United Nations Code for Trade and Transport Locations is a code list mantained by UNECE, United Nations agency, to facilitate trade.

## Data

United Nations Code for Trade and Transport Locations

UN/LOCODE The "United Nations Code for Trade and Transport Locations" is commonly more known as "UN/LOCODE". Although managed and maintained by the UNECE (http://www.unece.org/cefact/locode/welcome.html), it is the product of a wide collaboration in the framework of the joint trade facilitation effort undertaken within the United Nations. The files released in this package are extracted from the mdb archive to preserve UTF-8 encoding.

## Build dataset
Tools: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).

- List tables ```mdb-tables 2014-2\ UNLOCODE\ CodeList.mdb```
- Extract from mdb file: ```mdb-export 2014-2\ UNLOCODE\ CodeList.mdb "2014-2 UNLOCODE CodeList" > mdb_codelist.csv```
- Clean resulting csv: ```csvclean mdb_subdivisioncodes.csv```
- Remove country headers in codelist ```script/rmstr.php old_code-list.csv```

Tables:

- "2014-2 UNLOCODE CodeList" > code-list.csv
- "CountryCodes" > country-codes.csv
- "FunctionClassifiers" > function-classifiers.csv
- "StatusIndicators" > status-indicators.csv
- "SubdivisionCodes" > subdivision-codes.csv
