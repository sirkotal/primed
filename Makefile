.PHONY: all

all:
	@echo "Please specify a target: install, run, clean"

PYTHON = python3
VENV_DIR = venv
ACTIVATE = $(VENV_DIR)/bin/activate
REQS = data_pipeline/requirements.txt
LIB_NAME = wordninja
PATCH_FILE = ./patches/split_fix.patch

install:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR) && echo "Virtual environment created in $(VENV_DIR)" && echo ""
	@echo "Installing dependencies..."
	@. $(ACTIVATE) && pip install -r $(REQS) && echo "" && echo "Dependencies installed successfully!" && echo ""
	@echo "Checking for $(LIB_NAME)..." && \
		if . $(ACTIVATE) && python -c 'import $(LIB_NAME)' 2>/dev/null; then \
			LIB_PATH=$$(python -c 'import $(LIB_NAME); import os; print(os.path.dirname($(LIB_NAME).__file__))') && \
			echo "Applying patch to $$LIB_PATH..." && \
			patch -p0 -d $$LIB_PATH < $(PATCH_FILE) && echo "Patch applied successfully"; \
		else \
			echo "$(LIB_NAME) not found. Patch not applied."; \
			exit 1; \
		fi
	@echo "Done!"

uninstall:
	@rm -rf $(VENV_DIR) __pycache__
	@rm -rf data_pipeline/__pycache__
	@rm -rf venv

run:
	@. $(ACTIVATE) && $(PYTHON) data_pipeline/main.py && echo "" && echo "Done!"

clean:
	@rm -rf $(VENV_DIR) __pycache__
	@rm -rf data_pipeline/__pycache__
	@rm -rf venv
	@rm -rf dataset/output/*.json
	# @rm -rf dataset/output/*.db (not using this now so don't remove it)

down:
	docker compose -f docker/docker-compose.yml down --remove-orphans -v

up:
	docker compose -f docker/docker-compose.yml up -d

core:
	docker exec -it solr_pri bin/solr create_core -c primed-data

schema_simple:
	curl -X POST -H 'Content-type:application/json' --data-binary "@docker/data/primed_schema_simple.json" http://localhost:8983/solr/primed-data/schema

schema_advanced:
	curl -X POST -H 'Content-type:application/json' --data-binary "@docker/data/primed_schema_advanced.json" http://localhost:8983/solr/primed-data/schema
	
schema_semantic:
	curl -X POST -H 'Content-type:application/json' --data-binary "@docker/data/semantic_primed_schema_advanced.json" http://localhost:8983/solr/primed-data/schema
	
data:
	curl -X POST -H 'Content-type:application/json' --data-binary "@docker/data/combined_drug_data.json" http://localhost:8983/solr/primed-data/update\?commit\=true

trec_eval:
	git clone https://github.com/usnistgov/trec_eval.git src/trec_eval
	cd eval/trec_eval && make
	cd ../..

query_simple:
	$(PYTHON) docker/request_simple.py

query_advanced:
	$(PYTHON) docker/request_advanced.py

query_semantic:
	$(PYTHON) docker/request_semantic.py