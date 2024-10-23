#!/bin/bash

# Check arguments and unzip
if [ $# -lt 1 ]; then
    echo "Usage: $0 <zip_file>"
    exit 1
fi
unzip -j "$1" "*.mdb" > /dev/null 2>&1

# Get MDB file and wait for UNLOCODE CodeList.mdb to appear
mdb_file=$(basename -- *.mdb)
filename="${mdb_file%.*}"

file=""
for i in {1..3}; do
    file=$(ls *UNLOCODE\ CodeList.mdb 2>/dev/null)
    [ -n "$file" ] && break
    sleep 1
done

[ -z "$file" ] && { echo "Error: UNLOCODE CodeList.mdb file not found."; exit 1; }

# Process tables
IN=$(mdb-tables -d ";" "$mdb_file" 2>/dev/null)
IFS=';' read -ra TABLES <<< "$IN"

for i in "${TABLES[@]}"; do
    echo "Processing table: $i"
    mdb-export "$mdb_file" "$i" > "mdb_$i.csv" 2>/dev/null
    [ -f "mdb_$i.csv" ] && csvclean --empty-columns "mdb_$i.csv" > /dev/null 2>&1
    echo "Done processing table: $i"
done

# Handle specific tables and CSV cleanup
if [ -f "mdb_SubdivisionCodes.csv" ]; then
    echo "Processing SubdivisionCodes table"
    gawk -v RS='"' 'NR % 2 == 0 { gsub(/\n/, " "); gsub(/\r/, " "); } { printf("%s%s", $0, RT) }' "mdb_SubdivisionCodes.csv" > subdivision-codes.tmp.csv
    sed -i '' -e 's/ \{2,\}/ /g' -e 's/[[:blank:]]*$//' subdivision-codes.tmp.csv > /dev/null 2>&1
    sed -i '' 's/\t/ /g' subdivision-codes.tmp.csv > /dev/null 2>&1
    uniq subdivision-codes.tmp.csv > subdivision-codes.tmp2.csv
    mv subdivision-codes.tmp2.csv data/subdivision-codes.csv
    csvformat -U 1 data/subdivision-codes.csv > data/subdivision-codes-cleaned.csv && mv data/subdivision-codes-cleaned.csv data/subdivision-codes.csv
    echo "Done processing SubdivisionCodes table"
fi

# Handle remaining tables
[ -f "mdb_StatusIndicators.csv" ] && { mv "mdb_StatusIndicators.csv" data/status-indicators.csv; csvformat -U 1 data/status-indicators.csv > data/status-indicators-cleaned.csv && mv data/status-indicators-cleaned.csv data/status-indicators.csv; echo "Done processing StatusIndicators table"; }
[ -f "mdb_FunctionClassifiers.csv" ] && { mv "mdb_FunctionClassifiers.csv" data/function-classifiers.csv; csvformat -U 1 data/function-classifiers.csv > data/function-classifiers-cleaned.csv && mv data/function-classifiers-cleaned.csv data/function-classifiers.csv; echo "Done processing FunctionClassifiers table"; }
[ -f "mdb_CountryCodes.csv" ] && { mv "mdb_CountryCodes.csv" data/country-codes.csv; csvformat -U 1 data/country-codes.csv > data/country-codes-cleaned.csv && mv data/country-codes-cleaned.csv data/country-codes.csv; echo "Done processing CountryCodes table"; }

# Process UNLOCODE CodeList from MDB
if [ -f "$file" ]; then
    echo "Processing UNLOCODE CodeList table"
    gawk -v RS='"' 'NR % 2 == 0 { gsub(/\n/, "") } { printf("%s%s", $0, RT) }' "$file" > code-list.tmp.csv
    csvgrep -c 3 -r "^$" -i code-list.tmp.csv > code-list.tmp2.csv > /dev/null 2>&1
    (head -n 1 code-list.tmp2.csv && tail -n +2 code-list.tmp2.csv | LC_ALL=C sort -t, -k2,2 -k4,4 --ignore-case) > code-list.csv
    mv code-list.csv data/code-list.csv
    csvformat -U 1 data/code-list.csv > data/code-list-cleaned.csv && mv data/code-list-cleaned.csv data/code-list.csv
    echo "Done processing UNLOCODE CodeList table"
fi

# Cleanup temporary files and MDB file
rm *.csv
rm *.mdb
