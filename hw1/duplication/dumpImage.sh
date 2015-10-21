#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "./dumpImage.sh segmentDir outputDir"
    exit
fi

nutch dump -outputDir $2 -segment $1 -mimetype image/png image/jpeg image/x-ms-bmp image/vnd.microsoft.icon image/gif
