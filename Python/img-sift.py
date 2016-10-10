#!/usr/bin/env python

import sys
import subprocess
import os

# Remove the hyphen and number from the picture's name.
#
# A string indicating the path to the picture, or just the picture's name.
def get_regular_name(picture_path):


    hyph = picture_path.rfind("-")
    point = picture_path.rfind(".")
    under = picture_path.rfind("_")

    if under < hyph and hyph < point:
        return picture_path[:hyph] + picture_path[point:]
    else:
        return picture_path

def sort_all_jpegs(source, dest):
    all_files = subprocess.check_output(['find', source + '/', '-print']).decode('utf-8').split('\n')

    print "here"
    all_imgs = [f for f in all_files if (".jpg" in f or ".JPG" in f) and (not "._" in f)]
    print "here"

    right_imgs = [f for f in all_imgs if not is_video_preview(f)]

    print "here"

    for img in all_imgs:
        sort_jpeg(img, dest)

def sort_jpeg(image_path, dest):

    raw_date = get_jpeg_date(image_path)

    if raw_date == '':
        return

    img_date = raw_date.split(':')

    img_raw_name = image_path[image_path.rfind("/") + 1:]
    img_new_name = get_regular_name(img_raw_name)

    new_dest = dest + "/" + img_date[0] + "/" + img_date[1] + "/"

    make_directories(new_dest)

    if os.path.isfile(new_dest + img_new_name):

        equal = True

        try:
            subprocess.check_output(['equals-jpg.sh', new_dest + img_new_name, image_path])
        except Exception, ex:
            equal = False

        if equal:
            print image_path + " already exists as " + new_dest + img_new_name
            return

        copy_num = 1

        img_new_name = img_new_name[:img_new_name.rfind(".")] + "_" + str(copy_num) + img_new_name[img_new_name.rfind("."):]

        while os.path.isfile(new_dest + img_new_name):

            equal = True

            try:
                subprocess.check_output(['equals-jpg.sh', new_dest + img_new_name, image_path])
            except Exception, ex:
                equal = False

            if equal:
                print image_path + " already exists as " + new_dest + img_new_name
                return

            copy_num += 1

            img_new_name = img_new_name = img_new_name[:img_new_name.rfind("_") + 1] + str(copy_num) + img_new_name[img_new_name.rfind("."):]

    if os.path.isfile(new_dest + img_new_name):
        sys.stderr.write("Tried to move " + image_path + " to " + new_dest + img_new_name + ". Already exists\n")
        return

    print "Moving " + image_path + " as " + new_dest + img_new_name
    subprocess.check_output(['mv', image_path, new_dest + img_new_name])

def get_jpeg_date(jpg_path):
    output = subprocess.check_output(['file', jpg_path]).decode('utf-8').split(' ')

    raw_date_time = [s for s in output if 'datetime=' in s]

    if len(raw_date_time) == 0:
        return ''

    date_time = raw_date_time[0]

    return date_time[date_time.rfind('=') + 1:]

def make_directories(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_video_preview(picture_path):
    output = subprocess.check_output(['file', picture_path]).decode('utf-8')

    return "720x1280" in output or "1280x720" in output or "1920x1080" in output or "1080x1920" in output


sort_all_jpegs(sys.argv[1], sys.argv[2])
