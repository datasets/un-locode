all: prepare process

prepare:
	@test -d release || (echo "Error: release/ not found. Download from https://unece.org/trade/cefact/UNLOCODE-Download and extract here."; exit 1)
	zip -j loc_mdb.zip "release/UNLOCODE CodeList.mdb"
	bash scripts/prepare_edition_mdb.sh loc_mdb.zip
	rm -f loc_mdb.zip

process:
	zip -j loc0csv.zip release/csv/*.csv
	python3 scripts/prepare.py
	rm -f loc0csv.zip

clean:
	find . -maxdepth 1 -name "*.zip" -exec rm -f {} +

.PHONY: all prepare process clean
