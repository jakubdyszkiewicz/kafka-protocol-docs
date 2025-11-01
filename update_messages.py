#!/usr/bin/env python3
"""
Update Kafka protocol message files from the official Apache Kafka repository
"""

import os
import sys
import json
import urllib.request
import urllib.error

GITHUB_API_URL = "https://api.github.com/repos/apache/kafka/contents/clients/src/main/resources/common/message"
RAW_GITHUB_URL = "https://raw.githubusercontent.com/apache/kafka/trunk/clients/src/main/resources/common/message"
MESSAGES_DIR = "messages"

def fetch_file_list():
    """Fetch the list of files from GitHub API"""
    print(f"Fetching file list from {GITHUB_API_URL}...")

    try:
        req = urllib.request.Request(GITHUB_API_URL)
        req.add_header('User-Agent', 'Kafka Protocol Docs Updater')

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        print(f"Error fetching file list: {e}")
        sys.exit(1)

def download_file(filename):
    """Download a single file from GitHub"""
    url = f"{RAW_GITHUB_URL}/{filename}"
    filepath = os.path.join(MESSAGES_DIR, filename)

    print(f"  Downloading {filename}...")

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Kafka Protocol Docs Updater')

        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"    Error downloading {filename}: {e}")
        return False

def clean_old_files():
    """Remove all existing JSON files from messages directory"""
    if not os.path.exists(MESSAGES_DIR):
        os.makedirs(MESSAGES_DIR)
        return

    print(f"Cleaning old files from {MESSAGES_DIR}/...")
    for filename in os.listdir(MESSAGES_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(MESSAGES_DIR, filename)
            os.remove(filepath)
            print(f"  Removed {filename}")

def main():
    print("Kafka Protocol Messages Updater")
    print("=" * 50)

    # Clean old files
    clean_old_files()

    # Fetch file list from GitHub
    files = fetch_file_list()

    # Filter for Request.json and Response.json files
    message_files = [
        f['name'] for f in files
        if f['type'] == 'file' and
        (f['name'].endswith('Request.json') or f['name'].endswith('Response.json'))
    ]

    print(f"\nFound {len(message_files)} message files to download")
    print("=" * 50)

    # Download each file
    success_count = 0
    for filename in sorted(message_files):
        if download_file(filename):
            success_count += 1

    print("=" * 50)
    print(f"\nDownload complete!")
    print(f"Successfully downloaded: {success_count}/{len(message_files)} files")
    print(f"Files saved to: {os.path.abspath(MESSAGES_DIR)}/")

if __name__ == "__main__":
    main()
