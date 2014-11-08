# UN-LOCODE datapackage

The United Nations Code for Trade and Transport Locations is a code list mantained by UNECE, United Nations agency, to facilitate trade.

## Data

Data comes from the [UNECE page](http://www.unece.org/cefact/locode/welcome.html), released at least once a year. The files released in this package are extracted from the mdb archive to preserve UTF-8 encoding.

## Build dataset
Tools: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).

- List tables ```mdb-tables 2014-1\ UNLOCODE\ CodeList.mdb```
- Extract from mdb file: ```mdb-export 2014-1\ UNLOCODE\ CodeList.mdb "2014-1 UNLOCODE CodeList" > mdb_codelist.csv```
- Convert to TSV: ```csvformat -T mdb_subdivisioncodes.csv > mdb_subdivisioncodes.tsv```
- Remove country headers in codelist (see script/rmstr.php)
