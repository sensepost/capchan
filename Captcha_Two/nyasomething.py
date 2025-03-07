import argparse
import subprocess
import re
import os
from termcolor import colored
import binascii

def print_debug(message):
    print(colored('[DEBUG] ', 'green') + message)

def print_error(message):
    print(colored('[ERROR] ', 'red') + message)

def connect_to_ncat(destination, verbose, debug):
    command = ['ncat', '--ssl', destination, '443']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process

def read_first_lines(process, lines_to_read, verbose):
    for _ in range(lines_to_read):
        line = process.stdout.readline().decode().strip()
        if verbose:
            print(line)
        else:
            print(line, flush=True)

def press_enter(process, debug):
    process.stdin.write('\n'.encode())
    process.stdin.flush()
    hex_lines = []
    end_marker_pattern = r'--- Type Answer to provided captcha \d+ ---'

    while True:
        line = process.stdout.readline().decode().strip()
        if re.match(end_marker_pattern, line):
            if debug:
                print_debug("Hex conversion ended.")
            break
        if verbose:
            print(line)
        else:
            print(line, flush=True)
        if not line.startswith("---"):
            hex_lines.append(line)

    return ''.join(hex_lines).strip()

def hex_to_png(hexadecimal, filename, debug):
    try:
        binary_str = binascii.unhexlify(hexadecimal)

        with open(filename, 'wb') as f:
            f.write(binary_str)

        if debug:
            print_debug("Hex to PNG conversion completed. PNG saved to " + filename)
    except Exception as e:
        print_error("Error occurred during hex to PNG conversion: " + str(e))

def remove_control_characters(text):
    pattern = r"\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]"
    return re.sub(pattern, "", text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a hexadecimal string to a PNG image.')

    parser.add_argument('-s', '--source', required=True, help='Specify the destination for the "ncat" command.')
    parser.add_argument('-f', '--file', required=False, help='Specify the file name containing the hexadecimal string.')
    parser.add_argument('-o', '--output', default='image.png',
                        help="Specify the output file name. If not provided, the default is 'image.png'.")
    parser.add_argument('-v', '--verbose', action='store_true', help='Display verbose output of the "ncat" command.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')

    args = parser.parse_args()
    debug = args.debug
    verbose = args.verbose

    if args.source:
        if debug:
            print_debug("Connecting to " + args.source)
        process = connect_to_ncat(args.source, verbose, debug)
        lines_to_read = 4
        read_first_lines(process, lines_to_read, verbose)
    elif args.file:
        with open(args.file, 'r') as f:
            hexadecimal = f.read().strip()
    else:
        parser.error('Either --source or -f/--file must be provided.')
    
    for i in range(200):
        hexadecimal = press_enter(process, debug)
        filename = args.output

        if debug:
            print_debug("Converting hex to PNG...")
        hex_to_png(hexadecimal, filename, debug)

        if debug:
            print_debug("Running ImageSplit.py...")
        image_split_command = ['python3', 'ImageSplit.py', '--image_path', filename]
        subprocess.run(image_split_command)

        if debug:
            print_debug("Running ImageDetermine.py...")
        image_determine_command = ['python3', 'ImageDetermine.py', '--split_images_folder', '/home/changeme/Captcha_Two', '--data_folder', 'Images/']
        subprocess.run(image_determine_command)

        if debug:
            print_debug("Reading contents of output.txt...")
        with open("output.txt", "r") as f:
            lines = f.readlines()

        correct_answer_line = None
        for line in lines:
            if re.match(r"Correct Answer: .+", line):
                correct_answer_line = line
                break

        if correct_answer_line:
            image_name = re.search(r":\s*(\w+)", correct_answer_line).group(1)
            raw_dir = "Raw"  
            os.makedirs(raw_dir, exist_ok=True)
            new_image_path = os.path.join(raw_dir, image_name + ".png")
            os.rename(filename, new_image_path)
            print_debug(f"Renamed 'image.png' to '{image_name}.png' and moved to '{raw_dir}' directory.")
        else:
            print_error("Correct answer not found.")

        if debug:
            print_debug("Sending some numbers to netcat...")
        process.stdin.write("1234\n".encode())
        process.stdin.flush()

        if debug:
            print_debug("Receiving netcat response...")
        response = process.stdout.readline().decode().strip()
        print(response)

        second_line = process.stdout.readline().decode().strip()
        match = re.search(r"Correct Answer: (\w+)", second_line)
        if match:
            image_name = match.group(1)
            raw_dir = "RawV" #Change this one to where RAW images are. 
            os.makedirs(raw_dir, exist_ok=True)
            new_image_path = os.path.join(raw_dir, image_name + ".png")
            os.rename(filename, new_image_path)
            print_debug(f"Renamed 'image.png' to '{image_name}.png' and moved to '{raw_dir}' directory.")
        else:
            print_error("Correct answer not found.")

    process.stdin.write('\n'.encode())
    process.stdin.flush()
    print(colored("Last One.", 'blue'))
    response = process.stdout.readline().decode().strip()
    print(response)
    process.stdin.write('\n'.encode())
    process.stdin.flush()
    response = process.stdout.readline().decode().strip()
    print(colored(response, 'blue'))

