#!/bin/bash

if [[ -e $1 && -e $2 ]]
then
    convert "$1" "/tmp/Temp_IMG_A.bmp"
    convert "$2" "/tmp/Temp_IMG_B.bmp"

    cmp "/tmp/Temp_IMG_A.bmp" "/tmp/Temp_IMG_B.bmp"
fi
