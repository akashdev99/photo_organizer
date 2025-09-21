from pillow_heif import register_heif_opener
from pathlib import Path
import config
from utils.utils import make_folder, move_file, get_file_type, get_create_date_object

image_path = ""


def main():
    # Get default directories from config
    default_source, default_dest = config.get_default_directories()
    
    # Use defaults as suggestions
    source_directory = input(f"Enter the directory you want to organize [{default_source}]: ")
    if not source_directory:
        source_directory = default_source
    
    destination_directory = input(f"Enter the directory to which you want to write [{default_dest}]: ")
    if not destination_directory:
        destination_directory = default_dest
    
    # Save these as defaults for next time
    cfg = config.load_config()
    cfg['default_source_directory'] = source_directory
    cfg['default_destination_directory'] = destination_directory
    config.save_config(cfg)
    
    global image_path
    image_path = destination_directory
    organize(source_directory)

# Functions moved to utils.utils



def organize(file_path:str):
    register_heif_opener()
    file_path_obj = Path(file_path)
    print("Number of files to process : ", len(list(file_path_obj.iterdir())))
    
    cfg = config.load_config()
    organize_by_date = cfg['organize_by_date']
    separate_by_extension = cfg['separate_by_extension']
    
    for f in file_path_obj.iterdir():
        if f.is_file():
            try:
                if organize_by_date:
                    create_date_obj = get_create_date_object(str(f))    
                    year_path = Path(image_path) / str(create_date_obj.year)
                    month_path = year_path / str(create_date_obj.month)
                    
                    make_folder(str(year_path))
                    make_folder(str(month_path))  
                    move_file(source_path=str(f), directory_path=image_path, first_level=create_date_obj.year, second_level=create_date_obj.month)
                    print("moved file", f.name)
                else:
                    extension = f.suffix.replace(".", "").lower()
                    folder_name = f"{get_file_type(extension)}_{extension}" if separate_by_extension else get_file_type(extension)
                    extension_path = Path(image_path) / folder_name
                    make_folder(str(extension_path))
                    move_file(source_path=str(f), directory_path=image_path, first_level=folder_name)
                    print("moved file", f.name)
            except Exception as e:
                print("failed to move image to by date", e) 
                extension = f.suffix.replace(".", "").lower()
                folder_name = f"{get_file_type(extension)}_{extension}" if separate_by_extension else get_file_type(extension)
                extension_path = Path(image_path) / folder_name
                make_folder(str(extension_path))
                move_file(source_path=str(f), directory_path=image_path, first_level=folder_name)
                print("moved file", f.name)

if __name__ == "__main__":
    main()