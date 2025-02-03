from pillow_heif import register_heif_opener
from PIL import Image
from datetime import datetime
from os import listdir
import os
import shutil
from pathlib import Path

is_directory_created = {}
image_path = ""

def make_folder(directory_path:str):    
    if directory_path in is_directory_created.keys():
        print("Yup this exists skipping")
        return 

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")

    else:
        print(f"Directory '{directory_path}' already exists.")
    is_directory_created[directory_path] = True


def move_file(source_path:str , directory_path:str, first_level:int, second_level:int=None):
    if second_level:
        destination_path = os.path.join(directory_path , str(first_level), f"{str(second_level)}/")
    else:
        destination_path = os.path.join(directory_path , f"{str(first_level)}/")
    shutil.move(source_path , destination_path)

def get_file_type(extension:str):
    if extension in ["MOV" , "MP4"]:
        return "videos"
    else:
        return "images"

def get_create_date_object(source_path:str):
    image = Image.open(source_path)
    exif_data = image.getexif()
    create_date  = exif_data[306]
    return datetime.strptime(create_date , "%Y:%m:%d %H:%M:%S")


def extract_heic_opener(file_path:str):
    register_heif_opener()
    print("Number of files to process : ",len(listdir(file_path)))
    
    for f in listdir(file_path):
        source_path = os.path.join(file_path,f)
        try:
            create_date_obj = get_create_date_object(source_path)    
            make_folder(os.path.join(image_path, str(create_date_obj.year)))
            make_folder(os.path.join(image_path , str(create_date_obj.year) , str(create_date_obj.month)))  
            move_file(source_path =source_path , directory_path=image_path , first_level=create_date_obj.year ,second_level=create_date_obj.month)
            print("moved file ",f)
        except Exception as e :
            print("failed to move image to by date",e) 
            extension = Path(source_path).suffix.replace(".","")
            folder_name = f"{get_file_type(extension)}_{extension}"
            make_folder(os.path.join(image_path, folder_name))
            move_file(source_path =source_path , directory_path=image_path , first_level=folder_name)
            print("moved file ",f)

def main():
    source_directory = input("Enter the directory you want to organize: ")
    destination_directory = input("Enter the directory to which you want to write: ")
    
    global image_path
    image_path = destination_directory
    extract_heic_opener(source_directory)


if __name__ == "__main__":
    main()
