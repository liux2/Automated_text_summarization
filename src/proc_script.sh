#!/usr/bin/env bash

#get content of input dir and echo to file_list.txt
cd ..;
for file in input_files/*;
# run the actual program
do
  python3 src/main.py -i "$file" -o output_files -p 3 -w 50
  # break
done
