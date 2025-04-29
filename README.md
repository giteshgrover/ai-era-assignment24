# Movie Finder Chrome Extension with FastAPI Backend

This project consists of a Chrome extension that interacts with a FastAPI backend to find movie information and streaming links.

## Setup Instructions

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

3. Start the FastAPI server:
```bash
python app.py
```
The server will run on `http://localhost:8000`

### Chrome Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" in the top right corner
3. Click "Load unpacked" and select the directory containing the extension files
4. The extension should now appear in your Chrome toolbar

## Usage

1. Click the Movie Finder extension icon in your Chrome toolbar
2. Enter your movie query in the search box
3. Click "Search" or press Enter
4. View the movie information and streaming links in the popup

## Project Structure

- `app.py`: FastAPI backend server
- `manifest.json`: Chrome extension configuration
- `popup.html`: Extension popup UI
- `popup.js`: Extension functionality
- `requirements.txt`: Python dependencies
- `movies_functions.py`: Movie-related functions (existing file)

## API Endpoint

The FastAPI server exposes a single endpoint:
- POST `/query`: Accepts a movie query and returns movie information

## Note

Make sure the FastAPI server is running before using the Chrome extension. The extension is configured to connect to `http://localhost:8000` by default.