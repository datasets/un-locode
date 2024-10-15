all: requirements download prepare process 

requirements:
	pip3 install -r scripts/requirements.txt

download:
	python3 scripts/download_loc.py

prepare:
	bash scripts/prepare_edition_mdb.sh $(shell find . -maxdepth 1 -name "loc*[0-9]*mdb.zip" -print -quit)

process:
	python3 scripts/prepare.py

clean:
	find . -maxdepth 1 -name "*.zip" -exec rm -f {} +

.PHONY: clean
