filename=$(basename "$1")
filename="${filename%.*}"

IN=$(mdb-tables -d ";" "$1")
IFS=';' read -ra TABLES <<< "$IN"
for i in "${TABLES[@]}"; do
    mdb-export "$1" "$i" > "mdb_$i.csv"
    csvclean "mdb_$i.csv"
done
php scripts/rmstr.php "mdb_${filename}_out.csv"
mv code-list.csv data/code-list.csv
mv mdb_CountryCodes_out.csv data/country-codes.csv
mv mdb_FunctionClassifiers_out.csv data/function-classifiers.csv
mv mdb_StatusIndicators_out.csv data/status-indicators.csv
mv mdb_SubdivisionCodes_out.csv data/subdivision-codes.csv
rm *.csv
