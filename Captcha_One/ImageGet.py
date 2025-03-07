import binascii
import argparse
import subprocess
from termcolor import colored

def print_debug(message):
    print(colored('[DEBUG] ', 'green') + message)

def print_error(message):
    print(colored('[ERROR] ', 'red') + message)

def get_hex_value_from_ncat(destination, verbose, debug):
    command = ['ncat', '--ssl', destination, '443']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    start_marker = '--- press Enter to continue ---'
    while True:
        line = process.stdout.readline().decode().strip()
        if line == start_marker:
            if debug:
                print_debug("Enter pressed, capturing hex value...")
            break
        if verbose:
            print(line)
        else:
            print(line, flush=True)

    process.stdin.write('\n'.encode())
    process.stdin.flush()

    hex_lines = []
    end_marker = '--- Type Answer to provided captcha 1 ---'
    while True:
        line = process.stdout.readline().decode().strip()
        if line == end_marker:
            if debug:
                print_debug("Hex conversion ended.")
            process.send_signal(subprocess.signal.SIGINT)
            process.wait()
            if debug:
                print_debug("Netcat process stopped.")
            break
        if verbose:
            print(line)
        else:
            print(line, flush=True)
        if not line.startswith("---"):
            hex_lines.append(line)

    return ''.join(hex_lines).strip()

def hex_to_png(hexadecimal, filename):
    try:
        binary_str = binascii.unhexlify(hexadecimal)

        with open(filename, 'wb') as f:
            f.write(binary_str)
        
        if debug:
            print_debug("Hex to PNG conversion completed. PNG saved to " + filename)
    except Exception as e:
        print_error("Error occurred during hex to PNG conversion: " + str(e))

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

    if args.source:
        if debug:
            print_debug("Connecting to " + args.source)
        hexadecimal = get_hex_value_from_ncat(args.source, args.verbose, debug)
    elif args.file:
        with open(args.file, 'r') as f:
            hexadecimal = f.read().strip()
    else:
        parser.error('Either --source or -f/--file must be provided.')

    filename = args.output

    if debug:
        print_debug("Converting hex to PNG...")
    hex_to_png(hexadecimal, filename)

