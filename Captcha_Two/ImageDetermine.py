import os
import argparse
from PIL import Image
from colorama import Fore, Style

def compare_images(split_images_folder, data_folder, verbose=False):
    result = {}

    for folder_name in os.listdir(data_folder):
        folder_path = os.path.join(data_folder, folder_name)

        if not os.path.isdir(folder_path):
            continue

        matches = {}

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_image = Image.open(file_path).convert('1')

            for split_image_name in os.listdir(split_images_folder):
                if split_image_name.startswith("split_image_"):
                    split_image_path = os.path.join(split_images_folder, split_image_name)
                    split_image = Image.open(split_image_path).convert('1')

                    if split_image.size == file_image.size and list(split_image.getdata()) == list(file_image.getdata()):
                        split_image_number = int(split_image_name[len("split_image_"):-len(".png")])
                        if split_image_number not in matches:
                            matches[split_image_number] = []
                        matches[split_image_number].append(os.path.splitext(file_name)[0])

        result[folder_name] = matches

    return result

parser = argparse.ArgumentParser(description='Compare black and white split images with files in a data folder.')

parser.add_argument('--split_images_folder', type=str, help='Path to the folder containing split images')
parser.add_argument('--data_folder', type=str, help='Path to the data folder')
parser.add_argument('-v', '--verbose', action='store_true', help='Print all filenames with extensions')

args = parser.parse_args()

if args.split_images_folder is None:
    parser.error("Please provide the path to the split images folder.")

comparison_result = compare_images(args.split_images_folder, args.data_folder, args.verbose)

output = []

for folder_name, matches in comparison_result.items():
    if args.verbose:
        output.append(f"Matches in folder '{folder_name}':")
        if len(matches) > 0:
            for split_image_number, file_matches in sorted(matches.items()):
                split_image_name = f"split_image_{split_image_number}"
                output.append(split_image_name + ":")
                if len(file_matches) > 0:
                    for file_match in sorted(file_matches):
                        output.append(Fore.GREEN + file_match + Style.RESET_ALL)  
                else:
                    output.append(Fore.YELLOW + "No matches found." + Style.RESET_ALL)  
                output.append("---")
        else:
            output.append(Fore.YELLOW + "No matches found." + Style.RESET_ALL)  
    else:
        if len(matches) > 0:
            for split_image_number, file_matches in sorted(matches.items()):
                split_image_name = f"split_image_{split_image_number}"
                if len(file_matches) > 0:
                    file_names = ", ".join(sorted(file_matches))
                    output.append(Fore.GREEN + f"{split_image_name}: {file_names}" + Style.RESET_ALL)  
if not any(matches for matches in comparison_result.values()):
    if args.verbose:
        output.append(Fore.YELLOW + "No matches found." + Style.RESET_ALL)  

sorted_output = sorted(output, key=lambda x: int(x.split("_")[2].split(":")[0]))

concatenated_letters = ""
for line in sorted_output:
    line = line.strip()  
    if line and line[0] != "-":  
        concatenated_letters += line.split(":")[-1].replace(" ", "")

print(concatenated_letters)
with open("output.txt", "w") as file:
    file.write(concatenated_letters)
