#!/usr/bin/env python3
"""
Generate a static list of message files for static hosting (e.g., GitHub Pages)
"""

import os
import json

MESSAGES_DIR = "messages"
OUTPUT_FILE = "messages.json"

def generate_messages_list():
    """Generate a JSON file with the list of all message files"""
    files = []

    if os.path.exists(MESSAGES_DIR):
        for filename in os.listdir(MESSAGES_DIR):
            if filename.endswith('.json'):
                files.append(filename)

    # Sort the files for consistency
    files.sort()

    # Write to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2)

    print(f"Generated {OUTPUT_FILE} with {len(files)} message files")

if __name__ == "__main__":
    generate_messages_list()
