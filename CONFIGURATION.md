# Configuration Guide

This guide explains all configuration options and how to customize SKF PDF Viewer.

## Configuration Files

### Location

Settings are stored in platform-specific locations:

**Linux/Mac:**
```
~/.skf_pdf_viewer/
├── settings_<HOSTNAME>.json      # Device-specific settings
└── shared_settings.json           # PDF positions (local copy)
```

**Windows:**
```
%USERPROFILE%\.skf_pdf_viewer\
├── settings_<COMPUTERNAME>.json   # Device-specific settings
└── shared_settings.json            # PDF positions (local copy)
```

**OneDrive (for cross-device sync):**
```
~/OneDrive/.skf_pdf_viewer/
└── shared_settings.json           # PDF positions (synced)
```

## Settings File Format

### Device-Specific Settings

File: `settings_<DEVICE>.json`

```json
{
  "window_geometry": "hex_encoded_string",
  "window_state": "hex_encoded_string",
  "recent_folders": [
    "/path/to/folder1",
    "/path/to/folder2"
  ],
  "sidebar_visible": true,
  "zoom_level": 100,
  "stream_deck_port": 8765
}
```

#### Options Explained

**window_geometry** (string)
- Hex-encoded window size and position
- Automatically saved when closing the application
- Do not edit manually

**window_state** (string)
- Hex-encoded window state (maximized, toolbar positions, etc.)
- Automatically saved when closing the application
- Do not edit manually

**recent_folders** (array of strings)
- List of recently accessed folders
- Maximum 10 folders
- Newest folders appear first
- Can be edited to add favorite folders

**sidebar_visible** (boolean)
- `true`: Sidebar with thumbnails is visible on startup
- `false`: Sidebar is hidden on startup
- Toggle with F9 key

**zoom_level** (integer)
- Default zoom level percentage
- Range: 50 to 300
- Default: 100
- Affects all newly opened PDFs

**stream_deck_port** (integer)
- Port for Stream Deck HTTP server
- Default: 8765
- Change if port is already in use
- Valid range: 1024-65535

### Shared Settings (PDF Positions)

File: `shared_settings.json`

```json
{
  "pdf_positions": {
    "/full/path/to/document.pdf": {
      "page": 15,
      "timestamp": "2024-11-14T20:30:00.000000"
    },
    "/full/path/to/another.pdf": {
      "page": 3,
      "timestamp": "2024-11-14T19:45:00.000000"
    }
  }
}
```

#### Options Explained

**pdf_positions** (object)
- Maps PDF file paths to their last viewed page
- Automatically updated when navigating PDFs
- Keeps most recent 100 PDFs
- Older entries are automatically removed

**page** (integer)
- Zero-indexed page number
- Page 0 is the first page
- Automatically saved when changing pages

**timestamp** (string)
- ISO 8601 formatted timestamp
- When the PDF was last viewed
- Used to determine oldest entries for cleanup

## Customization Examples

### Change Default Zoom Level

Edit `settings_<DEVICE>.json`:

```json
{
  "zoom_level": 125
}
```

Now all PDFs will open at 125% zoom by default.

### Set Favorite Folders

Edit `settings_<DEVICE>.json`:

```json
{
  "recent_folders": [
    "/home/user/Documents/Work",
    "/home/user/Documents/Personal",
    "/home/user/Downloads",
    "/media/usb/PDFs"
  ]
}
```

These folders will appear in the "Recent Folders" menu.

### Change Stream Deck Port

Edit `settings_<DEVICE>.json`:

```json
{
  "stream_deck_port": 8888
}
```

Restart the application. Update Stream Deck buttons to use the new port.

### Always Start with Sidebar Hidden

Edit `settings_<DEVICE>.json`:

```json
{
  "sidebar_visible": false
}
```

### Clear PDF History

Delete or edit `shared_settings.json`:

```json
{
  "pdf_positions": {}
}
```

This will remove all saved PDF page positions.

## OneDrive Sync Configuration

### Enabling OneDrive Sync

1. Install OneDrive on all devices where you use the PDF viewer
2. Ensure OneDrive is syncing to the default location:
   - Windows: `%USERPROFILE%\OneDrive`
   - Mac: `~/OneDrive`
   - Linux: `~/OneDrive` (using onedrive client)

3. The PDF viewer will automatically detect OneDrive and use it for syncing PDF positions

### Verifying OneDrive Sync

Check if the shared settings file is in OneDrive:

**Windows:**
```cmd
dir %USERPROFILE%\OneDrive\.skf_pdf_viewer\shared_settings.json
```

**Mac/Linux:**
```bash
ls ~/OneDrive/.skf_pdf_viewer/shared_settings.json
```

If the file exists, OneDrive sync is active.

### Disabling OneDrive Sync

If you don't want to use OneDrive sync, simply don't install OneDrive or remove the OneDrive folder. The application will store shared settings locally instead.

### Troubleshooting OneDrive Sync

**PDF positions not syncing between devices:**

1. Verify OneDrive is running and syncing on all devices
2. Check the OneDrive sync status:
   - Look for the OneDrive icon in system tray/menu bar
   - Ensure the folder `.skf_pdf_viewer` is not excluded from sync
3. Manually check if the file was updated:
   ```bash
   # Linux/Mac
   cat ~/OneDrive/.skf_pdf_viewer/shared_settings.json
   ```
4. Wait for OneDrive sync to complete (can take a few minutes)

**Conflict files appearing:**

If you open the same PDF on multiple devices simultaneously, OneDrive may create conflict files. To resolve:

1. Close the PDF viewer on all devices
2. Keep the newest version of `shared_settings.json`
3. Delete conflict copies
4. Restart one PDF viewer at a time

## Advanced Configuration

### Multiple Profiles

To use different settings profiles (e.g., work vs. personal):

1. Create a wrapper script that sets the `COMPUTERNAME` (Windows) or `HOSTNAME` (Linux/Mac) environment variable:

**Linux/Mac:**
```bash
#!/bin/bash
export HOSTNAME="work"
python3 pdf_viewer.py "$@"
```

**Windows:**
```batch
@echo off
set COMPUTERNAME=work
python pdf_viewer.py %*
```

2. Each profile will have its own `settings_<PROFILE>.json` file

### Portable Installation

To make the PDF viewer portable (settings in application directory):

1. Edit `settings.py`
2. Find the `__init__` method of the `Settings` class
3. Change:
   ```python
   self.config_dir = Path.home() / ".skf_pdf_viewer"
   ```
   To:
   ```python
   self.config_dir = Path(__file__).parent / "settings"
   ```

4. Create a `settings` directory next to the application files

Now all settings will be stored with the application.

### Environment Variables

You can override settings using environment variables:

**Change Stream Deck port:**
```bash
# Linux/Mac
export SKF_STREAM_DECK_PORT=9000
python3 pdf_viewer.py

# Windows
set SKF_STREAM_DECK_PORT=9000
python pdf_viewer.py
```

Note: This requires modifying the code to read environment variables. See the Development section.

## Backup and Restore

### Backing Up Settings

**Backup device-specific settings:**
```bash
# Linux/Mac
cp ~/.skf_pdf_viewer/settings_*.json ~/backup/

# Windows
copy %USERPROFILE%\.skf_pdf_viewer\settings_*.json %USERPROFILE%\backup\
```

**Backup PDF positions:**
```bash
# Linux/Mac (if using OneDrive)
cp ~/OneDrive/.skf_pdf_viewer/shared_settings.json ~/backup/

# Linux/Mac (if not using OneDrive)
cp ~/.skf_pdf_viewer/shared_settings.json ~/backup/
```

### Restoring Settings

Simply copy the backup files back to the original location:

```bash
# Linux/Mac
cp ~/backup/settings_*.json ~/.skf_pdf_viewer/
cp ~/backup/shared_settings.json ~/.skf_pdf_viewer/

# Windows
copy %USERPROFILE%\backup\settings_*.json %USERPROFILE%\.skf_pdf_viewer\
copy %USERPROFILE%\backup\shared_settings.json %USERPROFILE%\.skf_pdf_viewer\
```

Restart the PDF viewer to load the restored settings.

## Resetting to Defaults

To reset all settings to defaults:

1. Close the PDF viewer
2. Delete the settings directory:
   ```bash
   # Linux/Mac
   rm -rf ~/.skf_pdf_viewer/
   
   # Windows
   rmdir /s /q %USERPROFILE%\.skf_pdf_viewer
   ```
3. Restart the PDF viewer

A new settings directory with default values will be created.

## Performance Tuning

### For Large PDFs

If working with very large PDFs (1000+ pages), consider:

1. Disable the sidebar:
   ```json
   {
     "sidebar_visible": false
   }
   ```
   
2. This reduces memory usage as thumbnails won't be generated

### For Slow Machines

If the application feels sluggish:

1. Reduce default zoom:
   ```json
   {
     "zoom_level": 80
   }
   ```

2. Lower zoom reduces rendering load

### For Multiple Monitors

The window geometry automatically saves position across monitors. If you frequently move between different monitor setups:

1. Delete `window_geometry` from settings to reset window size
2. The application will open with default dimensions on the primary monitor

## Troubleshooting Configuration Issues

### Settings Not Saving

**Symptoms:** Changes don't persist between sessions

**Causes & Solutions:**
1. **File permissions:** Ensure you have write permission to the settings directory
   ```bash
   # Linux/Mac
   chmod -R u+w ~/.skf_pdf_viewer/
   ```

2. **Disk full:** Check available disk space
   ```bash
   # Linux/Mac
   df -h ~
   
   # Windows
   dir %USERPROFILE%
   ```

3. **Corrupted JSON:** Delete and recreate settings files

### Settings From Wrong Device

**Symptoms:** Window size/position is wrong after switching devices

**Cause:** Device ID detection issue

**Solution:** Manually rename the correct settings file:
```bash
# Find your device name
echo $HOSTNAME  # Linux/Mac
echo %COMPUTERNAME%  # Windows

# Rename to match
mv settings_old.json settings_<YOUR_DEVICE>.json
```

### PDF Positions Lost

**Symptoms:** PDFs don't open at the last viewed page

**Causes & Solutions:**
1. **Shared settings file deleted:** Check if file exists
2. **OneDrive not syncing:** Check OneDrive sync status
3. **File path changed:** PDF positions are stored by full path

If you moved PDFs to a new location, positions are lost. This is by design for accuracy.

## Security Considerations

### Settings File Permissions

Settings files may contain sensitive information (folder paths, recently opened PDFs). Ensure proper file permissions:

```bash
# Linux/Mac - restrict to user only
chmod 600 ~/.skf_pdf_viewer/*.json
```

### Stream Deck Server Security

The Stream Deck server only binds to localhost by default, preventing remote access. Do not modify this unless you understand the security implications.

### OneDrive Sync Privacy

If using OneDrive sync, be aware that PDF positions (including full file paths) are synced to the cloud. If this is a concern:

1. Don't use OneDrive sync
2. Or ensure OneDrive folder is encrypted

## Getting Help

If you have configuration issues:

1. Check this guide for relevant solutions
2. Verify your JSON syntax at jsonlint.com
3. Check file permissions
4. Review application console output for errors
5. Open an issue on GitHub with:
   - Your operating system
   - Anonymized copy of your settings file
   - Description of the problem

## Contributing

Found a configuration option that should be added? Please submit a pull request or open an issue on GitHub!
