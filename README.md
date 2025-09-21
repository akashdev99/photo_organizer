# Photo Organizer

A cross-platform utility to organize photos and videos by date or file type.

## Features

- Organizes images and videos by date (year/month) or file type
- Supports HEIC/HEIF formats (iPhone photos)
- Automatically extracts date from image EXIF data
- Cross-platform compatibility (Windows, macOS, Linux)
- Configurable organization preferences
- Remembers your source and destination directories

## TODO 

- parallel batch execution 
- support for video 
- location based 

## Installation

### Prerequisites

- Python 3.6 or higher

### Installation Steps (All Platforms)

```bash
# Clone the repository or download the zip file
git clone https://github.com/yourusername/photo_organizer.git
cd photo_organizer
python -m venv <env_name>
# Activate the virtual environment (linux/mac)
source <env_name>/bin/activate 
# or for Windows
<env_name>\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python organizer.py
```

The first time you run the program, it will:
1. Ask for the source directory containing your photos
2. Ask for the destination directory where you want to organize them
3. Create a configuration file in the appropriate location for your OS

On subsequent runs, it will remember your previous directories and offer them as defaults.

### Example Prompt

```
Enter the directory you want to organize [/Users/username/Pictures]: /media/username/ExternalDrive/Photos
Enter the directory to which you want to write [/Users/username/Pictures/Organized]: /media/username/ExternalDrive/OrganizedPhotos
```

## Configuration

The program creates a configuration file in:
- Windows: `%APPDATA%\PhotoOrganizer\photo_organizer_config.json`
- macOS: `~/Library/Application Support/PhotoOrganizer/photo_organizer_config.json`
- Linux: `~/.config/photo_organizer/photo_organizer_config.json`

You can manually edit this file to change settings:

```json
{
    "supported_image_extensions": ["jpg", "jpeg", "png", "heic", "heif"],
    "supported_video_extensions": ["mov", "mp4", "avi", "mkv"],
    "default_source_directory": "/path/to/your/photos",
    "default_destination_directory": "/path/to/organized/photos",
    "organize_by_date": true,
    "separate_by_extension": true
}
```

## Platform-Specific Notes

### Windows
- Uses `%APPDATA%` for configuration storage
- Default photo location is the user's Pictures folder

### macOS
- Uses `~/Library/Application Support` for configuration storage
- Default photo location is the user's Pictures folder

### Linux
- Uses `~/.config` for configuration storage
- Default photo location is the user's Pictures folder