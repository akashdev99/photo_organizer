from pillow_heif import register_heif_opener
from PIL import Image
from datetime import datetime
from os import listdir
import os
import shutil

is_directory_created = {}
image_path = "/media/akash/ElementX/memories/iphone_automated/"

def make_folder(directory_path:str, year:int):
    # Check if the directory exists
    path = directory_path+str(year)
    
    if path in is_directory_created.keys():
        print("Yup this exists skipping")
        return 

    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created successfully.")

    else:
        print(f"Directory '{path}' already exists.")


def move_file(source_path:str , directory_path:str, first_level:int, second_level:int=None):
    if second_level:
        destination_path = directory_path+str(first_level)+"/"+str(second_level)+"/"
    else:
        destination_path = directory_path+str(first_level)+"/"
    shutil.move(source_path , destination_path)



def extract_heic_opener(file_path):
    register_heif_opener()
    print("no of files to process : ",len(listdir(file_path)))
    
    for f in listdir(file_path):
        source_path = file_path+f
        if "HEIC" in f:
            image = Image.open(source_path)
            exif_data = image.getexif()
            create_date  = exif_data[306]
            create_date_obj = datetime.strptime(create_date , "%Y:%m:%d %H:%M:%S")
            make_folder(image_path, create_date_obj.year)
            make_folder(image_path+str(create_date_obj.year)+"/" , create_date_obj.month)

            move_file(source_path =source_path , directory_path=image_path , first_level=create_date_obj.year , second_level=create_date_obj.month)
            print("moved file ",image.filename)
        if "MOV" in f:
            make_folder(image_path, "videos_mov")
            move_file(source_path =source_path , directory_path=image_path , first_level="videos_mov")
            print("moved file ",f)
        if "MP4" in f:
            make_folder(image_path, "videos_mp4")
            move_file(source_path =source_path , directory_path=image_path , first_level="videos_mp4")
            print("moved file ",f)
        if "JPG" in f or "JPEG" in f:
            make_folder(image_path, "images_jpg")
            move_file(source_path =source_path , directory_path=image_path , first_level="images_jpg")
            print("moved file ",f)

extract_heic_opener("/media/akash/ElementX/memories/iphone_automated/2025/")