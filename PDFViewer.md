# PDFViewer

PDFViewer is a desktop application designed for efficient PDF viewing and management, with comprehensive navigation controls and customization options.

## Core Features

### PDF Management

- **Drag and Drop**: Users can drag PDF files directly into the viewer to open them.
- **Tabbed Interface**: Each open PDF appears as a thumbnail tab on the left side of the window. Left-clicking a tab switches to that document, and dragging allows reordering.
- **Multiple Document Support**: Open and manage multiple PDFs simultaneously.
- **Document Closure**: Close individual PDFs or all documents at once via right-click context menu on tabs.

### Navigation

- **Page Navigation**: Navigate through document pages using hotkeys (previous/next page).
- **Document Switching**: Switch between open PDFs using hotkeys (previous/next document).
- **Zoom Control**: Zoom in and out of the current PDF using hotkeys.
- **Fullscreen Navigation**: All navigation hotkeys work without exiting fullscreen mode.
- **Window Management**: Toggle always-on-top mode or send window to back.

### Display Modes

- **Fullscreen Mode**: Distraction-free reading with toggleable fullscreen display.
- **Page-by-Page View**: Exclusive single-page display that fits content to window dimensions while maintaining PDF aspect ratio, with no borders.
- **Sidebar Thumbnails**: Toggleable sidebar showing thumbnail images of all pages in the current PDF.
- **Page Indicators**: Subtle overlay arrows at bottom-right indicate navigation options (left arrow for previous page, right arrow for next page).

## Typical Usage

A typical user workflow with PDFViewer:

1. **Launch and Restore**: Open the app to automatically display the last viewed PDF at the exact page and zoom level from the previous session.

2. **Quick Navigation**: Use a hotkey to bring up the sidebar thumbnails for rapid page navigation within the current document.

3. **Open New Documents**: Drag and drop PDF files directly into the viewer to open additional documents as new tabs.

4. **Folder Navigation**: Access a built-in file navigator to browse the folder containing the currently opened PDF. This fullscreen interface displays prominent thumbnails of all PDF files in the folder, allowing easy selection and opening of additional documents.

## Integration and Controls

### System Integration

- **Default PDF Viewer**: Can be set as the default application for opening PDF files through the operating system.

### Stream Deck Support

- Full integration with Stream Deck devices for hardware button control of all navigation and zoom functions.

#### Stream Deck Best Practices

- **Button Mapping**: Map frequently used actions (next/previous page, zoom in/out, show/hide sidebar) to easily accessible buttons for efficient workflow.
- **Visual Feedback**: Use Stream Deck's display capabilities to show current page numbers, document names, and active states on button labels.
- **Context Awareness**: Buttons should reflect the current application state (e.g., different icons for fullscreen mode vs. windowed mode).
- **Multi-Action Buttons**: Implement long-press actions for secondary functions (e.g., long-press next page for next document).
- **Status Indicators**: Display visual cues on buttons to indicate current zoom level, fullscreen status, or active document tab.
- **Custom Icons**: Provide PDFViewer-specific icons that clearly represent navigation actions and document states.
- **Responsive Updates**: Ensure button states update immediately when actions are performed through other input methods (hotkeys, mouse).

### Hotkey System

- **Global Access**: Single global hotkey brings the viewer to the front from any application.
- **Context-Aware Hotkeys**: When viewer is in background, only the global hotkey is active. Once focused, all hotkeys become available.
- **Show/Hide Controls**: Dedicated hotkeys to show (restore to last position/size) or hide (minimize completely) the viewer.
- **Tab Navigation**: Hotkeys to navigate through tabs and reorder them.
- **Auto-Show**: Using any navigation hotkey automatically brings the viewer to the front if hidden.
- **Customization**: All hotkeys are fully customizable through the settings menu.

## Settings and Customization

### Settings Menu

- **Hotkey Configuration**: Customize keyboard shortcuts for all functions.
- **Behavior Options**: Additional settings for tailoring application behavior.

### Persistence

- **Session Memory**: Remembers last viewed PDF, page, and zoom level on launch.
- **Document Page Memory**: Stores the last viewed page number for each PDF individually.
- **Recent Documents**: Maintains viewing history for up to 100 recently opened PDFs, with stored page positions. New PDFs default to the first page.
- **Recent Folders**: Remembers up to the last ten folders accessed, providing quick access to other folders for PDF viewing.
- **Window State**: Preserves exact window configuration (size, position, monitor, fullscreen state) between sessions.

### Theme Support

- **System Theme Integration**: Automatically follows system dark/light mode preferences.

## Suggested Features

*This section outlines potential future enhancements:*

- Advanced annotation and markup tools
- Full-text search within PDFs
- Bookmark and annotation management
- Multi-page view options
- Export and conversion capabilities
- Cloud storage synchronization
- Real-time collaboration features

## Development and Distribution

### Distribution Strategy

The application will be developed following best practices for cross-device distribution and synchronization:

- **Centralized Application**: The PDFViewer executable will be placed in a common folder on OneDrive, allowing easy access and updates across multiple devices.

- **Device-Specific Preferences**: Each device will maintain its own independent settings and preferences, stored locally to accommodate different user workflows and hardware configurations.

- **Default Isolation**: By default, each device will have its own document history and preferences, ensuring personalized experiences without unintended cross-device interference.

- **Settings Synchronization**: While core application settings remain device-specific, user preferences for features like hotkeys, theme choices, and UI customizations will be preserved per device.

- **Data Portability**: Document viewing history, bookmarks, and annotations will be designed to sync across devices when desired, while respecting device-specific viewing preferences.

