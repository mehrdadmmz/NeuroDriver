# Define variables for clarity and easy customization
PYTHON      = python3
PIP         = pip3
VENV_DIR    = venv
TRAIN_SCRIPT = scripts/training.py
TEST_SCRIPT  = scripts/testdrive.py

# Declare targets that don't represent files
.PHONY: help venv install run train test lint clean

# Display usage information
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  venv    - Create a virtual environment"
	@echo "  install - Install dependencies from requirements.txt"
	@echo "  run     - Run the main training script"
	@echo "  train   - Remove brain.json and then train from scratch"
	@echo "  test    - Run the testdrive on track 4"
	@echo "  lint    - Lint the code using flake8"
	@echo "  clean   - Remove virtual environment, brain.json, and __pycache__ directories"

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

# Run your main Python program (default to training script)
run: venv
	$(VENV_DIR)/bin/$(PYTHON) $(TRAIN_SCRIPT)

# Remove brain.json and then train from scratch
train: clean_brain run

# Test (the script that uses route 4)
test: venv
	$(VENV_DIR)/bin/$(PYTHON) $(TEST_SCRIPT)

# Lint your code with flake8 (or another linter of your choice)
lint: venv
	$(VENV_DIR)/bin/flake8 .

# Clean up the virtual environment, brain.json, and __pycache__ directories
clean: clean_brain
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleaned up virtual environment and __pycache__ directories."

# Separate target to clean brain.json (without removing venv)
clean_brain:
	rm -f brain.json
	@echo "Removed brain.json (if it existed)."
