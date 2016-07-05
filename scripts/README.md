To build the dataset we use the mdb version of the current edition. Tools needed: [MDBTools](http://mdbtools.sourceforge.net/) and [CSVKit](https://github.com/onyxfish/csvkit).

- List tables ```mdb-tables {yyyy}-{r}\ UNLOCODE\ CodeList.mdb```
- Extract from mdb file: ```mdb-export {yyyy}-{r}\ UNLOCODE\ CodeList.mdb "{yyyy}-{r} UNLOCODE CodeList" > mdb_codelist.csv```
- Clean resulting csv: ```csvclean mdb_subdivisioncodes.csv```
- Remove country headers in codelist ```script/rmstr.php old_code-list.csv```

Tables needed to be exported:

- "{yyyy}-{r} UNLOCODE CodeList" > code-list.csv
- "CountryCodes" > country-codes.csv
- "FunctionClassifiers" > function-classifiers.csv
- "StatusIndicators" > status-indicators.csv
- "SubdivisionCodes" > subdivision-codes.csv

Note: in the strings above {yyyy} is the full year, {r} is the revision (1 or 2)
