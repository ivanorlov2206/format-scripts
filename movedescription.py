#!/usr/bin/python3
import argparse
import glob

def read_data(src_p, dst_p):
    with open(src_p, "r") as src:
        src_lines = src.readlines()

    with open(dst_p, "r") as dst:
        dst_data = dst.read()

    return src_lines, dst_data

def copy_cl(src_lines, dst_data):
    header = ""
    for src_l in src_lines:
        src_l = src_l.rstrip()
        if src_l.startswith("Subject:"):
            header = src_l[src_l.index("]") + 2:]
            break
    if header == "":
        print("Error: Can't find the subject")
        exit(-1)
    dst_data = dst_data.replace("*** SUBJECT HERE ***", header)

    body = ""
    recording = False
    for src_l in src_lines:
        src_l = src_l.rstrip()
        if src_l.startswith("Ivan Orlov (") and src_l[-1] == ':':
            break
        if src_l == "" and not recording:
            recording = True
        elif recording:
            body += src_l + "\n"
    body = body.rstrip()
    if body == "":
        print("Error: CL has an empty body")
        exit(-1)
    dst_data = dst_data.replace("*** BLURB HERE ***", body)
    return dst_data

def process_file(src_p, dst_p):
    src_lines, dst_data = read_data(src_p, dst_p)
    if "-0000-" not in src_p:
        dst_data = copy_changelog(src_lines, dst_data)
    else:
        dst_data = copy_cl(src_lines, dst_data)
    with open(dst_p, "w") as dst:
        dst.write(dst_data)


def copy_changelog(src_lines, dst_data):
    changelog = ""
    recording = False
    for src_l in src_lines:
        src_l = src_l.rstrip()
        if (recording and src_l == "") or (src_l != "---" and (src_l.endswith("+") or src_l.endswith("-"))):
            break
        if src_l == "---" and not recording:
            recording = True
        elif recording:
            changelog += src_l + "\n"
    if changelog == "":
        print("Error: no changelog found")
        exit(-1)
    b_ind = dst_data.index("---\n")
    dst_data = dst_data[:b_ind+4] + changelog + dst_data[b_ind+3:]
    return dst_data

parser = argparse.ArgumentParser("copychange")
parser.add_argument('-f', '--file', action='store_true')
parser.add_argument('source', help='Patch to copy from')
parser.add_argument('destination', help='Patch to copy to')

args = parser.parse_args()


if args.file:
    process_file(args.source, args.destination)
else:
    input_files = sorted([x for x in glob.glob(f"{args.source}/*.patch")])
    output_files = sorted([x for x in glob.glob(f"{args.destination}/*.patch")])
    if len(input_files) != len(output_files):
        print("Error: files count doesn't match")
        exit(-1)
    for i in range(len(input_files)):
        process_file(input_files[i], output_files[i])
