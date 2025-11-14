# Quick Start Guide

Get up and running with SKF PDF Viewer in minutes!

## Installation

### Step 1: Install Python

**Windows:**
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify: Open Command Prompt and run `python --version`

**Mac:**
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
# Install Python 3
sudo apt update
sudo apt install python3 python3-pip

# Verify
python3 --version
```

### Step 2: Clone or Download the Repository

**Option A: Using Git**
```bash
git clone https://github.com/RobertFWoo/SKF_PDF_Viewer.git
cd SKF_PDF_Viewer
```

**Option B: Download ZIP**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in the extracted folder

### Step 3: Install Dependencies

**Linux/Mac:**
```bash
pip3 install -r requirements.txt
```

**Windows:**
```cmd
pip install -r requirements.txt
```

This installs:
- PyQt6 (GUI framework)
- PyMuPDF (PDF rendering)
- Pillow (Image processing)

### Step 4: Launch the Application

**Linux/Mac:**
```bash
# Option 1: Using the launcher script
./launch.sh

# Option 2: Direct Python execution
python3 pdf_viewer.py
```

**Windows:**
```cmd
REM Option 1: Using the launcher script
launch.bat

REM Option 2: Direct Python execution
python pdf_viewer.py
```

## First Use

### Opening Your First PDF

1. **File Menu**: Click `File > Open PDF...` or press `Ctrl+O`
2. **Drag & Drop**: Simply drag a PDF file from your file manager into the window
3. Browse to a PDF file and click "Open"

The PDF will open in a new tab and remember your position automatically!

### Basic Navigation

**Moving Between Pages:**
- Click the toolbar buttons: "◀ Previous" or "Next ▶"
- Press `Left Arrow` or `Right Arrow`
- Press `Page Up` or `Page Down`
- Click a thumbnail in the sidebar

**Zooming:**
- Click toolbar buttons: "Zoom -" or "Zoom +"
- Press `Ctrl++` to zoom in
- Press `Ctrl+-` to zoom out
- Press `Ctrl+0` to reset to 100%

**Fullscreen Mode:**
- Press `F11` to enter fullscreen
- Press `F11` or `Escape` to exit fullscreen

### Working with Multiple PDFs

**Opening Additional PDFs:**
1. Use `File > Open PDF...` or `Ctrl+O`
2. Or drag another PDF into the window
3. A new tab appears for each PDF

**Switching Between Tabs:**
- Click on the tab you want to view
- Press `Ctrl+Tab` for next tab
- Press `Ctrl+Shift+Tab` for previous tab
- Press `Ctrl+1` through `Ctrl+9` to jump to tabs 1-9

**Closing Tabs:**
- Click the X button on the tab
- Press `Ctrl+W` to close current tab

## Quick Tips

### The Sidebar

Press `F9` to show/hide the thumbnail sidebar. The sidebar shows:
- Thumbnails of all pages in the current PDF
- Click any thumbnail to jump to that page
- Current page is highlighted

### Recent Folders

After opening a PDF, the folder appears in `File > Recent Folders` for quick access to your frequently used directories.

### Keyboard Shortcuts Cheat Sheet

Print this for reference:

```
┌─────────────────────────────────────────┐
│          ESSENTIAL SHORTCUTS            │
├─────────────────┬───────────────────────┤
│ Ctrl+O          │ Open PDF              │
│ Ctrl+W          │ Close tab             │
│ Ctrl+Q          │ Exit                  │
│ F11             │ Fullscreen toggle     │
│ F9              │ Sidebar toggle        │
│ F1              │ Help                  │
├─────────────────┼───────────────────────┤
│ Left/Right      │ Previous/Next page    │
│ Page Up/Down    │ Previous/Next page    │
│ Ctrl+Tab        │ Next tab              │
│ Ctrl+Shift+Tab  │ Previous tab          │
│ Ctrl+1-9        │ Jump to tab 1-9       │
├─────────────────┼───────────────────────┤
│ Ctrl++          │ Zoom in               │
│ Ctrl+-          │ Zoom out              │
│ Ctrl+0          │ Reset zoom            │
└─────────────────┴───────────────────────┘
```

### Memory Feature

The viewer remembers:
- **Page positions** for the last 100 PDFs you opened
- **Window size** and position
- **Sidebar visibility** preference
- **Recent folders** (last 10)

Next time you open a PDF, it automatically jumps to where you left off!

## Troubleshooting

### "Module not found" Error

**Problem:** `ModuleNotFoundError: No module named 'PyQt6'`

**Solution:**
```bash
# Reinstall dependencies
pip3 install -r requirements.txt --upgrade
```

### "Permission denied" Error

**Problem:** `./launch.sh: Permission denied`

**Solution:**
```bash
# Make the script executable
chmod +x launch.sh
```

### Application Won't Start

**Check Python version:**
```bash
python3 --version
```
You need Python 3.8 or higher.

**Check dependencies:**
```bash
python3 -c "import PyQt6; print('PyQt6 OK')"
python3 -c "import fitz; print('PyMuPDF OK')"
```

### PDF Won't Open

**Possible causes:**
1. File is corrupted - try opening in another PDF reader
2. File is password-protected - not currently supported
3. File permissions - check you have read access

## Next Steps

### Customize Your Experience

Edit settings in `~/.skf_pdf_viewer/settings_<DEVICE>.json`:

```json
{
  "zoom_level": 125,           // Start at 125% zoom
  "sidebar_visible": true,     // Show sidebar on startup
  "stream_deck_port": 8765     // Stream Deck API port
}
```

See [CONFIGURATION.md](CONFIGURATION.md) for all options.

### Set Up OneDrive Sync

To sync your PDF positions across devices:

1. Install OneDrive
2. Ensure it's syncing to the default location
3. The app automatically uses OneDrive if available
4. Your PDF positions now sync across all your devices!

### Stream Deck Integration

If you have an Elgato Stream Deck:

1. The HTTP server starts automatically on port 8765
2. Configure buttons to send HTTP requests
3. See [STREAM_DECK.md](STREAM_DECK.md) for detailed setup

Example Stream Deck button:
```
Action: Website
URL: http://localhost:8765/next
```

## Getting Help

- **Full documentation**: See [README.md](README.md)
- **Configuration guide**: See [CONFIGURATION.md](CONFIGURATION.md)
- **Stream Deck setup**: See [STREAM_DECK.md](STREAM_DECK.md)
- **Keyboard shortcuts**: Press `F1` in the app
- **Report issues**: Open an issue on GitHub

## What's Next?

Now that you're up and running, explore these features:

1. **Open multiple PDFs** and use `Ctrl+Tab` to switch between them
2. **Try fullscreen mode** with `F11` for distraction-free reading
3. **Use the sidebar** (press `F9`) to see all pages at once
4. **Set up OneDrive** to sync your reading positions across devices
5. **Configure Stream Deck** if you have one for ultimate control

Enjoy your new PDF viewer! 📚
