#!/usr/bin/env python

import sys
import subprocess

def rename(picture_path):
    hyph = picture_path.rfind("-")
    point = picture_path.rfind(".")

    return picture_path[:point] + "_" + picture_path[hyph + 1:] + picture_path[point:hyph]

def get_problem_pics(directory):
    all_pics = subprocess.check_output(['find', directory + '/', '-print']).decode('utf-8').split('\n')

    return [s for s in all_pics if (".jpg-" in s) or (".JPG-" in s)]

def fix_names(pics):
    
    for pic in pics:
        print "Changing " + pic + " to " + rename(pic)
        subprocess.check_output(['mv', pic, rename(pic)])

def run_fix(directory):
    fix_names(get_problem_pics(directory))



run_fix(sys.argv[1])
