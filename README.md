# Kafka Protocol Messages Viewer

A simple web-based viewer to display Kafka protocol message pairs (Request/Response) side-by-side.

## Features

- Automatically loads all JSON files from the `messages/` directory
- Pairs Request and Response messages together
- Strips JSON comments (both `//` and `/* */` style)
- Pretty-prints JSON for easy reading
- Dark theme optimized for readability
- Responsive design (side-by-side on desktop, stacked on mobile)

## Usage

### Local Development

1. Start a simple static server:
   ```bash
   python3 -m http.server
   ```

2. Open your browser to: http://localhost:8000 (or the port printed in your terminal)

3. The page will automatically load and display all message pairs from the `messages/` directory

### Hosting Online

The viewer now loads its manifest directly from `messages.json`, so it works on any static host (GitHub Pages, Netlify, Vercel, etc.).

- Keep the `messages.json` manifest in sync with the files in `messages/`.
- Deploy the repository contents (including `messages/` and `messages.json`) to your static hosting provider.
- Optional: If you prefer a dynamic environment, you can still run `server.py`, which serves the same assets and remains useful for local experimentation.

## File Structure

```
kafka-protocol-docs/
├── index.html          # Main viewer page
├── server.py           # Python web server
├── messages/           # Directory containing message JSON files
│   ├── ProduceRequest.json
│   ├── ProduceResponse.json
│   └── ...more message files
└── README.md          # This file
```

## Adding New Messages

Simply add new JSON files to the `messages/` directory following the naming convention:
- `[MessageName]Request.json`
- `[MessageName]Response.json`

The viewer will automatically pair them based on the message name and display them side-by-side.

## Technologies Used

- **Frontend**: Plain HTML5, CSS3 (Grid layout), Vanilla JavaScript
- **Backend**: Python 3 HTTP server (for local development)
- **No frameworks or dependencies** - just modern web standards

## Requirements

- Python 3.x (for local server)
- Modern web browser with JavaScript enabled
