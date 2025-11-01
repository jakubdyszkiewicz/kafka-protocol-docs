# Kafka Protocol Messages Viewer

A simple web-based viewer to display Kafka protocol message pairs (Request/Response) side-by-side.
This repo is 100% vibecoded. I did not edit a single file manually other than this README.md.

## Why?

Lately I've been working quite a lot with the Kafka protocol.
While I appreciate the Kafka contributors for creating descriptive docs at https://kafka.apache.org/protocol, that site is hard to navigate.
I wanted an easy way to explore Kafka protocol messages and error codes using only my keyboard.

## Usage

Go to https://kafka.dyszkiewicz.me, which is hosted via GitHub Pages.

### Running locally

Clone the repo, then run
```
cd docs
python3 -m http.server 8000
```
or use any other static file server.

## Keeping messages up to date

The Kafka protocol is constantly evolving. To keep it up to date, two Python scripts pull the latest messages from the Kafka repository.
On top of that, a GitHub Actions workflow creates a PR on a daily schedule.
