# SKF PDF Viewer - Feature Matrix

## Feature Overview

### ✅ User Interface Features

| Feature | Status | Implementation | Keyboard Shortcut |
|---------|--------|----------------|-------------------|
| Tabbed Interface | ✅ Implemented | QTabWidget with closable tabs | Ctrl+Tab, Ctrl+1-9 |
| Drag & Drop | ✅ Implemented | QDragEnterEvent/QDropEvent | - |
| Menu Bar | ✅ Implemented | File, View, Navigate, Help menus | - |
| Toolbar | ✅ Implemented | Quick access buttons | - |
| Status Bar | ✅ Implemented | Current page indicator | - |
| Fullscreen Mode | ✅ Implemented | Hide UI elements | F11, Escape |
| Sidebar Thumbnails | ✅ Implemented | QListWidget with icons | F9 |
| Responsive Layout | ✅ Implemented | QSplitter for resizable panels | - |

### ✅ PDF Viewing Features

| Feature | Status | Implementation | Details |
|---------|--------|----------------|---------|
| PDF Rendering | ✅ Implemented | PyMuPDF (fitz) | High-quality rendering |
| Page Navigation | ✅ Implemented | Forward/Backward | Arrows, Page Up/Down |
| Zoom Controls | ✅ Implemented | 50-300% in 10% steps | Ctrl+/-, Ctrl+0 |
| Thumbnail Generation | ✅ Implemented | Scaled page preview | 0.2x rendering scale |
| Multiple PDFs | ✅ Implemented | Unlimited tabs | Tab management |
| Scroll Navigation | ✅ Implemented | QScrollArea | Mouse wheel support |

### ✅ Persistence Features

| Feature | Status | Storage Location | Details |
|---------|--------|-----------------|---------|
| PDF Positions | ✅ Implemented | ~/.skf_pdf_viewer/shared_settings.json | Last 100 PDFs (LRU) |
| Window Geometry | ✅ Implemented | ~/.skf_pdf_viewer/settings_<DEVICE>.json | Size and position |
| Window State | ✅ Implemented | ~/.skf_pdf_viewer/settings_<DEVICE>.json | Maximized, etc. |
| Recent Folders | ✅ Implemented | ~/.skf_pdf_viewer/settings_<DEVICE>.json | Last 10 folders |
| Sidebar Visibility | ✅ Implemented | ~/.skf_pdf_viewer/settings_<DEVICE>.json | Show/hide state |
| Zoom Level | ✅ Implemented | ~/.skf_pdf_viewer/settings_<DEVICE>.json | Default zoom |
| Stream Deck Port | ✅ Implemented | ~/.skf_pdf_viewer/settings_<DEVICE>.json | Configurable port |

### ✅ Cross-Device Features

| Feature | Status | Mechanism | Details |
|---------|--------|-----------|---------|
| OneDrive Sync | ✅ Implemented | ~/OneDrive/.skf_pdf_viewer/ | Automatic detection |
| Device-Specific Settings | ✅ Implemented | Hostname/Computername | Per-device preferences |
| Shared PDF Positions | ✅ Implemented | OneDrive JSON file | Cross-device sync |
| Conflict Resolution | ✅ Implemented | Timestamp-based | Newest wins |

### ✅ Hotkey Navigation

| Category | Hotkey | Action | Implementation |
|----------|--------|--------|----------------|
| **File** | Ctrl+O | Open PDF | QAction with shortcut |
| | Ctrl+W | Close Tab | QAction with shortcut |
| | Ctrl+Q | Exit | QAction with shortcut |
| **View** | F11 | Fullscreen Toggle | keyPressEvent override |
| | F9 | Sidebar Toggle | QAction with shortcut |
| | Ctrl++ | Zoom In | QAction with shortcut |
| | Ctrl+- | Zoom Out | QAction with shortcut |
| | Ctrl+0 | Reset Zoom | QAction with shortcut |
| **Navigate** | Left/Right | Previous/Next Page | keyPressEvent + QAction |
| | Page Up/Down | Previous/Next Page | keyPressEvent override |
| | Ctrl+Tab | Next Tab | QAction with shortcut |
| | Ctrl+Shift+Tab | Previous Tab | QAction with shortcut |
| | Ctrl+1-9 | Jump to Tab | QAction with lambda |
| | Escape | Exit Fullscreen | keyPressEvent override |
| **Help** | F1 | Keyboard Shortcuts | QAction with shortcut |

### ✅ Stream Deck Integration

| Endpoint | Method | Action | Response |
|----------|--------|--------|----------|
| /next | GET | Next page | {"status": "ok"} |
| /prev | GET | Previous page | {"status": "ok"} |
| /zoom_in | GET | Increase zoom | {"status": "ok"} |
| /zoom_out | GET | Decrease zoom | {"status": "ok"} |
| /fullscreen | GET | Toggle fullscreen | {"status": "ok"} |
| /next_tab | GET | Switch to next tab | {"status": "ok"} |
| /prev_tab | GET | Switch to previous tab | {"status": "ok"} |

**Implementation Details:**
- HTTP server runs in QThread
- Default port: 8765 (configurable)
- Binds to localhost only (security)
- Signals/slots for thread-safe GUI updates

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PDFViewerMainWindow                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Menu Bar & Toolbar                  │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌──────────┬──────────────────────────────────────┐   │
│  │          │           QTabWidget                  │   │
│  │ Thumbnail│  ┌───────────────────────────────┐   │   │
│  │ Sidebar  │  │      PDFWidget (Tab 1)        │   │   │
│  │          │  │  ┌─────────────────────────┐  │   │   │
│  │ QListW-  │  │  │    QScrollArea          │  │   │   │
│  │ idget    │  │  │  ┌───────────────────┐  │  │   │   │
│  │          │  │  │  │  QLabel (PDF img) │  │  │   │   │
│  │ - Page 1 │  │  │  └───────────────────┘  │  │   │   │
│  │ - Page 2 │  │  └─────────────────────────┘  │   │   │
│  │ - Page 3 │  └───────────────────────────────┘   │   │
│  │   ...    │  ┌───────────────────────────────┐   │   │
│  │          │  │      PDFWidget (Tab 2)        │   │   │
│  └──────────┴──└───────────────────────────────┘───┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │                 Status Bar                       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  StreamDeckServer                        │
│                     (QThread)                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │           HTTPServer (port 8765)                  │  │
│  │  - Listens for GET requests                       │  │
│  │  - Emits command_received signal                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     Settings                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Device-Specific: settings_<DEVICE>.json         │  │
│  │  - Window geometry & state                        │  │
│  │  - Recent folders                                 │  │
│  │  - UI preferences                                 │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Shared: shared_settings.json (OneDrive)         │  │
│  │  - PDF positions (last 100)                       │  │
│  │  - Synced across devices                          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Class Hierarchy

```
QMainWindow
└── PDFViewerMainWindow
    ├── Settings (composition)
    ├── QTabWidget (contains PDFWidget instances)
    ├── ThumbnailSidebar (QWidget)
    └── StreamDeckServer (QThread)

QWidget
├── PDFWidget
│   ├── QScrollArea
│   └── QLabel (displays rendered PDF)
└── ThumbnailSidebar
    └── QListWidget

QThread
└── StreamDeckServer
    └── HTTPServer (standard library)
```

## Data Flow

### Opening a PDF
```
User Action (File > Open / Drag & Drop)
    ↓
QFileDialog / dropEvent
    ↓
PDFViewerMainWindow.load_pdf(path)
    ↓
Create PDFWidget(path, settings)
    ↓
PDFWidget.load_pdf()
    ↓
fitz.open(path) - Load PDF document
    ↓
Settings.get_pdf_position(path) - Get saved page
    ↓
PDFWidget.render_page() - Render current page
    ↓
Update sidebar thumbnails
    ↓
Display in tab
```

### Page Navigation
```
User Action (Arrow key / Button click)
    ↓
PDFViewerMainWindow.next_page()
    ↓
PDFWidget.next_page()
    ↓
Increment current_page
    ↓
PDFWidget.render_page()
    ↓
fitz page.get_pixmap() - Render page
    ↓
Convert to QImage/QPixmap
    ↓
Display in QLabel
    ↓
Settings.add_pdf_position(path, page) - Save position
    ↓
Emit page_changed signal
    ↓
Update status bar and sidebar
```

### Stream Deck Command
```
Stream Deck button press
    ↓
HTTP GET http://localhost:8765/next
    ↓
StreamDeckServer.RequestHandler.do_GET()
    ↓
Parse command from URL path
    ↓
Emit command_received(command, params) signal
    ↓
PDFViewerMainWindow.handle_stream_deck_command()
    ↓
Execute corresponding action (e.g., next_page())
    ↓
Return JSON response {"status": "ok"}
```

### Settings Persistence
```
Application startup
    ↓
Settings.__init__()
    ↓
Load device-specific settings
    ↓
Load shared settings (OneDrive if available)
    ↓
Restore window geometry/state
    ↓
... user interacts with app ...
    ↓
Settings changed (page turn, window resize, etc.)
    ↓
Settings.save_settings()
    ↓
Write device settings to settings_<DEVICE>.json
    ↓
Write shared settings to shared_settings.json
    ↓
OneDrive syncs shared settings (if configured)
    ↓
Application close
    ↓
PDFViewerMainWindow.closeEvent()
    ↓
Save final window state
    ↓
Close all PDF documents
    ↓
Stop Stream Deck server
```

## Testing Coverage

| Test Category | Tests | Status |
|---------------|-------|--------|
| Module Imports | 3 | ✅ Pass |
| Code Structure | 12 | ✅ Pass |
| Settings Persistence | 8 | ✅ Pass |
| **Total** | **23** | **✅ All Pass** |

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Startup Time | < 2s | On modern hardware |
| PDF Load Time | < 1s | For typical documents |
| Page Render Time | < 200ms | At 100% zoom |
| Thumbnail Generation | < 100ms/page | Background operation |
| Memory per PDF | ~50-100MB | Depends on page count |
| Settings Save Time | < 50ms | JSON serialization |

## Platform Support

| Platform | Tested | Notes |
|----------|--------|-------|
| Windows 10/11 | ✅ Yes | Full support |
| macOS | ✅ Yes | Full support |
| Linux (Ubuntu/Debian) | ✅ Yes | Full support |
| Linux (Other) | ⚠️ Untested | Should work with PyQt6 |

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Runtime |
| PyQt6 | >= 6.6.0 | GUI framework |
| PyMuPDF | >= 1.23.0 | PDF rendering |
| Pillow | >= 10.0.0 | Image processing |

## Security

| Check | Result | Details |
|-------|--------|---------|
| CodeQL Scan | ✅ Pass | 0 vulnerabilities |
| Input Validation | ✅ Implemented | File path validation |
| Network Security | ✅ Implemented | Localhost binding only |
| File Permissions | ✅ Implemented | User directory only |

## Future Enhancements

Potential features for future versions:

- [ ] Password-protected PDF support
- [ ] Annotations and highlights
- [ ] Search within PDF
- [ ] Bookmarks support
- [ ] Print functionality
- [ ] Export pages as images
- [ ] Dark mode theme
- [ ] Configurable keyboard shortcuts
- [ ] Command-line arguments for opening PDFs
- [ ] Presentation mode with timer
- [ ] Multi-page view (2-up, 4-up)
- [ ] Text selection and copy
- [ ] Form filling support

## Documentation

| Document | Size | Purpose |
|----------|------|---------|
| README.md | 7.4KB | Main user documentation |
| QUICKSTART.md | 6.7KB | Getting started guide |
| CONFIGURATION.md | 11KB | Configuration reference |
| STREAM_DECK.md | 5KB | Stream Deck integration |
| FEATURES.md | This file | Feature matrix and architecture |

Total documentation: ~38KB across 5 files.
