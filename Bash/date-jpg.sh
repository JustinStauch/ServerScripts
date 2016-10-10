substring=datetime

for x in `file "$1"`
do
    if [[ "$x" =~ "$substring" ]]
    then
        echo "$x" | cut -d '=' -f 2
    fi
done
