# Define virtual environment directory variables
VENV_DIR = venv

# 'init' Goal: Initialize the virtual environment and install dependency packages
init: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

# 'run' Goal: Run the main program
run: $(VENV_DIR)/bin/activate
	./start.sh\

# 'clean' Goal: Delete virtual environment
clean:
	rm -rf $(VENV_DIR)
	@echo "Virtual environment cleaned."

# If the virtual environment directory does not exist, create a virtual environment
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created. Run 'make init' to install dependencies."


# make init  # Initialize virtual environment and install dependencies
# make run   # Run Project
# make clean # Clean up virtual environment
