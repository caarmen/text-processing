import gzip
import os
import sys
import fileinput

def main(argv):
    if sys.stdin.isatty():
        usage()

    here = os.path.dirname(os.path.realpath(__file__))
    dbpath = os.path.join(here, "google-english-1gram-frequencies-2008.txt.gz")
    frequency_db = {}
    with gzip.open(dbpath, "rb") as f:
        for line in f:
            (word, frequency) = line.strip().split()
            frequency_db[word] = frequency

    for line in fileinput.input():
        word = line.strip()
        if word in frequency_db:
            frequency = frequency_db[word]
            print("%s\t%s") % (word, frequency)
        else:
            print >> sys.stderr, ("%s not found") % (word)


def usage():
    print ("This script reads a list of words from stdin and prints the frequency of each word to stdout.")
    print
    print ("Usage: cat /path/to/wordlist.txt | python %s") % (__file__)
    exit(1)

if __name__ == "__main__":
    main(sys.argv)
