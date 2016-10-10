#!/bin/bash

find $1/ -print | grep -E "*.jpg|*.JPG" | {
    while IFS= read -r line
    do
        datetime=$(date-jpg.sh "$line")
        
        if [[ ! (( -z "$datetime" )) ]]
        then
            year=$(echo "$datetime" | cut -d ':' -f 1)
            month=$(echo "$datetime" | cut -d ':' -f 2)

            if [ ! -d "$2/$year" ]
            then
                mkdir "$2/$year"
            fi

            if [ ! -d "$2/$year/$month" ]
            then
                mkdir "$2/$year/$month"
            fi

            filename=${line##*/}
            
            if [ -e "$2/$year/$month/$filename" ]
            then
                convert "$line" "Temp_IMG_A.rgba"
                convert "$2/$year/$month/$filename" "Temp_IMG_B.rgba"
                if [ ! -z "$(cmp "Temp_IMG_A.rgba" "Temp_IMG_B.rgba")" ]
                then
                    echo "Name Collision $line in $2/$year/$month/"
                    num=1
                    
                    if [[ -e "$2/$year/$month/$filename-$num" ]]
                    then
                        convert "$2/$year/$month/$filename-$num" "Temp_IMG_B.rgba"
                    fi

                    while [[ -e "$2/$year/$month/$filename-$num" && ! -z "$(cmp "Temp_IMG_A.rgba" "Temp_IMG_B.rgba")" ]]
                    do
                        num=$((num + 1))
                        convert "$2/$year/$month/$filename-$num" "Temp_IMG_B.rgba"
                    done

                    if [ ! -e "$2/$year/$month/$filename-$num" ]
                    then
                        echo "Moving $line as $2/$year/$month/$filename-num"
                        mv "$line" "$2/$year/$month/$filename-$num"
                    else
                        echo "Already exists $line as $2/$year/$month/$filename-num"
                    fi
                else
                    echo "Already exists $line in $2/$year/$month/"
                fi
            else
                echo "Moving $line to $2/$year/$month/"
                mv "$line" "$2/$year/$month/"
            fi
        else
            echo "No Date: $line"
        fi
    done
}
