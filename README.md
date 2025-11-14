# SKF PDF Viewer

A feature-rich desktop PDF viewer with tabbed interface, drag-and-drop support, and comprehensive hotkey navigation.

## Features

### Core Functionality
- **Tabbed Interface**: Open multiple PDFs simultaneously with easy tab management
- **Drag & Drop Support**: Simply drag PDF files into the window to open them
- **Comprehensive Navigation**: Full keyboard and mouse navigation support
- **Fullscreen Mode**: Distraction-free reading with F11 toggle
- **Sidebar Thumbnails**: Visual page navigation with clickable thumbnails
- **Zoom Controls**: Flexible zoom levels from 50% to 300%

### Advanced Features
- **Persistent State Management**: 
  - Remembers page positions for the last 100 PDFs opened
  - Saves window geometry and state
  - Tracks recent folders for quick access
  - Device-specific preferences
  
- **Cross-Device Sync**: 
  - Supports OneDrive for centralized PDF position tracking
  - Maintains device-specific settings locally
  - Seamless experience across multiple computers

- **Stream Deck Integration**: 
  - HTTP API server for external control
  - Control navigation, zoom, and tabs remotely
  - Perfect for presentation setups

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages
- PyQt6 >= 6.6.0 (GUI framework)
- PyMuPDF >= 1.23.0 (PDF rendering)
- Pillow >= 10.0.0 (Image processing)

## Usage

### Starting the Application

```bash
python pdf_viewer.py
```

### Opening PDFs

1. **File Menu**: `File > Open PDF...` or `Ctrl+O`
2. **Drag & Drop**: Drag PDF files directly into the window
3. **Recent Folders**: `File > Recent Folders` for quick access
4. **Command Line**: `python pdf_viewer.py path/to/file.pdf` (future enhancement)

### Keyboard Shortcuts

#### File Operations
- `Ctrl+O` - Open PDF file dialog
- `Ctrl+W` - Close current tab
- `Ctrl+Q` - Exit application

#### Navigation
- `Left Arrow` / `Right Arrow` - Previous/Next page
- `Page Up` / `Page Down` - Previous/Next page
- `Ctrl+Tab` - Switch to next tab
- `Ctrl+Shift+Tab` - Switch to previous tab
- `Ctrl+1` through `Ctrl+9` - Jump to tab 1-9

#### View Controls
- `F11` - Toggle fullscreen mode
- `F9` - Toggle sidebar visibility
- `Ctrl++` - Zoom in
- `Ctrl+-` - Zoom out
- `Ctrl+0` - Reset zoom to 100%
- `Escape` - Exit fullscreen (when in fullscreen)

#### Help
- `F1` - Show keyboard shortcuts reference

### Sidebar Thumbnails

The sidebar displays thumbnails of all pages in the current PDF:
- Click any thumbnail to jump to that page
- Current page is highlighted
- Toggle visibility with `F9` or `View > Toggle Sidebar`
- Sidebar state is preserved between sessions

### Tabbed Interface

- Open multiple PDFs in separate tabs
- Click the X button on tabs to close them
- Drag tabs to reorder (standard tab behavior)
- Tab titles show the PDF filename
- Recently accessed tabs are easier to find

### Fullscreen Mode

Press `F11` to enter fullscreen mode for distraction-free reading:
- Hides menu bar, toolbar, and status bar
- Press `F11` or `Escape` to exit
- All navigation shortcuts remain functional

## Settings and Persistence

### Configuration Files

Settings are stored in:
- **Linux/Mac**: `~/.skf_pdf_viewer/`
- **Windows**: `%USERPROFILE%\.skf_pdf_viewer\`

### Device-Specific Settings
File: `settings_<COMPUTERNAME>.json`

Stores:
- Window geometry and position
- Window state (maximized, etc.)
- Recent folders list
- Sidebar visibility
- Default zoom level
- Stream Deck server port

### Shared Settings (OneDrive Sync)
File: `~/OneDrive/.skf_pdf_viewer/shared_settings.json`

Stores:
- PDF page positions (last 100 PDFs)
- Syncs across all devices with OneDrive

If OneDrive is not available, shared settings are stored locally.

### PDF Position Memory

The viewer remembers the last page you were on for the 100 most recently opened PDFs. When you reopen a PDF, it automatically jumps to where you left off.

## Stream Deck Integration

### Starting the Server

The Stream Deck server starts automatically when the application launches on port 8765 (configurable).

### API Endpoints

Send HTTP GET requests to `http://localhost:8765/<command>`:

- `/next` - Next page
- `/prev` - Previous page
- `/zoom_in` - Increase zoom
- `/zoom_out` - Decrease zoom
- `/fullscreen` - Toggle fullscreen
- `/next_tab` - Switch to next tab
- `/prev_tab` - Switch to previous tab

### Example Stream Deck Configuration

1. Add a "Website" action
2. Set URL to: `http://localhost:8765/next`
3. Configure button appearance
4. Repeat for other commands

### cURL Examples

```bash
# Next page
curl http://localhost:8765/next

# Previous page
curl http://localhost:8765/prev

# Zoom in
curl http://localhost:8765/zoom_in

# Toggle fullscreen
curl http://localhost:8765/fullscreen
```

## Advanced Usage

### OneDrive Setup for Cross-Device Sync

1. Ensure OneDrive is installed and syncing
2. The application automatically detects `~/OneDrive/` directory
3. PDF positions are saved to OneDrive and sync across devices
4. Each device maintains its own window preferences

### Customizing Settings

Edit the settings JSON files directly:

```json
{
  "window_geometry": "...",
  "window_state": "...",
  "recent_folders": [
    "/path/to/folder1",
    "/path/to/folder2"
  ],
  "sidebar_visible": true,
  "zoom_level": 100,
  "stream_deck_port": 8765
}
```

### Multiple Instances

You can run multiple instances of the viewer simultaneously. Each instance:
- Uses the same shared PDF position database
- Maintains independent window states
- Can have different files open

## Troubleshooting

### Application Won't Start

1. Verify Python version: `python --version` (need 3.8+)
2. Check dependencies: `pip install -r requirements.txt`
3. Test PyQt6: `python -c "from PyQt6.QtWidgets import QApplication"`

### PDF Won't Open

1. Verify the file is a valid PDF
2. Check file permissions
3. Try opening in another PDF reader to confirm it's not corrupted

### Stream Deck Not Connecting

1. Check if port 8765 is available: `netstat -an | grep 8765`
2. Verify firewall settings
3. Try changing the port in settings
4. Ensure Stream Deck is on the same network (for remote control)

### Settings Not Persisting

1. Check write permissions in `~/.skf_pdf_viewer/`
2. Verify OneDrive is syncing (if using cross-device sync)
3. Check for file system errors

### Thumbnails Not Loading

1. Large PDFs may take time to generate thumbnails
2. Check system memory availability
3. Try closing other applications

## Development

### Project Structure

```
SKF_PDF_Viewer/
├── pdf_viewer.py          # Main application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

### Key Classes

- `Settings`: Manages configuration and persistence
- `PDFWidget`: Displays individual PDF documents
- `ThumbnailSidebar`: Shows page thumbnails
- `StreamDeckServer`: HTTP server for external control
- `PDFViewerMainWindow`: Main application window

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Acknowledgments

- Built with PyQt6 for the GUI framework
- PDF rendering powered by PyMuPDF (fitz)
- Inspired by modern PDF viewers with a focus on efficiency