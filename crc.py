#!python3

import glob
import zlib
import os
import sys
from multiprocessing import Pool, freeze_support
import argparse


def get_crc(file):
    cur_crc = 0
    with open(file, 'rb') as f:
        while True:
            cur_data = f.read(8192)
            if not cur_data:
                break
            cur_crc = zlib.crc32(cur_data, cur_crc)
    return file, format(cur_crc & 0xFFFFFFFF, '08x')


def main():

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'pattern', help='wildcard pattern for matching files. e.g. *.yuv')
        args = parser.parse_args()
        pattern = args.pattern
    else:
        pattern = '*.*'

    files = glob.iglob(os.path.join(os.getcwd(), pattern))
    p = Pool()
    res = p.imap(get_crc, files)
    for file, crc in res:
        print(crc, file)


if __name__ == '__main__':
    freeze_support()
    main()
