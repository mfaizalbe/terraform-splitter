#!/usr/bin/env python3
import os
import re
import sys

# default filenames for terraform blocks
BASE_MAP = {
    "terraform": "terraform.tf",
    "provider": "provider.tf",
    "variable": "variables.tf",
    "data": "data.tf",
    "output": "outputs.tf",
    "module": "modules.tf",
    "locals": "locals.tf"
}

def find_main_tf(start_dir):
    # search for main.tf in current folder or subfolders
    for root, _, files in os.walk(start_dir):
        if "main.tf" in files:
            return os.path.join(root, "main.tf")
    return None

def split_terraform(main_tf_path):
    # get folder path of main.tf
    current_dir = os.path.dirname(main_tf_path)
    # dictionary to keep open file handles for resource types
    resource_files = {}

    # variables to track current block and braces
    block_type = None   # current terraform block type
    brace_count = 0     # track open and close braces
    current_file = None
    line_buffer = []    # buffer to store comments or empty lines before a block

    with open(main_tf_path) as f:
        for line in f:
            # if line is a comment or empty and not inside a block, add to buffer
            if re.match(r'^\s*(#|//|$)', line) and brace_count == 0:
                line_buffer.append(line)
                continue

            # detect start of a terraform block
            match = re.match(r'^\s*(terraform|provider|variable|data|resource|output|module|locals)\b', line)
            if match and brace_count == 0:
                block_type = match.group(1)

                # decide which file to write based on block type
                if block_type == "resource":
                    # get resource type for splitting
                    res_match = re.match(r'^\s*resource\s+"([^"]+)"', line)
                    if res_match:
                        res_name = res_match.group(1)
                        # aws_s3_bucket → s3.tf
                        short_name = res_name.replace("aws_", "").split("_")[0]
                        filename = os.path.join(current_dir, f"{short_name}.tf")
                        if filename not in resource_files:
                            # open file for writing resource type
                            resource_files[filename] = open(filename, "w")
                        current_file = resource_files[filename]
                else:
                    # normal block → use predefined file
                    filename = os.path.join(current_dir, BASE_MAP.get(block_type))
                    current_file = open(filename, "a")

                # write any buffered comments to the file before the block
                for buf_line in line_buffer:
                    current_file.write(buf_line)
                # clear the buffer after writing
                line_buffer.clear()

            # write the current line to the appropriate file
            if current_file:
                current_file.write(line)

            # update brace count to track block start/end
            brace_count += line.count("{")
            brace_count -= line.count("}")

            # reset variables when block ends
            if brace_count == 0:
                block_type = None
                current_file = None

    # close all open resource files
    for f in resource_files.values():
        f.close()

    # print completion message
    print(f"terraform files split completed in {current_dir}")

if __name__ == "__main__":
    # start from current working directory
    start_dir = os.getcwd()
    # find main.tf automatically
    main_tf_path = find_main_tf(start_dir)
    if not main_tf_path:
        print("error: no main.tf found")
        sys.exit(1)
    # run the terraform splitter
    split_terraform(main_tf_path)