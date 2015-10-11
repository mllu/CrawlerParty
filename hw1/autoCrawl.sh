#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "./autoCrawl.sh URL_FILE_NAME NUMBER_OF_RUN OUT_DIR"
    exit
fi
nutch inject $3/crawldb $1

for i in `seq 1 $2`;
do
  echo "round $i"
  echo "=========== Generate Phase ==========="
  nutch generate $3/crawldb $3/segments
  seg=`ls -d $3/segments/2* | tail -1`
  echo $seg
  echo "=========== Fetch Phase ==========="
  nutch fetch $seg
  echo "=========== Parse Phase ==========="
  nutch parse $seg
  echo "=========== Update Phase ==========="
  nutch updatedb $3/crawldb $seg

  FILE="/tmp/outlinks"
  if [ -f "$FILE" ]
  then
    echo "=========== Inject new outlinks ==========="
    nutch inject $3/crawldb /tmp/outlinks
    mv /tmp/outlinks /tmp/outlinks$i
  fi
  printf "\n\n"
done

