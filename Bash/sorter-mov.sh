#!/bin/bash

find $1/ -print | grep -E "*.mov|*.MOV|*.mp4|*.MP4" | {
    while IFS= read -r line
    do
        datetime=$(date-mov.sh "$line")

        if [[ ! -z "$datetime" ]]
        then
            year=$(echo "$datetime" | cut -d '-' -f 1)
            month=$(echo "$datetime" | cut -d '-' -f 2)

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
                if [ ! -z "$(cmp "$2/$year/$month/$filename" "$line")" ]
                then
                    echo "Name Collision $line at $2/$year/$month"
                    num=1
                    while [[ -e "$2/$year/$month/$filename-$num" && ! -z "$(cmp "$2/$year/$month/$filename-$num" "$line")" ]]
                    do
                        num=$((num + 1))
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
