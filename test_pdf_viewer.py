#!/usr/bin/env python3
"""
Test script for SKF PDF Viewer non-GUI components
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_settings():
    """Test the Settings class"""
    print("Testing Settings class...")
    
    # Import Settings from separate module (no GUI dependencies)
    from settings import Settings
    
    # Temporarily override config directory for testing
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        test_settings = Settings()
        test_settings.config_dir = Path(tmpdir)
        test_settings.settings_file = Path(tmpdir) / "test_settings.json"
        test_settings.shared_settings_file = Path(tmpdir) / "test_shared.json"
        
        # Test basic get/set
        test_settings.set('test_key', 'test_value')
        assert test_settings.get('test_key') == 'test_value', "Basic get/set failed"
        print("✓ Basic get/set works")
        
        # Test PDF position tracking
        test_settings.add_pdf_position('/test/file1.pdf', 5)
        assert test_settings.get_pdf_position('/test/file1.pdf') == 5, "PDF position tracking failed"
        print("✓ PDF position tracking works")
        
        # Test adding multiple PDFs
        for i in range(10):
            test_settings.add_pdf_position(f'/test/file{i}.pdf', i * 10)
        
        positions = test_settings.get('pdf_positions', {})
        assert len(positions) == 10, f"Expected 10 positions, got {len(positions)}"
        print("✓ Multiple PDF positions work")
        
        # Test 100 PDF limit
        for i in range(150):
            test_settings.add_pdf_position(f'/test/large_file{i}.pdf', i)
        
        positions = test_settings.get('pdf_positions', {})
        assert len(positions) == 100, f"Expected 100 positions (limit), got {len(positions)}"
        print("✓ 100 PDF position limit works")
        
        # Test recent folders
        test_settings.add_recent_folder('/test/folder1')
        test_settings.add_recent_folder('/test/folder2')
        test_settings.add_recent_folder('/test/folder1')  # Duplicate should move to front
        
        recent = test_settings.get('recent_folders', [])
        assert recent[0] == '/test/folder1', "Recent folder ordering failed"
        print("✓ Recent folder tracking works")
        
        # Add 15 folders to test the 10-folder limit
        for i in range(15):
            test_settings.add_recent_folder(f'/test/folder{i}')
        
        recent = test_settings.get('recent_folders', [])
        assert len(recent) == 10, f"Expected 10 recent folders, got {len(recent)}"
        print("✓ Recent folder limit (10) works")
        
        # Test settings persistence
        test_settings.save_settings()
        assert test_settings.settings_file.exists(), "Settings file not created"
        print("✓ Settings file created")
        
        # Verify JSON format
        with open(test_settings.settings_file, 'r') as f:
            saved_data = json.load(f)
            assert 'recent_folders' in saved_data, "Recent folders not saved"
            assert 'sidebar_visible' in saved_data, "Sidebar visibility not saved"
        print("✓ Settings saved in correct JSON format")
        
    print("\n✅ All Settings tests passed!")
    return True

def test_imports():
    """Test that all required modules are available"""
    print("\nTesting module imports...")
    
    try:
        import fitz
        print("✓ PyMuPDF (fitz) available")
    except ImportError as e:
        print(f"✗ PyMuPDF import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow available")
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False
    
    # Note: PyQt6 requires display, so we can't test it in headless environment
    print("✓ Core dependencies available")
    
    print("\n✅ All import tests passed!")
    return True

def test_code_structure():
    """Test that all required functions and classes exist"""
    print("\nTesting code structure...")
    
    # Read the source files
    with open('pdf_viewer.py', 'r') as f:
        viewer_source = f.read()
    
    with open('settings.py', 'r') as f:
        settings_source = f.read()
    
    # Check for Settings class in settings.py
    assert 'class Settings' in settings_source, "Class Settings not found in settings.py"
    print("✓ Class Settings exists")
    
    # Check for required classes in pdf_viewer.py
    required_classes = [
        'PDFWidget',
        'ThumbnailSidebar',
        'StreamDeckServer',
        'PDFViewerMainWindow'
    ]
    
    for cls in required_classes:
        assert f'class {cls}' in viewer_source, f"Class {cls} not found"
        print(f"✓ Class {cls} exists")
    
    # Check for required methods in Settings
    required_methods = [
        'load_settings',
        'save_settings',
        'add_pdf_position',
        'get_pdf_position',
        'add_recent_folder'
    ]
    
    for method in required_methods:
        assert f'def {method}' in settings_source, f"Method {method} not found"
        print(f"✓ Method {method} exists")
    
    # Check for Stream Deck endpoints
    stream_deck_commands = [
        'next', 'prev', 'zoom_in', 'zoom_out', 'fullscreen', 'next_tab', 'prev_tab'
    ]
    
    for cmd in stream_deck_commands:
        assert f"'{cmd}'" in viewer_source, f"Stream Deck command {cmd} not found"
        print(f"✓ Stream Deck command '{cmd}' implemented")
    
    print("\n✅ All structure tests passed!")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("SKF PDF Viewer - Test Suite")
    print("=" * 60)
    
    try:
        # Run tests
        test_imports()
        test_code_structure()
        test_settings()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
