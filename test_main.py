#!venv/bin/python

import pytest
import tempfile
import csv, os
import responses
from .main import *


def test_extract_domain():
    """
        Tests the extract_domain function.
    """

    assert extract_domain("https://www.google.com/email.asp") == "google.com"
    assert extract_domain("http://google.com/?email=someemail@gmail.com") == "google.com"
    assert extract_domain("https://subdomain.example.com/path?query=param") == "example.com"
    assert extract_domain("http://another-example.co.uk") == "another-example.co.uk"
    assert extract_domain("https://www.multiple-levels.subdomain.example.com") == "example.com"
    assert extract_domain("ftp://ftp.example.com") == "example.com"
    assert extract_domain("https://example.com:8080") == "example.com"


def test_crawl():
    """
        Tests the crawl function.
    """

    start_url = "https://www.example.com"
    max_domains = 10
    domains = crawl(start_url, max_domains)
    assert len(domains) == max_domains
    assert "example.com" in domains


def test_save_to_csv():
    """
    Tests the save_to_csv function.
    """
    
    domains = ["example.com", "google.com", "test.com"]

    # Create a temporary file to save the CSV data
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_csv:
        temp_csv_path = tmp_csv.name

    # Save the domains to the temporary CSV file
    save_to_csv(domains, temp_csv_path)

    # Read the temporary CSV file and verify the contents
    with open(temp_csv_path, mode="r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        fieldnames = csv_reader.fieldnames
        assert fieldnames == ["Domain"]
        
        read_domains = [row["Domain"] for row in csv_reader]
        assert read_domains == domains

    # Clean up the temporary CSV file
    os.remove(temp_csv_path)


def test_extract_links():
    """
        Tests the extract_links function.
    """

    test_url = "https://www.example.com"
    test_html = '''
    <html>
        <body>
            <a href="https://www.example.com/link1">Link 1</a>
            <a href="https://sub.google.com/link2">Link 2</a>
            <a href="ftp://foxnews.com/link3">Link 3</a>
        </body>
    </html>
    '''
    
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, test_url, body=test_html, status=200)
        links = extract_links(test_url)

    expected_links = [
        "https://www.example.com/link1",
        "https://sub.google.com/link2",
        "ftp://foxnews.com/link3",
    ]

    assert links == expected_links


def test_arg_parser():
    """
        Tests the arguments function.
    """

    parser = arguments()

    test_args = ["https://www.example.com", "--max_domains", "300", "--output_file", "test_urls.csv"]
    args = parser.parse_args(test_args)

    assert args.start_url == "https://www.example.com"
    assert args.max_domains == 300
    assert args.output_file == "test_urls.csv"