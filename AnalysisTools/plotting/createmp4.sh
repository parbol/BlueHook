#!/bin/bash

CONCAT=$(echo $(ls *.png | sort -n -t _ -k 2) | sed -e "s/ /|/g")
ffmpeg -framerate 25 -i "concat:$CONCAT" -c:v libx264 -profile:v high -pix_fmt yuv420p output.mp4
