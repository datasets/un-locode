all: download prepare process

download:
	$(eval LATEST_TAG := $(shell curl -sL "https://opensource.unicc.org/api/v4/projects/un%2Funece%2Funcefact%2Fvocab-locode/repository/tags?per_page=1" | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['name'])"))
	curl -L -o release.zip "https://opensource.unicc.org/un/unece/uncefact/vocab-locode/-/jobs/artifacts/$(LATEST_TAG)/download?job=package-release"
	unzip -o release.zip
	rm release.zip

prepare:
	@test -d release || (echo "Error: release/ not found. Download from https://unece.org/trade/cefact/UNLOCODE-Download and extract here."; exit 1)
	zip -j loc_mdb.zip "release/UNLOCODE CodeList.mdb"
	bash scripts/prepare_edition_mdb.sh loc_mdb.zip
	rm -f loc_mdb.zip

process:
	zip -j loc0csv.zip release/csv/*.csv
	.venv/bin/python3.12 scripts/prepare.py
	rm -f loc0csv.zip

clean:
	find . -maxdepth 1 -name "*.zip" -exec rm -f {} +

.PHONY: all prepare process clean
