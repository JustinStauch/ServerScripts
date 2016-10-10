#!/usr/bin/env python

import os
import filecmp
import sys

def get_all_mmv(path):
    result = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in dirnames + filenames:
            total_name = os.path.join(dirpath, filename)

            if ".mmv" in total_name:
                result.append(total_name)

    return result


def find_doubles(all_mmv):
    for mmv in all_mmv:
        for mmv2 in all_mmv:
            if not mmv == mmv2:
                if (not mmv.endswith('/')) and (not mmv2.endswith('/')):
                    if mmv[mmv.rfind('/') + 1:] == mmv2[mmv2.rfind('/') + 1:]:
                        print mmv + " is the same as " + mmv2

find_doubles(get_all_mmv(sys.argv[1]))
