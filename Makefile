PYTHON=python3
VENV_DIR=venv
ACTIVATE=$(VENV_DIR)/bin/activate
REQS=requirements.txt

run:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv venv && echo "Virtual environment created in $(VENV_DIR)" && echo ""
	@echo "Installing dependencies..."
	@. $(ACTIVATE) && pip install -r $(REQS) && echo "Dependencies installed successfully!" && echo ""
	@. $(ACTIVATE) && $(PYTHON) run_pipeline.py && echo "" && echo "Done!"

clean:
	@rm -rf $(VENV_DIR) __pycache__
	@rm -rf dataset/*.json 
