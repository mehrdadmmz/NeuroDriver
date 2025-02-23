# Define variables for clarity and easy customization
PYTHON      = python3
PIP         = pip3
VENV_DIR    = venv

# Declare targets that don't represent files
.PHONY: help venv install run test lint clean

# Display usage information
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  venv    - Create a virtual environment"
	@echo "  install - Install dependencies from requirements.txt"
	@echo "  run     - Run the main program (main.py)"
	@echo "  test    - Run tests using pytest"
	@echo "  lint    - Lint the code using flake8"
	@echo "  clean   - Remove virtual environment and __pycache__ directories"

# Create a virtual environment if it doesn't exist
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Virtual environment created in $(VENV_DIR)"; \
	else \
		echo "Virtual environment already exists."; \
	fi

# Install dependencies using pip inside the virtual environment
install: venv
	$(VENV_DIR)/bin/$(PIP) install -r requirements.txt

# Run your main Python program
run: venv
	$(VENV_DIR)/bin/$(PYTHON) training.py

# Run tests using pytest 
test: venv
	$(VENV_DIR)/bin/$(PYTHON) test.py

# Lint your code with flake8 (or another linter of your choice)
lint: venv
	$(VENV_DIR)/bin/flake8 .

# Clean up temporary files and remove the virtual environment if needed
clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleaned up virtual environment and __pycache__ directories."
