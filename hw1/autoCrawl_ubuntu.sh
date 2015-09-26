#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "./autoCrawl.sh URL_FILE_NAME"
    exit
fi
nutch inject crawl/crawldb $1

for i in `seq 1 20`;
do
  echo "round $i"
  nutch generate crawl/crawldb crawl/segments
  seg=`ls -d crawl/segments/2* | tail -1`
  echo $seg
  nutch fetch $seg
  nutch parse $seg
  nutch updatedb crawl/crawldb $seg
  printf "\n\n"
done

