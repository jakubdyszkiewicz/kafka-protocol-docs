#!/usr/bin/env python3
"""
Scrape Kafka protocol error codes from the official documentation
"""

import urllib.request
import json
import re
from html.parser import HTMLParser


class ErrorCodeTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_thead = False
        self.in_tbody = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.current_cell = ""
        self.headers = []
        self.rows = []
        self.found_error_table = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'thead' and self.in_table:
            self.in_thead = True
        elif tag == 'tbody' and self.in_table:
            self.in_tbody = True
        elif tag == 'tr' and (self.in_thead or self.in_tbody):
            self.in_row = True
            self.current_row = []
        elif tag in ['th', 'td'] and self.in_row:
            self.in_cell = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
            self.in_thead = False
            self.in_tbody = False
        elif tag == 'thead':
            self.in_thead = False
        elif tag == 'tbody':
            self.in_tbody = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row:
                if self.in_thead or (not self.headers and len(self.current_row) == 4):
                    # Check if this looks like the error table header
                    if any('error' in cell.lower() for cell in self.current_row):
                        self.headers = self.current_row
                        self.found_error_table = True
                elif self.found_error_table and len(self.current_row) == 4:
                    self.rows.append(self.current_row)
        elif tag in ['th', 'td'] and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data


def fetch_error_codes():
    """Fetch the error codes page from Kafka documentation"""
    url = "https://kafka.apache.org/protocol"
    print(f"Fetching error codes from {url}...")

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Kafka Protocol Docs Error Code Scraper')

        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"Error fetching page: {e}")
        return None


def parse_error_codes(html):
    """Parse the HTML to extract error codes"""
    parser = ErrorCodeTableParser()
    parser.feed(html)

    error_codes = []

    print(f"Found {len(parser.rows)} rows in error codes table")

    for row in parser.rows:
        if len(row) >= 4:
            # Clean up the retriable field
            retriable_text = row[2].lower().strip()
            retriable = retriable_text == 'true' or retriable_text == 'yes'

            # Parse the code
            code_text = row[1].strip()
            try:
                code = int(code_text)
            except ValueError:
                code = code_text

            error_code = {
                "error": row[0].strip(),
                "code": code,
                "retriable": retriable,
                "description": row[3].strip()
            }
            error_codes.append(error_code)

    return error_codes


def save_to_json(error_codes, filename='error_codes.json'):
    """Save error codes to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(error_codes, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(error_codes)} error codes to {filename}")


def main():
    print("Kafka Protocol Error Codes Scraper")
    print("=" * 50)

    # Fetch the page
    html = fetch_error_codes()
    if not html:
        print("Failed to fetch the page")
        return

    # Parse error codes
    error_codes = parse_error_codes(html)

    if not error_codes:
        print("No error codes found. The page structure might have changed.")
        return

    # Save to JSON
    save_to_json(error_codes)

    # Print summary
    print("\nSample error codes:")
    for error_code in error_codes[:5]:
        print(f"  {error_code['code']}: {error_code['error']} - {error_code['retriable']}")


if __name__ == "__main__":
    main()
