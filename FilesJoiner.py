import os
import argparse
import re

def concatenate_files(input_dir, regex, output_filename, output_dir, max_size):
    # Compile the regular expression
    regex = re.compile(regex)

    # Initialize the list of files
    files = []

    # Walk through the input directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for filename in filenames:
            # Add the file to the list if it matches the regex
            if regex.match(filename):
                files.append(os.path.join(dirpath, filename))

    # Sort the files
    files = sorted(files)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the output file and its size
    output_file = None
    output_size = 0

    # Initialize the output file and its size
    output_index = 1
    output_file = open(os.path.join(output_dir, output_filename + f"-{output_index}.txt"), 'w')

    print("Start join files")
    for f in files:
        # Open the input file
        with open(f, 'r') as input_file:
            # Read the input file
            content = input_file.read()

            # Check if the output file size would exceed the maximum
            content_length = len(content.encode('utf-8'))
            if output_size + content_length > max_size:
                # Close the current output file
                output_file.close()

                # Create a new output file with an incremented index
                output_index += 1
                output_file = open(os.path.join(output_dir, output_filename + '-' + str(output_index) + '.txt'), 'w')
                output_size = 0

            # Write the content to the output file
            # get file name from full path: f and input_dir
            file_name = f[len(input_dir) + 1:]
            print("join file: ", file_name)
            write_content = '# ' + file_name + '\n---\n' + content + '\n'
            output_file.write(write_content)
            output_size += len(content)

    # Close the last output file
    if output_file is not None:
        output_file.close()
        print("Finish join files")
        

if __name__ == '__main__':
    # get from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='The input directory')
    parser.add_argument('regex', help='The regular expression')
    parser.add_argument('output_filename', help='The output filename')
    parser.add_argument('output_dir', help='The output directory')
    parser.add_argument('max_size', type=int, help='The maximum size of the output file')
    args = parser.parse_args()

    # Call the concatenate_files function
    concatenate_files(args.input_dir, args.regex, args.output_filename, args.output_dir, args.max_size)
