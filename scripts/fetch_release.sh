#!/bin/bash
# Downloads the current UN/LOCODE publication into ./release/ (the folder layout `make` expects).
# The old unece.org download page answers 403 to scripts, so this uses the file that
# unlocode.unece.org publishes. Set UNLOCODE_URL to download another zip.
set -euo pipefail
cd "$(dirname "$0")/.."

URL="${UNLOCODE_URL:-https://unlocode.unece.org/downloads/unlocode-latest.zip}"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

curl -fsSL --retry 3 --retry-delay 5 --max-time 300 -o "$tmp/release.zip" "$URL"
unzip -q "$tmp/release.zip" -d "$tmp/unzipped"

for f in "release/UNLOCODE CodeList.mdb" "release/csv/SubdivisionCodes.csv" \
         "release/csv/UNLOCODE CodeListPart1.csv" "release/csv/UNLOCODE CodeListPart2.csv" \
         "release/csv/UNLOCODE CodeListPart3.csv"; do
  [ -f "$tmp/unzipped/$f" ] || { echo "Unexpected release layout: missing $f" >&2; exit 1; }
done

rm -rf release
mv "$tmp/unzipped/release" release
echo "Downloaded $URL"
echo "release/ contains: $(ls release | tr '\n' ' ')"
