PYTHON=python3
VENV_DIR=venv
ACTIVATE=. $(VENV_DIR)/bin/activate
REQS=requirements.txt

run:
	@$(PYTHON) -m venv venv
	@echo "Virtual environment created in $(VENV_DIR)"
	@. $(ACTIVATE) && pip install -r $(REQS)
	@. $(ACTIVATE) && $(PYTHON) run_pipeline.py

clean:
	@rm -rf $(VENV_DIR) __pycache__
	@rm -rf dataset/*.json 
