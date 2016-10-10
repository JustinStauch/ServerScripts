#!/bin/bash

find $1/ -print | grep -E ".jpg-|.JPG-" | {
    while IFS= read -r line
    do
        stripped="${line%%-*}"
        
        if [ -z "$(equals-jpg.sh "$line" "$stripped")" ]
        then
            echo "Removing $line"
            rm -f "$line"
        else
            echo "Not Equal: $line"
        fi
    done
}
