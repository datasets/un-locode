#!/bin/bash
# Exports the lookup tables from "UNLOCODE CodeList.mdb" into data/*.csv.
# Needs mdbtools, gawk and csvkit. Works with GNU sed and with macOS sed.
# The script stops on a real error (a failed export, a missing table).
# It does not stop on csvclean, which only prints a report.
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <zip_file>"
    exit 1
fi

mdb_file="UNLOCODE CodeList.mdb"

# Remove temporary files when the script ends, also after an error.
cleanup() {
    rm -f mdb_*.csv subdivision-codes.tmp* data/*.tmp "$mdb_file"
}
trap cleanup EXIT

unzip -o -j "$1" "*.mdb" > /dev/null
[ -f "$mdb_file" ] || { echo "Error: $mdb_file not found in $1." >&2; exit 1; }

# Export every table to mdb_<table>.csv
table_list=$(mdb-tables -d ";" "$mdb_file")   # a failure here stops the script
IFS=';' read -ra TABLES <<< "$table_list"

for i in "${TABLES[@]}"; do
    echo "Processing table: $i"
    mdb-export "$mdb_file" "$i" > "mdb_$i.csv"
    # csvclean only prints a report here and exits non-zero when it finds rows to report.
    csvclean --empty-columns "mdb_$i.csv" > /dev/null 2>&1 || true
    echo "Done processing table: $i"
done

# These four tables must exist. Fail loudly instead of writing nothing.
for t in SubdivisionCodes StatusIndicators FunctionClassifiers CountryCodes; do
    [ -f "mdb_$t.csv" ] || { echo "Error: table $t is missing in $mdb_file." >&2; exit 1; }
done

# csvformat writes LF line endings (-M) so the files do not change line by line on every run.
format_csv() {
    csvformat -U 1 -M $'\n' "$1" > "$2.tmp" && mv "$2.tmp" "$2"
}

echo "Processing SubdivisionCodes table"
gawk -v RS='"' 'NR % 2 == 0 { gsub(/\n/, " "); gsub(/\r/, " "); } { printf("%s%s", $0, RT) }' "mdb_SubdivisionCodes.csv" > subdivision-codes.tmp.csv
# No "sed -i": its syntax differs between GNU and macOS. Write to a new file instead.
sed -e 's/ \{2,\}/ /g' -e 's/[[:blank:]]*$//' subdivision-codes.tmp.csv > subdivision-codes.tmp.sed
# tr instead of sed 's/\t/ /g': macOS sed does not understand \t
tr '\t' ' ' < subdivision-codes.tmp.sed > subdivision-codes.tmp2.csv
# uniq removes duplicate lines that follow each other (the export has three such pairs)
uniq subdivision-codes.tmp2.csv > subdivision-codes.tmp3.csv
format_csv subdivision-codes.tmp3.csv data/subdivision-codes.csv
echo "Done processing SubdivisionCodes table"

format_csv mdb_StatusIndicators.csv data/status-indicators.csv
echo "Done processing StatusIndicators table"
format_csv mdb_FunctionClassifiers.csv data/function-classifiers.csv
echo "Done processing FunctionClassifiers table"
format_csv mdb_CountryCodes.csv data/country-codes.csv
echo "Done processing CountryCodes table"

# data/code-list.csv is not written here. scripts/prepare.py builds it from the
# release/csv files, and the old block that tried to build it from the MDB wrote an empty file.
