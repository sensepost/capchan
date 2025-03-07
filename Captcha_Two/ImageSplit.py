import argparse
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

parser = argparse.ArgumentParser(description='Split an image into four vertical sections.')

parser.add_argument('--image_path', type=str, help='Path to the image file')

args = parser.parse_args()

split_images = split_image(args.image_path)

for i, image in enumerate(split_images):
    image.save(f"split_image_{i+1}.png")

