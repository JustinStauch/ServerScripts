#!/usr/bin/env python

import sys
import subprocess
import os
import filecmp

def delete_copies(vids):

    to_delete = []

    for index in range(len(vids) - 1):
        if vids[index] in to_delete:
            continue

        to_delete += [vid for vid in vids[index + 1:] if filecmp.cmp(vids[index], vid)]

    for copy in to_delete:
        print "Deleting " + copy
        os.remove(copy)


def group_videos(path):
    all_vids = get_all_videos(path)

    for vid in all_vids:
        if "clip" in vid or "Clip" in vid or "Cache" in vid or "cache" in vid:
            continue

        prefix = vid[:vid.rfind('.')] + '_'
        extension = vid[vid.rfind('.'):].upper()
        extension_up = extension.upper()
        extension_low = extension.lower()

        group = [video for video in all_vids if video.startswith(prefix) and (video.endswith(extension) or video.endswith(extension_up) or video.endswith(extension_low))]

       
        if len(group) > 0:
            delete_copies([vid] + group)
    
def get_all_videos(path):
    result = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in dirnames + filenames:
            total_name = os.path.join(dirpath, filename)
            
            if ".MP4" in total_name or ".mp4" in total_name or ".MOV" in total_name or ".mov" in total_name:
                result.append(total_name)

    return result

group_videos(sys.argv[1])
print "Done"
