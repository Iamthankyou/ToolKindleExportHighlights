from __future__ import print_function
import re
import os
import argparse

#Format filename
def remove_chars(s):
    s = re.sub(" *: *", " - ", s)
    s = s.replace("?", "").replace("&", "and")
    s = re.sub(r"\((.+?)\)", r"- \1", s)
    s = re.sub(r"[^a-zA-Z\d\s;,_-]+", "", s)
    s = re.sub(r"^\W+|\W+$", "", s)
    return s


def parse_clippings(source_file, end_directory):
    if not os.path.isfile(source_file):
        raise IOError("ERROR: cannot find " + source_file)

    if not os.path.exists(end_directory):
        os.makedirs(end_directory)

    output_files = set()
    title = ""

    with open(source_file, "r") as f:
        for highlight in f.read().split("=========="):
            lines = highlight.split("\n")[1:]
            if len(lines) < 3 or lines[3] == "":
                continue
            title = lines[0]
            if title[0] == "\ufeff":
                title = title[1:]

            outfile_name = remove_chars(title) + ".txt"
            path = end_directory + "/" + outfile_name

            if outfile_name not in (list(output_files) + os.listdir(end_directory)):
                mode = "w"
                output_files.add(outfile_name)
                current_text = ""
            else:
                mode = "a"
                with open(path, "r") as textfile:
                    current_text = textfile.read()

            clipping_text = lines[3]

            with open(path, mode) as outfile:
                if clipping_text not in current_text:
                    outfile.write(clipping_text + "\n\n...\n\n")

    print("\nExported titles:\n")
    for i in output_files:
        print(i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract kindle clippings into a folder with nice text files"
    )
    parser.add_argument("-source", type=str, default="/Volumes/Kindle")
    parser.add_argument("-destination", type=str, default="/")

    args = parser.parse_args()

    if args.source[-4:] == ".txt":
        source_file = args.source
    elif args.source[-1] == "/":
        source_file = args.source + "/My Clippings.txt"
    else:
        source_file = args.source + "/My Clippings.txt"

    if args.destination[-1] == "/":
        destination = args.destination + "/ExportClippings/"
    else:
        destination = args.destination + "/ExportClippings/"

    parse_clippings(source_file, destination)
