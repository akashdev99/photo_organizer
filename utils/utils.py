from PIL import Image
from datetime import datetime
import shutil
from pathlib import Path
import config

is_directory_created = {}

def make_folder(directory_path:str):    
    directory = Path(directory_path)
    if str(directory) in is_directory_created:
        print("Yup this exists skipping")
        return 

    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Directory '{directory}' created successfully.")

    else:
        print(f"Directory '{directory}' already exists.")
    is_directory_created[str(directory)] = True


def move_file(source_path:str, directory_path:str, first_level:int, second_level:int=None):
    source = Path(source_path)
    if second_level:
        destination_path = Path(directory_path) / str(first_level) / str(second_level)
    else:
        destination_path = Path(directory_path) / str(first_level)
    
    # Ensure the destination directory exists
    destination_path.mkdir(parents=True, exist_ok=True)
    
    # Get the destination file path (directory + filename)
    destination_file = destination_path / source.name
    
    # Move the file
    shutil.move(str(source), str(destination_file))


def get_file_type(extension:str):
    cfg = config.load_config()
    extension = extension.lower()
    
    if extension in [ext.lower() for ext in cfg['supported_video_extensions']]:
        return "videos"
    else:
        return "images"


def get_create_date_object(source_path:str):
    image = Image.open(source_path)
    exif_data = image.getexif()
    if 306 in exif_data.keys():
        create_date = exif_data[306]
        return datetime.strptime(create_date, "%Y:%m:%d %H:%M:%S")
    else:
        return datetime.fromtimestamp(Path(source_path).stat().st_mtime)
