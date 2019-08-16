#!/bin/bash
filename=$(basename "$1")
filename="${filename%.*}"

IN=$(mdb-tables -d ";" "$1")
IFS=';' read -ra TABLES <<< "$IN"
for i in "${TABLES[@]}"; do
    mdb-export "$1" "$i" > "mdb_$i.csv"
    csvclean "mdb_$i.csv"
done

gawk -v RS='"[^"]*"' -v ORS= '{gsub(/\n/, " ", RT); print $0  RT}' mdb_SubdivisionCodes_out.csv > subdivision-codes.tmp.csv
sed -i 's/ \{2,\}/ /g;s/[[:blank:]]*$//' subdivision-codes.tmp.csv
sed -i 's/\t/ /g' subdivision-codes.tmp.csv

gawk -v RS='"' 'NR % 2 == 0 { gsub(/\n/, "") } { printf("%s%s", $0, RT) }'  "mdb_${filename}_out.csv" > code-list.tmp.csv #remove newlines in data
csvgrep -c 3 -r "^$" -i code-list.tmp.csv > code-list.tmp2.csv #remove country headers

(head -n 1 code-list.tmp2.csv && tail -n +2 code-list.tmp2.csv | LC_ALL=C sort -t, -k2,2  -k4,4 --ignore-case) > code-list.csv # sort data by locode

mv code-list.csv data/code-list.csv
mv mdb_CountryCodes_out.csv data/country-codes.csv
mv mdb_FunctionClassifiers_out.csv data/function-classifiers.csv
mv mdb_StatusIndicators_out.csv data/status-indicators.csv
mv subdivision-codes.tmp.csv data/subdivision-codes.csv
rm *.csv
