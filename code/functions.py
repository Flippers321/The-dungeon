from settings import *
from os import walk
from os.path import join

def import_folder(*paths):
    #import all images from a folder and return them as a list of frames
    frames = []
    for folder_path, subfolders, image_names in walk(join(*paths)):
        #traverse the directory specified by the joined paths
        print(image_names)
        for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
            #sort image names numerically based on the number before the file extension
            full_path = join(folder_path, image_name) #getting full path
            frames.append(pygame.image.load(full_path).convert_alpha()) #loading and append image to list
    return frames
            
def import_sub_folders(*path):
    #import images from subfolders and return them as a dictionary of frames
    frame_dict = {}
    for _, sub_folders, _ in walk(join(*path)):
        #traverse the directory specified by the joined path
        if sub_folders:
            for sub_folder in sub_folders:
                #import images from each subfolder and store them in the dictionary
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict