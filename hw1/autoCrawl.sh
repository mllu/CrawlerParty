#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "./autoCrawl.sh URL_FILE_NAME NUMBER_OF_RUN"
    exit
fi
nutch inject crawl/crawldb $1

for i in `seq 1 $2`;
do
  echo "round $i"
  echo "=========== Generate Phase ==========="
  nutch generate crawl/crawldb crawl/segments
  seg=`ls -d crawl/segments/2* | tail -1`
  echo $seg
  echo "=========== Fetch Phase ==========="
  nutch fetch $seg
  echo "=========== Parse Phase ==========="
  nutch parse $seg
  echo "=========== Update Phase ==========="
  nutch updatedb crawl/crawldb $seg

  FILE="/tmp/outlinks"
  if [ -f "$FILE" ]
  then
    echo "=========== Inject new outlinks ==========="
    nutch inject crawl/crawldb /tmp/outlinks
  fi
  printf "\n\n"
done

