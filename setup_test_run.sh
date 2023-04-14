#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Run the tests with coverage
coverage run -m pytest test_main.py -vv

# Display the coverage report
coverage report -m

# Run the web crawler
python main.py "https://www.example.com" --max_domains 500
