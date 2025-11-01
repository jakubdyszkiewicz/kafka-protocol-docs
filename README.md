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

1. Start the web server:
   ```bash
   python3 server.py
   ```

2. Open your browser to: http://localhost:8000

3. The page will automatically load and display all message pairs from the `messages/` directory

### Hosting Online

When deploying to a web host, you have several options:

#### Option 1: Static Hosting (GitHub Pages, Netlify, Vercel, etc.)

You'll need to generate a static list of files since the API endpoint won't work on static hosts:

1. Create a `messages.json` file with the list of your JSON files
2. Modify `index.html` to read from `messages.json` instead of `/api/messages`

#### Option 2: Dynamic Hosting (Heroku, Railway, etc.)

Simply deploy the `server.py` along with your HTML and messages files. The server will work as-is.

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
