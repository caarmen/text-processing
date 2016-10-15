import gzip
import os
import sys
import fileinput


def main():
    if sys.stdin.isatty():
        usage()

    here = os.path.dirname(os.path.realpath(__file__))
    frequency_data_path = os.path.join(here, "google-english-1gram-frequencies-2008.txt.gz")
    frequency_dict = {}
    with gzip.open(frequency_data_path, "rb") as f:
        for line in f:
            (word, frequency) = line.strip().split()
            frequency_dict[word] = frequency

    for line in fileinput.input():
        word = line.strip()
        if word in frequency_dict:
            print("%s\t%s") % (word, frequency_dict[word])
        else:
            sys.stderr.write("%s not found\n" % word)


def usage():
    print("This script reads a list of words from stdin and prints the frequency of each word to stdout.\n")
    print("Usage: cat /path/to/word_list.txt | python %s") % __file__
    exit(1)


if __name__ == "__main__":
    main()
