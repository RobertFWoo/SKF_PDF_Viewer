"""
Settings management for SKF PDF Viewer
Handles persistence of preferences and PDF positions
"""

import os
import json
from pathlib import Path
from collections import OrderedDict
from datetime import datetime


class Settings:
    """Manage application settings and persistence"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".skf_pdf_viewer"
        self.config_dir.mkdir(exist_ok=True)
        
        # Device-specific settings file
        self.device_id = os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'default'))
        self.settings_file = self.config_dir / f"settings_{self.device_id}.json"
        
        # Shared settings (can be on OneDrive)
        self.shared_dir = Path.home() / "OneDrive" / ".skf_pdf_viewer"
        if self.shared_dir.exists():
            self.shared_settings_file = self.shared_dir / "shared_settings.json"
        else:
            self.shared_settings_file = self.config_dir / "shared_settings.json"
        
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Load settings from file"""
        settings = {
            'window_geometry': None,
            'window_state': None,
            'recent_folders': [],
            'pdf_positions': OrderedDict(),  # Last 100 PDFs
            'sidebar_visible': True,
            'zoom_level': 100,
            'stream_deck_port': 8765
        }
        
        # Load device-specific settings
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    settings.update(loaded)
            except Exception as e:
                print(f"Error loading settings: {e}")
        
        # Load shared settings (PDF positions)
        if self.shared_settings_file.exists():
            try:
                with open(self.shared_settings_file, 'r') as f:
                    shared = json.load(f)
                    if 'pdf_positions' in shared:
                        settings['pdf_positions'] = OrderedDict(shared['pdf_positions'])
            except Exception as e:
                print(f"Error loading shared settings: {e}")
        
        return settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            # Save device-specific settings
            device_settings = {
                'window_geometry': self.settings.get('window_geometry'),
                'window_state': self.settings.get('window_state'),
                'recent_folders': self.settings.get('recent_folders', []),
                'sidebar_visible': self.settings.get('sidebar_visible', True),
                'zoom_level': self.settings.get('zoom_level', 100),
                'stream_deck_port': self.settings.get('stream_deck_port', 8765)
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(device_settings, f, indent=2)
            
            # Save shared settings (PDF positions)
            shared_dir = self.shared_settings_file.parent
            shared_dir.mkdir(parents=True, exist_ok=True)
            
            shared_settings = {
                'pdf_positions': dict(self.settings.get('pdf_positions', {}))
            }
            
            with open(self.shared_settings_file, 'w') as f:
                json.dump(shared_settings, f, indent=2)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
    
    def add_pdf_position(self, pdf_path, page_num):
        """Store page position for a PDF (keep last 100)"""
        positions = self.settings.get('pdf_positions', OrderedDict())
        
        # Remove if exists (to update order)
        if pdf_path in positions:
            del positions[pdf_path]
        
        # Add to end
        positions[pdf_path] = {
            'page': page_num,
            'timestamp': datetime.now().isoformat()
        }
        
        # Keep only last 100
        if len(positions) > 100:
            # Remove oldest
            positions.popitem(last=False)
        
        self.settings['pdf_positions'] = positions
        self.save_settings()
    
    def get_pdf_position(self, pdf_path):
        """Get saved page position for a PDF"""
        positions = self.settings.get('pdf_positions', {})
        if pdf_path in positions:
            return positions[pdf_path].get('page', 0)
        return 0
    
    def add_recent_folder(self, folder_path):
        """Add folder to recent folders list"""
        recent = self.settings.get('recent_folders', [])
        if folder_path in recent:
            recent.remove(folder_path)
        recent.insert(0, folder_path)
        # Keep only last 10
        self.settings['recent_folders'] = recent[:10]
        self.save_settings()
