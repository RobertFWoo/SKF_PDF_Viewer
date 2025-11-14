#!/usr/bin/env python3
"""
SKF PDF Viewer - A feature-rich desktop PDF viewer
with tabbed interface, drag-and-drop, and comprehensive navigation
"""

import sys
import os
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QScrollArea, QLabel, QMenuBar, QMenu, QFileDialog,
    QSplitter, QListWidget, QListWidgetItem, QToolBar, QMessageBox,
    QPushButton
)
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QImage, QAction, QKeySequence, QDragEnterEvent, QDropEvent
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Import Settings from separate module
from settings import Settings


class PDFWidget(QWidget):
    """Widget to display a PDF document"""
    
    page_changed = pyqtSignal(int, int)  # current_page, total_pages
    
    def __init__(self, pdf_path, settings):
        super().__init__()
        self.pdf_path = pdf_path
        self.settings = settings
        self.doc = None
        self.current_page = 0
        self.zoom_level = settings.get('zoom_level', 100)
        
        self.init_ui()
        self.load_pdf()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for PDF display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.pdf_label = QLabel()
        self.pdf_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.pdf_label)
        
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)
        
    def load_pdf(self):
        """Load PDF document"""
        try:
            self.doc = fitz.open(self.pdf_path)
            # Restore saved position
            saved_page = self.settings.get_pdf_position(self.pdf_path)
            self.current_page = min(saved_page, len(self.doc) - 1)
            self.render_page()
        except Exception as e:
            self.pdf_label.setText(f"Error loading PDF: {str(e)}")
    
    def render_page(self):
        """Render current page"""
        if not self.doc or self.current_page >= len(self.doc):
            return
        
        try:
            page = self.doc[self.current_page]
            
            # Calculate zoom matrix
            zoom = self.zoom_level / 100.0
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to QImage
            img_format = QImage.Format.Format_RGB888 if pix.alpha == 0 else QImage.Format.Format_RGBA8888
            qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, img_format)
            
            # Display
            pixmap = QPixmap.fromImage(qimage)
            self.pdf_label.setPixmap(pixmap)
            
            # Save position
            self.settings.add_pdf_position(self.pdf_path, self.current_page)
            
            # Emit signal
            self.page_changed.emit(self.current_page + 1, len(self.doc))
            
        except Exception as e:
            print(f"Error rendering page: {e}")
    
    def next_page(self):
        """Go to next page"""
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.render_page()
            return True
        return False
    
    def prev_page(self):
        """Go to previous page"""
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.render_page()
            return True
        return False
    
    def goto_page(self, page_num):
        """Go to specific page (0-indexed)"""
        if self.doc and 0 <= page_num < len(self.doc):
            self.current_page = page_num
            self.render_page()
    
    def zoom_in(self):
        """Increase zoom level"""
        self.zoom_level = min(self.zoom_level + 10, 300)
        self.render_page()
    
    def zoom_out(self):
        """Decrease zoom level"""
        self.zoom_level = max(self.zoom_level - 10, 50)
        self.render_page()
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.zoom_level = 100
        self.render_page()
    
    def get_page_count(self):
        """Get total number of pages"""
        return len(self.doc) if self.doc else 0
    
    def get_thumbnail(self, page_num, size=(100, 150)):
        """Generate thumbnail for a page"""
        if not self.doc or page_num >= len(self.doc):
            return None
        
        try:
            page = self.doc[page_num]
            # Render small version for thumbnail
            mat = fitz.Matrix(0.2, 0.2)
            pix = page.get_pixmap(matrix=mat)
            
            img_format = QImage.Format.Format_RGB888 if pix.alpha == 0 else QImage.Format.Format_RGBA8888
            qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, img_format)
            pixmap = QPixmap.fromImage(qimage)
            
            return pixmap.scaled(size[0], size[1], Qt.AspectRatioMode.KeepAspectRatio)
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
    
    def close_document(self):
        """Close the PDF document"""
        if self.doc:
            self.doc.close()


class ThumbnailSidebar(QWidget):
    """Sidebar showing page thumbnails"""
    
    thumbnail_clicked = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.pdf_widget = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setIconSize(QSize(100, 150))
        self.thumbnail_list.itemClicked.connect(self.on_thumbnail_click)
        
        layout.addWidget(self.thumbnail_list)
        self.setLayout(layout)
        
        self.setMinimumWidth(120)
        self.setMaximumWidth(200)
    
    def set_pdf_widget(self, pdf_widget):
        """Set the PDF widget to generate thumbnails for"""
        self.pdf_widget = pdf_widget
        self.load_thumbnails()
    
    def load_thumbnails(self):
        """Load thumbnails for all pages"""
        self.thumbnail_list.clear()
        
        if not self.pdf_widget:
            return
        
        page_count = self.pdf_widget.get_page_count()
        for i in range(page_count):
            thumbnail = self.pdf_widget.get_thumbnail(i)
            if thumbnail:
                item = QListWidgetItem(f"Page {i + 1}")
                item.setIcon(thumbnail)
                item.setData(Qt.ItemDataRole.UserRole, i)
                self.thumbnail_list.addItem(item)
    
    def on_thumbnail_click(self, item):
        """Handle thumbnail click"""
        page_num = item.data(Qt.ItemDataRole.UserRole)
        self.thumbnail_clicked.emit(page_num)
    
    def highlight_page(self, page_num):
        """Highlight current page in thumbnail list"""
        for i in range(self.thumbnail_list.count()):
            item = self.thumbnail_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == page_num:
                self.thumbnail_list.setCurrentItem(item)
                break


class StreamDeckServer(QThread):
    """HTTP server for Stream Deck integration"""
    
    command_received = pyqtSignal(str, dict)
    
    def __init__(self, port=8765):
        super().__init__()
        self.port = port
        self.server = None
        self.running = False
        
    def run(self):
        """Run the HTTP server"""
        self.running = True
        
        class RequestHandler(BaseHTTPRequestHandler):
            command_signal = self.command_received
            
            def do_GET(self_handler):
                """Handle GET requests"""
                parsed = urllib.parse.urlparse(self_handler.path)
                query = urllib.parse.parse_qs(parsed.query)
                
                command = parsed.path.strip('/')
                
                self_handler.send_response(200)
                self_handler.send_header('Content-type', 'application/json')
                self_handler.end_headers()
                
                self_handler.command_signal.emit(command, query)
                self_handler.wfile.write(b'{"status": "ok"}')
            
            def log_message(self_handler, format, *args):
                """Suppress log messages"""
                pass
        
        try:
            self.server = HTTPServer(('localhost', self.port), RequestHandler)
            print(f"Stream Deck server started on port {self.port}")
            self.server.serve_forever()
        except Exception as e:
            print(f"Error starting Stream Deck server: {e}")
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server:
            self.server.shutdown()


class PDFViewerMainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.is_fullscreen = False
        self.stream_deck_server = None
        
        self.init_ui()
        self.restore_window_state()
        self.setup_stream_deck()
        
    def init_ui(self):
        self.setWindowTitle("SKF PDF Viewer")
        self.setMinimumSize(800, 600)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar for thumbnails
        self.sidebar = ThumbnailSidebar()
        self.sidebar.thumbnail_clicked.connect(self.on_thumbnail_clicked)
        
        # Tab widget for multiple PDFs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.setStretchFactor(1, 1)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        
        central_widget.setLayout(layout)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Apply sidebar visibility
        if not self.settings.get('sidebar_visible', True):
            self.sidebar.hide()
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open PDF...", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)
        
        # Recent folders submenu
        self.recent_menu = QMenu("Recent &Folders", self)
        self.update_recent_folders_menu()
        file_menu.addMenu(self.recent_menu)
        
        file_menu.addSeparator()
        
        close_tab_action = QAction("&Close Tab", self)
        close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_tab_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        fullscreen_action = QAction("&Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        sidebar_action = QAction("Toggle &Sidebar", self)
        sidebar_action.setShortcut(QKeySequence("F9"))
        sidebar_action.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(sidebar_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("&Reset Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        # Navigate menu
        nav_menu = menubar.addMenu("&Navigate")
        
        next_page_action = QAction("&Next Page", self)
        next_page_action.setShortcut(QKeySequence("Right"))
        next_page_action.triggered.connect(self.next_page)
        nav_menu.addAction(next_page_action)
        
        prev_page_action = QAction("&Previous Page", self)
        prev_page_action.setShortcut(QKeySequence("Left"))
        prev_page_action.triggered.connect(self.prev_page)
        nav_menu.addAction(prev_page_action)
        
        nav_menu.addSeparator()
        
        next_tab_action = QAction("Next &Tab", self)
        next_tab_action.setShortcut(QKeySequence("Ctrl+Tab"))
        next_tab_action.triggered.connect(self.next_tab)
        nav_menu.addAction(next_tab_action)
        
        prev_tab_action = QAction("Pre&vious Tab", self)
        prev_tab_action.setShortcut(QKeySequence("Ctrl+Shift+Tab"))
        prev_tab_action.triggered.connect(self.prev_tab)
        nav_menu.addAction(prev_tab_action)
        
        # Tab shortcuts (Ctrl+1 through Ctrl+9)
        for i in range(1, 10):
            tab_action = QAction(f"Go to Tab {i}", self)
            tab_action.setShortcut(QKeySequence(f"Ctrl+{i}"))
            tab_action.triggered.connect(lambda checked, idx=i-1: self.goto_tab(idx))
            nav_menu.addAction(tab_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.setShortcut(QKeySequence("F1"))
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
    
    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Open button
        open_btn = QPushButton("Open PDF")
        open_btn.clicked.connect(self.open_pdf)
        toolbar.addWidget(open_btn)
        
        toolbar.addSeparator()
        
        # Navigation buttons
        prev_btn = QPushButton("◀ Previous")
        prev_btn.clicked.connect(self.prev_page)
        toolbar.addWidget(prev_btn)
        
        next_btn = QPushButton("Next ▶")
        next_btn.clicked.connect(self.next_page)
        toolbar.addWidget(next_btn)
        
        toolbar.addSeparator()
        
        # Zoom buttons
        zoom_out_btn = QPushButton("Zoom -")
        zoom_out_btn.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out_btn)
        
        zoom_in_btn = QPushButton("Zoom +")
        zoom_in_btn.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in_btn)
        
        self.toolbar = toolbar
    
    def update_recent_folders_menu(self):
        """Update recent folders menu"""
        self.recent_menu.clear()
        
        recent_folders = self.settings.get('recent_folders', [])
        for folder in recent_folders:
            if os.path.exists(folder):
                action = QAction(folder, self)
                action.triggered.connect(lambda checked, f=folder: self.open_pdf_from_folder(f))
                self.recent_menu.addAction(action)
    
    def open_pdf(self):
        """Open PDF file dialog"""
        last_folder = ""
        recent = self.settings.get('recent_folders', [])
        if recent:
            last_folder = recent[0]
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            last_folder,
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.load_pdf(file_path)
            # Add folder to recent
            folder = os.path.dirname(file_path)
            self.settings.add_recent_folder(folder)
            self.update_recent_folders_menu()
    
    def open_pdf_from_folder(self, folder):
        """Open PDF from a specific folder"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            folder,
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.load_pdf(file_path)
    
    def load_pdf(self, file_path):
        """Load a PDF file in a new tab"""
        pdf_widget = PDFWidget(file_path, self.settings)
        pdf_widget.page_changed.connect(self.on_page_changed)
        
        file_name = os.path.basename(file_path)
        self.tab_widget.addTab(pdf_widget, file_name)
        self.tab_widget.setCurrentWidget(pdf_widget)
        
        # Update sidebar
        self.sidebar.set_pdf_widget(pdf_widget)
        
        self.statusBar().showMessage(f"Loaded: {file_name}")
    
    def close_tab(self, index):
        """Close a specific tab"""
        if self.tab_widget.count() > 0:
            widget = self.tab_widget.widget(index)
            if isinstance(widget, PDFWidget):
                widget.close_document()
            self.tab_widget.removeTab(index)
    
    def close_current_tab(self):
        """Close the current tab"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.close_tab(current_index)
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        if index >= 0:
            widget = self.tab_widget.widget(index)
            if isinstance(widget, PDFWidget):
                self.sidebar.set_pdf_widget(widget)
                # Trigger page changed to update status
                widget.page_changed.emit(widget.current_page + 1, widget.get_page_count())
    
    def on_page_changed(self, current_page, total_pages):
        """Handle page change"""
        self.statusBar().showMessage(f"Page {current_page} of {total_pages}")
        # Update thumbnail sidebar
        self.sidebar.highlight_page(current_page - 1)
    
    def on_thumbnail_clicked(self, page_num):
        """Handle thumbnail click"""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, PDFWidget):
            current_widget.goto_page(page_num)
    
    def get_current_pdf_widget(self):
        """Get current PDF widget"""
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, PDFWidget):
            return widget
        return None
    
    def next_page(self):
        """Go to next page"""
        pdf = self.get_current_pdf_widget()
        if pdf:
            pdf.next_page()
    
    def prev_page(self):
        """Go to previous page"""
        pdf = self.get_current_pdf_widget()
        if pdf:
            pdf.prev_page()
    
    def zoom_in(self):
        """Zoom in"""
        pdf = self.get_current_pdf_widget()
        if pdf:
            pdf.zoom_in()
    
    def zoom_out(self):
        """Zoom out"""
        pdf = self.get_current_pdf_widget()
        if pdf:
            pdf.zoom_out()
    
    def reset_zoom(self):
        """Reset zoom"""
        pdf = self.get_current_pdf_widget()
        if pdf:
            pdf.reset_zoom()
    
    def next_tab(self):
        """Switch to next tab"""
        count = self.tab_widget.count()
        if count > 1:
            current = self.tab_widget.currentIndex()
            next_idx = (current + 1) % count
            self.tab_widget.setCurrentIndex(next_idx)
    
    def prev_tab(self):
        """Switch to previous tab"""
        count = self.tab_widget.count()
        if count > 1:
            current = self.tab_widget.currentIndex()
            prev_idx = (current - 1) % count
            self.tab_widget.setCurrentIndex(prev_idx)
    
    def goto_tab(self, index):
        """Go to specific tab"""
        if 0 <= index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(index)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.is_fullscreen:
            self.showNormal()
            self.menuBar().show()
            self.toolbar.show()
            self.statusBar().show()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.menuBar().hide()
            self.toolbar.hide()
            self.statusBar().hide()
            self.is_fullscreen = True
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        if self.sidebar.isVisible():
            self.sidebar.hide()
            self.settings.set('sidebar_visible', False)
        else:
            self.sidebar.show()
            self.settings.set('sidebar_visible', True)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About SKF PDF Viewer",
            "SKF PDF Viewer v1.0\n\n"
            "A feature-rich desktop PDF viewer with:\n"
            "- Tabbed interface\n"
            "- Drag-and-drop support\n"
            "- Comprehensive hotkey navigation\n"
            "- Fullscreen mode\n"
            "- Sidebar thumbnails\n"
            "- Stream Deck integration\n"
            "- Persistent preferences\n\n"
            "© 2024 SKF PDF Viewer"
        )
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_text = """
Keyboard Shortcuts:

File Operations:
  Ctrl+O          Open PDF
  Ctrl+W          Close tab
  Ctrl+Q          Exit

Navigation:
  Left/Right      Previous/Next page
  Page Up/Down    Previous/Next page
  Ctrl+Tab        Next tab
  Ctrl+Shift+Tab  Previous tab
  Ctrl+1-9        Go to tab 1-9

View:
  F11             Toggle fullscreen
  F9              Toggle sidebar
  Ctrl++          Zoom in
  Ctrl+-          Zoom out
  Ctrl+0          Reset zoom

Help:
  F1              Show this help
"""
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.pdf'):
                self.load_pdf(file_path)
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        key = event.key()
        
        # Page Up/Down for navigation
        if key == Qt.Key.Key_PageDown:
            self.next_page()
        elif key == Qt.Key.Key_PageUp:
            self.prev_page()
        # Escape to exit fullscreen
        elif key == Qt.Key.Key_Escape and self.is_fullscreen:
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)
    
    def restore_window_state(self):
        """Restore window geometry and state"""
        geometry = self.settings.get('window_geometry')
        if geometry:
            self.restoreGeometry(bytes.fromhex(geometry))
        
        state = self.settings.get('window_state')
        if state:
            self.restoreState(bytes.fromhex(state))
    
    def save_window_state(self):
        """Save window geometry and state"""
        self.settings.set('window_geometry', self.saveGeometry().toHex().data().decode())
        self.settings.set('window_state', self.saveState().toHex().data().decode())
    
    def setup_stream_deck(self):
        """Setup Stream Deck integration server"""
        port = self.settings.get('stream_deck_port', 8765)
        self.stream_deck_server = StreamDeckServer(port)
        self.stream_deck_server.command_received.connect(self.handle_stream_deck_command)
        self.stream_deck_server.start()
    
    def handle_stream_deck_command(self, command, params):
        """Handle Stream Deck commands"""
        if command == 'next':
            self.next_page()
        elif command == 'prev':
            self.prev_page()
        elif command == 'zoom_in':
            self.zoom_in()
        elif command == 'zoom_out':
            self.zoom_out()
        elif command == 'fullscreen':
            self.toggle_fullscreen()
        elif command == 'next_tab':
            self.next_tab()
        elif command == 'prev_tab':
            self.prev_tab()
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.save_window_state()
        
        # Close all PDFs
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, PDFWidget):
                widget.close_document()
        
        # Stop Stream Deck server
        if self.stream_deck_server:
            self.stream_deck_server.stop()
        
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SKF PDF Viewer")
    
    window = PDFViewerMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
