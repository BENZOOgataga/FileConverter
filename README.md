# FileConverter

This project provides a self-hosted file conversion service.

## Features
- Simple web interface for converting files between many formats
- Backend API for programmatic conversions

## Recommended usage

Use the web interface by running the Flask server and visiting `http://localhost:5000`. Upload your file, choose the desired output format, and download the converted file.

Advanced users can interact with the `/convert` API endpoint directly using `curl` or other tools.

## Running the server

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure `ffmpeg` is installed on your system for audio and video conversions.
3. Start the server:
   ```bash
   python app.py
   ```

## API

**POST /convert**

Fields:
- `file`: uploaded file
- `target_format`: extension of the desired output format (e.g. `jpg`)

The converted file is returned as a download.

