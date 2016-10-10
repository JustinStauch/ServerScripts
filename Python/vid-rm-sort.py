#!/usr/bin/env python

import sys
import subprocess
import os
import filecmp

def get_regular_name(vid_path):
    
    vid_name = vid_path
    vid_dir = ""

    if "/" in vid_path:
        slash = vid_path.rfind("/")
        vid_name = vid_path[slash + 1:]
        vid_dir = vid_path[:slash + 1]

    hyph = vid_name.rfind("-")
    point = vid_name.rfind(".")
    under = vid_name.rfind("_")
    space = vid_name.rfind(" ")

    if under < hyph and hyph < point:
        return vid_dir + vid_name[:hyph] + vid_name[point:]
    
    if under < space and space < point:
        return vid_dir + vid_name[:space] + vid_name[point:]

    return vid_dir + vid_name


def get_video_date(vid_path):
    output = subprocess.check_output(['mediainfo', vid_path]).decode('utf-8').split('\n')

    all_tagged_dates = [s for s in output if "Tagged date" in s]

    if len(all_tagged_dates) == 0:
        return []

    tagged_date_line = all_tagged_dates[0]

    full_date = tagged_date_line[tagged_date_line.rfind("UTC") + 4:]
    
    return full_date[:10].split('-')


def sort_all_videos(source, dest):
    all_files = subprocess.check_output(['find', source + '/', '-print']).decode('utf-8').split('\n')

    all_vids = [f for f in all_files if (".mov" in f or ".MOV" in f or ".mp4" in f or ".MP4" in f) and (not "._" in f)]

    for vid in all_vids:
        sort_vid(vid, dest)


def sort_vid(vid_path, dest):

    vid_date = get_video_date(vid_path)

    new_dest = dest + "/NoDate/"

    if len(vid_date) == 1:
        new_dest = dest + vid_date[0]
    elif len(vid_date) > 1:
        new_dest = dest + "/" + vid_date[0] + "/" + vid_date[1] + "/"

    vid_basename = vid_path[vid_path.rfind("/") + 1:]
    vid_new_name = get_regular_name(vid_basename)

    make_directories(new_dest)
    
    if os.path.isfile(new_dest + vid_new_name):
        
        if filecmp.cmp(new_dest + vid_new_name, vid_path):
            print vid_path + " already exists as " + new_dest + vid_new_name + ". Deleting it."
            subprocess.check_output(['rm', '-f', vid_path])
            return

        copy_num = 1

        vid_new_name = vid_new_name[:vid_new_name.rfind(".")] + "_" + str(copy_num) + vid_new_name[vid_new_name.rfind("."):]

        while os.path.isfile(new_dest + vid_new_name):

            if filecmp.cmp(new_dest + vid_new_name, vid_path):
                print vid_path + " already exists as " + new_dest + vid_new_name + ". Deleting it."
                subprocess.check_output(['rm', '-f', vid_path])
                return

            copy_num += 1

            vid_new_name = vid_new_name[:vid_new_name.rfind("_") + 1] + str(copy_num) + vid_new_name[vid_new_name.rfind("."):]

    if os.path.isfile(new_dest + vid_new_name):
        sys.stderr.write("Tried to move " + vid_path + " to " + new_dest + img_new_name + ". Already exists\n")
        return

    print "Moving " + vid_path + " as " + new_dest + vid_new_name
    
    subprocess.check_output(['mv', vid_path, new_dest + vid_new_name])

def make_directories(path):
    if not os.path.exists(path):
        os.makedirs(path)


sort_all_videos(sys.argv[1], sys.argv[2])
