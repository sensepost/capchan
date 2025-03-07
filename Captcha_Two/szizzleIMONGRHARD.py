import binascii
import argparse
import subprocess
from termcolor import colored
import os
import re
import time

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
    process.stdin.write('\n'.encode())
    process.stdin.flush()

def press_enter(process, debug):
    hex_lines = []
    end_marker_pattern = r'--- Type Answer to provided captcha \d+ ---'
    correct_answer_pattern = r'Correct Answer: ([a-zA-Z]{4})'
    wrong_answer_pattern = r'Wrong!'
    correct_pattern = r'Correct!'

    while True:
        line = process.stdout.readline().decode().strip()
        if re.match(end_marker_pattern, line):
            if debug:
                print_debug("Hex conversion ended.")
            break
        if re.match(correct_answer_pattern, line):
            if debug:
                print_debug("Just Keep Swimming")
            correct_answer = re.match(correct_answer_pattern, line).group(1)
            print_debug("Correct Answer: " + colored(correct_answer, 'yellow'))
            continue
        if re.match(wrong_answer_pattern, line):
            if debug:
                print_debug("Received 'Wrong!' response from netcat.")
            break
        if re.match(correct_pattern, line):
            if debug:
                print_debug("Received 'Correct!' response from netcat.")
            continue
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

def remove_control_characters(text): #THis caused me pain before knowing what it was.
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

    correct_count = 0
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
            print_debug("Running NyaDetermine.py...")
        image_determine_command = ['python3', 'nyadetermine.py']
        subprocess.run(image_determine_command)

        if debug:
            print_debug("Reading contents of output.txt...")
        with open("output.txt", "r") as f:
            file_contents = f.read().strip()

        if debug:
            print_debug("Sending contents of output.txt to netcat...")
        file_contents = remove_control_characters(file_contents)[:4]
        print_debug("Value sent to netcat: " + file_contents)    
        process.stdin.write(file_contents.encode() + '\n'.encode())
        process.stdin.flush()

        if debug:
            print_debug("Receiving netcat response...")
        response = process.stdout.readline().decode().strip()
        print(response)

        if response == "Correct!":
            correct_count += 1
            if correct_count < 120:
                process.stdin.write('\n'.encode())
                process.stdin.flush()
                line = process.stdout.readline().decode().strip()
                print(colored(f"=-=-=- Count: {correct_count} -=-=-=", 'magenta'))
                print(colored(f"=-=-=- Iteration: {i} -=-=-=", 'blue'))
            else:
                print(colored("We Ball x2.", 'blue'))
                response = process.stdout.readline().decode().strip()
                print(response)
                process.stdin.write('\n'.encode())
                process.stdin.flush()
                response = process.stdout.readline().decode().strip()
                print(colored(response, 'blue'))
