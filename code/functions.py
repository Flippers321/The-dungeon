from settings import *
from os import walk
from os.path import join

def import_folder(*paths):
    frames = []
    for folder_path, subfolders, image_names in walk(join(*paths)):
        print(image_names)
        for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames
            
def import_sub_folders(*path):
    frame_dict = {}
    for _, sub_folders, _ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict