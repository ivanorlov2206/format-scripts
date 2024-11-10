#!/usr/bin/python3
import argparse
import re

WARN_COLOR = '\033[93m'
ERR_COLOR = '\033[91m'
OK_COLOR = '\033[92m'
END_COLOR = '\033[0m'

def question(question_text):
    ans = input(f"{question_text} (y/n)?: ").rstrip().lower()
    if ans == 'n':
        print(f"{ERR_COLOR}Fix that, motherfucker!{END_COLOR}")
        exit()
    elif ans == 'y':
        return
    else:
        print("Sorry, I can't recognize this shit")


def process_all_allocs(lines):
    alloc_pattern = re.compile(r'^\+\t.*((alloc)|(dup)).*\(.*\)')
    for line in lines:
        if not alloc_pattern.match(line):
            continue
        print(f"\n{WARN_COLOR}Found the following (possible) memory allocation:{END_COLOR}\n")
        print(f"{line}\n")
        question("Is possible memory allocation error processed?")
        question("Is it cleaned up in the corresponding free, if applicable?")


def process_all_includes_defines(lines):
    include_pattern = re.compile(r'^\+\t?#((include)|(define))')
    for line in lines:
        if not include_pattern.match(line):
            continue
        print(f"\n{WARN_COLOR}Found the following include/define:{END_COLOR}\n")
        print(f"{line}\n")
        question("Is it used?")

    
def analyze_file(fname):
    f = open(fname, "r")
    lines = [x.rstrip() for x in f.readlines()]
    f.close()

    process_all_allocs(lines)
    process_all_includes_defines(lines)
    print(f"\n{OK_COLOR}You're good to go!{END_COLOR}\n")


parser = argparse.ArgumentParser("error-checker")
parser.add_argument("file", help="patch file for analysis")

args = parser.parse_args()
analyze_file(args.file)
