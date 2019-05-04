#Detecting file which have white space characters
inotifywait -m -r -e moved_to -e create -e close_write --format "%e %w%f" ~/Desktop/bitirme |
  while read evt dir file; do
    echo "Fullpath: $dir $file" #note the space between $dir and $file
    rm $file
done

