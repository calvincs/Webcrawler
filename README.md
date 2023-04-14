# Web Crawler

This project is a simple web crawler that starts from a given URL and crawls the web, collecting a list of unique domain names. The results are saved to a CSV file.

## Features

- Crawls the web starting from a specified URL
- Extracts unique domain names from the crawled URLs
- Limits the number of domains collected (default: 500)
- Saves the collected domains to a CSV file
- Supports optional command-line arguments for customization

## Requirements

- Python 3.6 or higher
- `requests`
- `beautifulsoup4`
- `publicsuffixlist`
- `coverage` (for running tests with coverage)

## Installation

1. Clone this repository:

   ```ruby
   git clone https://github.com/calvincs/Webcrawler.git
   ```

2. Change to the project directory:
   ```ruby
   cd Webcrawler
   ```

3. Test and Run script:
   ```ruby
   chmod +x setup_test_run.sh; ./setup_test_run.sh
   ```

## Usage

To run the web crawler, execute the following command:

   ```ruby
   python main.py <start_url> [--max_domains <max_domains>] [--output_file <output_file>]
   ```

   - `<start_url>`: The starting URL for the web crawler (required).
   - `<max_domains>`: The maximum number of unique domains to crawl (optional, default: 500).
   - `<output_file>`: The name of the CSV file where the domains will be saved (optional, default: "urls.csv").

