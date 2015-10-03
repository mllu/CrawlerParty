#!/bin/bash


if [ "$#" -ne 2 ]; then
    echo "./autoCrawl.sh URL_FILE_NAME NUMBER_OF_RUN"
    exit
fi

rm -rf crawl

./runtime/local/bin/nutch inject crawl/crawldb $1

for i in `seq 1 $2`;
do
  echo "round $i"
  echo "=========== Generate Phase ==========="
  ./runtime/local/bin/nutch generate crawl/crawldb crawl/segments
  seg=`ls -d crawl/segments/2* | tail -1`
  echo $seg
  echo "=========== Fetch Phase ==========="
  ./runtime/local/bin/nutch fetch $seg
  echo "=========== Parse Phase ==========="
  ./runtime/local/bin/nutch parse $seg
  echo "=========== Update Phase ==========="
  ./runtime/local/bin/nutch updatedb crawl/crawldb $seg
  printf "\n\n"
done

