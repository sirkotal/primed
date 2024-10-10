#!/bin/sh

# Change to the data_pipeline directory
cd data_pipeline || { echo "Failed to change directory"; exit 1; }
echo "Changed directory to $(pwd)"

# Create a Python virtual environment
echo "\n\nCreating python virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "\n\nActivating virtual environment..."
. venv/bin/activate

# Install required packages
echo "\n\nInstalling dependencies..."
pip install -r requirements.txt

# Run the Python function from the module
echo "\n\nParsing drug details..."
python3 -c 'from to_json import parse_drug_details; parse_drug_details()'

echo "\nParsing sicknesses..."
python3 -c 'from to_json import parse_sicknesses; parse_sicknesses()'

echo "\nParsing drug reviews..."
python3 -c 'from to_json import parse_drug_reviews; parse_drug_reviews()'

echo "\n\nDo you wish to download pharmaceutical company data from Wikipedia? (may take 1-5 minutes)"
while true; do
    read -p "$1 (y/n): " answer
    case $answer in
        [Yy]* ) return 0;;  # User answered "yes"
        [Nn]* ) return 1;;  # User answered "no"
        * ) echo "Please answer yes or no.";;  # Invalid input
    esac
done

echo "\nParsing drug reviews..."
python3 -c 'from to_json import parse_drug_reviews; parse_drug_reviews()'

echo "Done!"
