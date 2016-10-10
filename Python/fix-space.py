#!/usr/bin/env python

import sys
import subprocess
import os

def remove_space(file_path):
    file_name = file_path
    file_dir = ""

    if "/" in file_path:
        slash = file_path.rfind("/")
        file_name = file_path[slash + 1:]
        file_dir = file_path[:slash + 1]

    space = file_name.rfind(" ")
    under = file_name.rfind("_")
    point = file_name.rfind(".")

    if under < space and space < point:
        file_name = file_name[:space] + file_name[point:]

    return file_dir + file_name

def has_space(file_path):

    file_name = file_path
    file_dir = ""

    if "/" in file_path:
        slash = file_path.rfind("/")
        file_name = file_path[slash + 1:]
        file_dir = file_path[:slash + 1]

    return "IMG_" in file_name and " " in file_name and "." in file_name

def fix_all(files):

    to_fix = [f for f in files if has_space(f)]

    for fix in to_fix:
        fix_name(fix)

def fix_name(file_path):

    if not has_space(file_path):
        return

    file_name = file_path
    file_dir = ""

    if "/" in file_path:
        slash = file_path.rfind("/")
        file_name = file_path[slash + 1:]
        file_dir = file_path[:slash + 1]

    file_new_name = remove_space(file_name)

    if os.path.isfile(file_dir + file_new_name):

        if jpg_equal(file_path, file_dir + file_new_name):
            print file_path + " already exists as " + file_dir + file_new_name + ", Deleting it."
            subprocess.check_output(['rm', '-f', file_path])
            return

        copy_num = 1

        file_new_name = file_new_name[:file_new_name.rfind(".")] + "_" + str(copy_num) + file_new_name[file_new_name.rfind("."):]

        while os.path.isfile(file_dir + file_new_name):

            if jpg_equal(file_path, file_dir + file_new_name):
                print file_path + " already exists as " + file_dir + file_new_name + ", Deleting it."
                subprocess.check_output(['rm', '-f', file_path])
                return

            copy_num += 1

            file_new_name = file_new_name[:file_new_name.rfind("_") + 1] + str(copy_num) + file_new_name[file_new_name.rfind("."):]

    if os.path.isfile(file_dir + file_new_name):
        sys.stderr.write("Tried to rename " + file_path + " to " + file_dir + file_new_name + ". Already taken\n")

    print "Renaming " + file_path + " to " + file_dir + file_new_name
    subprocess.check_output(['mv', file_path, file_dir + file_new_name])


def jpg_equal(file1, file2):
    
    try:
        subprocess.check_output(['equals-jpg.sh', file1, file2])
    except Exception, ex:
        return False

    return True

def get_all_files(source):

    return subprocess.check_output(['find', source + "/", '-print']).decode('utf-8').split('\n')


fix_all(get_all_files(sys.argv[1]))
