import argparse
import os
import random
import string
from PIL import Image

def split_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    section_width = width // 4
    split_images = []
    for i in range(4):
        left = i * section_width
        upper = 0
        right = left + section_width
        lower = height
        section = image.crop((left, upper, right, lower))
        split_images.append(section)
    return split_images

def generate_random_name(length=8):
    letters_and_digits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

parser = argparse.ArgumentParser(description='Split images into four vertical sections.')
parser.add_argument('--image_folder', type=str, help='Path to the folder containing the images')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()

image_folder = args.image_folder
output_folder = "Val" #Changeme this to Data or Val depending on what you want. 

os.makedirs(output_folder, exist_ok=True)

current_file = None

for image_file in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_file)
    if os.path.isfile(image_path):
        image_name = os.path.splitext(image_file)[0]
        
        if len(image_name) >= 4:
            new_image_names = [image_name[0], image_name[1], image_name[2], image_name[3]]
            
            split_images = split_image(image_path)
            
            for i, section in enumerate(split_images):
                new_image_name = new_image_names[i]
                
                random_name = generate_random_name()
                
                split_image_path = os.path.join(output_folder, new_image_name, f"{random_name}.png")
                os.makedirs(os.path.dirname(split_image_path), exist_ok=True)
                try:
                    section.save(split_image_path)
                    if args.debug:
                        if current_file != image_file:
                            current_file = image_file
                            print(f"\033[94m[NEW FILE]\033[0m Processing '{image_file}'")
                        print(f"\033[92m[SUCCESS]\033[0m Moved '{image_file}' to '{split_image_path}'")
                except Exception as e:
                    if args.debug:
                        print(f"\033[91m[ERROR]\033[0m Failed to move '{image_file}' to '{split_image_path}': {str(e)}")

