import os
import json
import platform
from pathlib import Path

CONFIG_FILE = 'photo_organizer_config.json'

# Default configuration
DEFAULT_CONFIG = {
    'supported_image_extensions': ['jpg', 'jpeg', 'png', 'heic', 'heif'],
    'supported_video_extensions': ['mov', 'mp4', 'avi', 'mkv'],
    'default_source_directory': '',
    'default_destination_directory': '',
    'organize_by_date': True,
    'separate_by_extension': True
}

def get_config_path():
    """Get the appropriate config file path based on the operating system"""
    system = platform.system()
    
    if system == 'Windows':
        config_dir = Path(os.environ.get('APPDATA', '')) / 'PhotoOrganizer'
    elif system == 'Darwin':  # macOS
        config_dir = Path.home() / 'Library' / 'Application Support' / 'PhotoOrganizer'
    else:  # Linux and others
        config_dir = Path.home() / '.config' / 'photo_organizer'
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / CONFIG_FILE

def load_config():
    """Load configuration from file or create default if not exists"""
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG
    else:
        # Create default config
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file"""
    config_path = get_config_path()
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def update_config(key, value):
    """Update a specific configuration value"""
    config = load_config()
    config[key] = value
    return save_config(config)

def get_default_directories():
    """Get platform-specific default directories"""
    system = platform.system()
    config = load_config()
    
    # Use configured defaults if they exist
    if config['default_source_directory'] and config['default_destination_directory']:
        return config['default_source_directory'], config['default_destination_directory']
    
    # Otherwise suggest platform-specific defaults
    if system == 'Windows':
        pictures_dir = Path(os.environ.get('USERPROFILE', '')) / 'Pictures'
    elif system == 'Darwin':  # macOS
        pictures_dir = Path.home() / 'Pictures'
    else:  # Linux and others
        pictures_dir = Path.home() / 'Pictures'
    
    return str(pictures_dir), str(pictures_dir / 'Organized')
