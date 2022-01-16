#!/bin/bash

# Replace transparency in input image into whte background

color=white
for input in $(ls *png)
do
    echo ${input}
    output="no_transparency_${input}"
    convert ${input} -background ${color} -alpha remove -flatten -alpha off ${output}
done