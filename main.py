#!venv/bin/python

import requests
from bs4 import BeautifulSoup
import csv, sys
from urllib.parse import urlparse
from collections import deque
import argparse
from publicsuffixlist import PublicSuffixList


####
#
# WEB Crawler Example Code
# 
# Author: Calvin Schultz, 2023
# On exception, prints error message and exits with status code 1.
####


def extract_links(url):
    """
    Extracts all href links from a given URL.
    :param url: URL to extract links from.
    :return: List of extracted links.
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        return links
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        return []


def extract_domain(url):
    """
    Extracts the domain from a given URL.
    :param url: URL to extract domain from.
    :return: Extracted domain.
    """
    try:
        # Use the publicsuffixlist library to extract the domain
        psl = PublicSuffixList()
        # Parse the URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.split(':')[0]
        tld = psl.publicsuffix(domain)

        # If the domain is the same as the TLD, then the URL is a top-level domain
        if not tld:
            return domain

        # Split the domain and TLD into parts
        domain_parts = domain.split(".")
        tld_parts = tld.split(".")
        
        # If the domain has more parts than the TLD, then the domain is a subdomain
        if len(domain_parts) > len(tld_parts):
            return f"{domain_parts[-(len(tld_parts) + 1)]}.{tld}"
        else:
            return tld
    except Exception as e:
        print(f"Error extracting domain from {url}: {e}")
        sys.exit(1)


def crawl(start_url, max_domains=500):
    """
    Crawls the web starting from a given URL and returns a list of unique domain names.
    :param start_url: Starting URL to begin crawling.
    :param max_domains: Maximum number of unique domains to crawl.
    :return: List of crawled domain names.
    """
    try:
        # Use a set to store the crawled domains
        crawled_domains = set()

        # Use a deque to implement a queue
        
        domain_queue = deque([start_url])
        
        # Keep track of the number of domains crawled
        counter = 0
        
        while domain_queue and len(crawled_domains) < max_domains:
            current_url = domain_queue.popleft()
            domain = extract_domain(current_url)
            counter += 1
            
            if domain not in crawled_domains:
                crawled_domains.add(domain)
                print(f"Queue Size: {len(crawled_domains)} | Crawling [{counter}] {current_url} -> {domain}")
                links = extract_links(current_url)
                
                for link in links:
                    domain_queue.append(link)
                    
        return list(crawled_domains)[:max_domains]
    except Exception as e:
        print(f"Error crawling {start_url}: {e}")
        sys.exit(1)


def save_to_csv(domains, file_name="urls.csv"):
    """
    Saves a list of domains to a CSV file.
    :param domains: List of domain names.
    :param file_name: Name of the CSV file to save the domains.
    :return: None
    """
    try:
        with open(file_name, "w", newline="") as csvfile:
            fieldnames = ['Domain']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for domain in domains:
                writer.writerow({'Domain': domain})
    except Exception as e:
        print(f"Error saving domains to {file_name}: {e}")
        sys.exit(1)


def arguments():
    """
    Parses command line arguments.
    :return: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument("start_url", help="Starting URL to begin crawling")
    parser.add_argument("--max_domains", type=int, default=500, help="Maximum number of unique domains to crawl")
    parser.add_argument("--output_file", default="urls.csv", help="Name of the CSV file to save the domains")

    return parser


if __name__ == "__main__":
    # Parse command line arguments
    parser = arguments()
    args = parser.parse_args()

    # Crawl the web and save the results to a CSV file
    crawled_domains = crawl(args.start_url, args.max_domains)
    save_to_csv(crawled_domains, args.output_file)

