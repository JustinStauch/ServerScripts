#!/usr/bin/env python

import sys
import subprocess
import os
import filecmp

def delete_copies(images):

    imgs = []

    for img in images:
        if os.path.isfile(img):
            imgs.append(img)

    if '(' in imgs[0]:
       delete_copies_brackets(imgs)
       return

    for img in imgs:
        if not "IMG_" in img:
            return

    to_delete = []

    for index in range(len(imgs) - 1):
        if imgs[index] in to_delete:
            continue

        to_delete += [img for img in imgs[index + 1:] if filecmp.cmp(imgs[index], img)]

    for copy in to_delete:
        print "Deleting " + copy
        os.remove(copy)


# Handles instances where the image name has brackets.
def delete_copies_brackets(imgs):
    
    copy_lists = []

    for i in range(len(imgs) - 1):
        
        for group in copy_lists:
            if imgs[i] in group:
                continue

        copy_lists.append([imgs[i]] + [img for img in imgs[i + 1:] if filecmp.cmp(imgs[i], img)])

    for copies in copy_lists:
        keep = max(copies, key=len)

        for copy in copies:
            if not copy == keep:
                print "Deleting " + copy
                os.remove(copy)

def group_images(path):
    all_imgs = get_all_images(path)

    for img in all_imgs:
        if "clip" in img or "Clip" in img or "Cache" in img or "cache" in img:
            continue

        if not os.path.isfile(img):
            continue

        prefix = img[:img.rfind('.')]
        extension = img[img.rfind('.'):]
#        extension_up = extension.upper()
        extension_low = extension.lower()

        group = [image for image in all_imgs if image.startswith(prefix) and (image.endswith(extension) or image.endswith(extension_low)) and not image == img]

       
        if len(group) > 0:
            delete_copies([img] + group)
    

def get_all_images(path):
    result = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in dirnames + filenames:
            total_name = os.path.join(dirpath, filename)
            
            if ".JPG" in total_name or ".jpg" in total_name:
                result.append(total_name)

    return result

group_images(sys.argv[1])
print "Done"
