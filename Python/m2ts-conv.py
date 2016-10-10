#!/usr/bin/env python

import sys
import subprocess
import os
import filecmp


def get_date(vid_path):
    vid_name = vid_path[vid_path.rfind('/') + 1:]

    return [vid_name[0:4], vid_name[4:6], vid_name[6:8], vid_name[8:10], vid_name[10:12], vid_name[12:14]]


def format_date(file_date):
    return file_date[0] + "-" + file_date[1] + "-" + file_date[2] + " " + file_date[3] + ":" + file_date[4] + ":" + file_date[5]

def change_extension(file_name):
    return file_name[:file_name.rfind(".m2ts")] + ".MP4"

def convert_to_mp4(vid_path, dest):
    
    vid_date = get_date(vid_path)

    new_dest = dest + "/" + vid_date[0] + "/" + vid_date[1] + "/"

    make_directories(new_dest)

    new_name = new_dest + "OVC_" + change_extension(vid_path[vid_path.rfind('/') + 1:])

    if os.path.isfile(new_name):
        subprocess.check_output(['rm', '-f', new_name])

    print "Converting " + vid_path + " to " + new_name

    subprocess.check_output(['ffmpeg', '-i', vid_path, '-vcodec', 'copy', '-acodec', 'copy', '-metadata', 'creation_time=' + format_date(vid_date), new_name])



def make_directories(path):
    if not os.path.exists(path):
        os.makedirs(path)

def convert_all(source, dest):
    all_files = subprocess.check_output(['find', source + "/", '-print']).decode('utf-8').split('\n')

    all_vids = [f for f in all_files if (".m2ts" in f) and (not "._" in f)]

    for vid in all_vids:
        convert_to_mp4(vid, dest)


convert_all(sys.argv[1], sys.argv[2])
