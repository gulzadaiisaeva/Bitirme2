# this reads file and show to screen. Files with white spaces characters dont work 

inotifywait -m ~/Desktop/bitirme -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        echo "Going to remove '$file' ....."
        cat $file
        #rm $file
        echo "Removed..."
    done

