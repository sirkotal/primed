.PHONY: all

all:
	@echo "Please specify a target: install, run, clean"

PYTHON=python3
VENV_DIR=venv
ACTIVATE=$(VENV_DIR)/bin/activate
REQS=data_pipeline/requirements.txt

install:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv venv && echo "Virtual environment created in $(VENV_DIR)" && echo ""
	@echo "Installing dependencies..."
	@. $(ACTIVATE) && pip install -r $(REQS) && echo "" && echo "Dependencies installed successfully!" && echo ""

run:
	@. $(ACTIVATE) && $(PYTHON) data_pipeline/main.py && echo "" && echo "Done!"

clean:
	@rm -rf $(VENV_DIR) __pycache__
	@rm -rf data_pipeline/__pycache__
	@rm -rf venv
	@rm -rf dataset/output/*.json
	# @rm -rf dataset/output/*.db (not using this now so don't remove it)
