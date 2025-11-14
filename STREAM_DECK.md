# Stream Deck Integration Examples

This document provides examples for integrating SKF PDF Viewer with Elgato Stream Deck.

## Setup

1. Start the PDF Viewer application
2. The HTTP server will automatically start on port 8765
3. Configure Stream Deck buttons to send HTTP requests

## Stream Deck Button Configuration

### Method 1: Using the "Website" Action

1. Drag a "Website" action to your Stream Deck
2. Set the URL to one of the commands below
3. Configure the button appearance (icon, title)
4. Save

### Method 2: Using the "System: Open" Action

1. Drag "System: Open" action to your Stream Deck
2. Set the app/file to: `curl`
3. Set arguments to: `http://localhost:8765/COMMAND`

## Available Commands

### Navigation Commands

**Next Page**
```
URL: http://localhost:8765/next
Button Label: Next Page
Icon: →
```

**Previous Page**
```
URL: http://localhost:8765/prev
Button Label: Previous
Icon: ←
```

### Zoom Commands

**Zoom In**
```
URL: http://localhost:8765/zoom_in
Button Label: Zoom In
Icon: +
```

**Zoom Out**
```
URL: http://localhost:8765/zoom_out
Button Label: Zoom Out
Icon: -
```

### View Commands

**Toggle Fullscreen**
```
URL: http://localhost:8765/fullscreen
Button Label: Fullscreen
Icon: ⛶
```

### Tab Commands

**Next Tab**
```
URL: http://localhost:8765/next_tab
Button Label: Next Tab
Icon: ⇥
```

**Previous Tab**
```
URL: http://localhost:8765/prev_tab
Button Label: Prev Tab
Icon: ⇤
```

## Sample Stream Deck Layout

```
┌───────┬───────┬───────┐
│ Prev  │ Next  │ Full  │
│ Page  │ Page  │Screen │
├───────┼───────┼───────┤
│ Zoom  │ Zoom  │       │
│  Out  │  In   │       │
├───────┼───────┼───────┤
│ Prev  │ Next  │       │
│  Tab  │  Tab  │       │
└───────┴───────┴───────┘
```

## Testing the Integration

You can test commands from the command line:

### Linux/Mac
```bash
curl http://localhost:8765/next
curl http://localhost:8765/prev
curl http://localhost:8765/zoom_in
curl http://localhost:8765/fullscreen
```

### Windows (PowerShell)
```powershell
Invoke-WebRequest -Uri http://localhost:8765/next
Invoke-WebRequest -Uri http://localhost:8765/prev
Invoke-WebRequest -Uri http://localhost:8765/zoom_in
```

### Windows (Command Prompt with curl)
```cmd
curl http://localhost:8765/next
curl http://localhost:8765/prev
curl http://localhost:8765/zoom_in
```

## Advanced Configuration

### Custom Port

If port 8765 is already in use, you can change it by editing the settings file:

**Location:**
- Linux/Mac: `~/.skf_pdf_viewer/settings_<HOSTNAME>.json`
- Windows: `%USERPROFILE%\.skf_pdf_viewer\settings_<COMPUTERNAME>.json`

**Edit:**
```json
{
  "stream_deck_port": 8888
}
```

Then restart the application and update your Stream Deck button URLs to use the new port.

### Multiple Instances

If you're running multiple instances of the PDF Viewer, you'll need to configure different ports for each:
1. Start first instance (uses default port 8765)
2. Configure second instance to use port 8766
3. Configure Stream Deck buttons to target the appropriate port

### Remote Control

By default, the server only listens on localhost (127.0.0.1) for security. If you need to control the PDF viewer from another device on your network:

1. This requires modifying the `StreamDeckServer` class in `pdf_viewer.py`
2. Change the bind address from `'localhost'` to `'0.0.0.0'`
3. Update your Stream Deck button URLs to use your computer's IP address
4. Ensure your firewall allows incoming connections on the configured port

**Example for remote control:**
```
http://192.168.1.100:8765/next
```

⚠️ **Security Note:** Opening the server to your network may pose security risks. Only do this on trusted networks.

## Troubleshooting

### "Connection refused" Error

**Cause:** The PDF Viewer is not running or the server didn't start.

**Solution:**
1. Ensure the PDF Viewer application is running
2. Check the console output for any server startup errors
3. Try a different port if 8765 is already in use

### Commands Not Working

**Cause:** Wrong port or URL format

**Solution:**
1. Verify the port in your settings file
2. Ensure URL format is correct: `http://localhost:PORT/COMMAND`
3. Test with curl first before configuring Stream Deck

### Slow Response

**Cause:** Network latency or application load

**Solution:**
1. Ensure the application is not frozen
2. Check system resources (CPU, memory)
3. Close unnecessary PDFs or tabs

## API Response Format

All endpoints return a JSON response:

```json
{
  "status": "ok"
}
```

This can be useful for debugging or building custom integrations.

## Future Enhancements

Potential future API endpoints:
- `/goto/<page>` - Jump to specific page
- `/open/<path>` - Open a specific PDF
- `/close` - Close current tab
- `/status` - Get current state (page number, zoom level, etc.)

If you need these features, please open an issue on GitHub.
