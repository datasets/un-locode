all: requirements download prepare process 

requirements:
	pip install -r scripts/requirements.txt

download:
	python scripts/download_loc.py

prepare:
	bash scripts/prepare_edition_mdb.sh $(shell find . -maxdepth 1 -name "loc*[0-9]*mdb.zip" -print -quit)

process:
	python scripts/prepare.py

clean:
	find . -maxdepth 1 -name "*.zip" -exec rm -f {} +

.PHONY: clean
