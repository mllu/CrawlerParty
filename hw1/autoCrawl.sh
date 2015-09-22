#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "./autoCrawl.sh URL_FILE_NAME"
    exit
fi
nutch inject crawl/crawldb $1

nutch generate crawl/crawldb crawl/segments
s1=`ls -d crawl/segments/2* | tail -1`
echo $s1
nutch fetch $s1
nutch parse $s1
nutch updatedb crawl/crawldb $s1

nutch generate crawl/crawldb crawl/segments -topN 1000
s2=`ls -d crawl/segments/2* | tail -1`
echo $s2
nutch fetch $s2
nutch parse $s2
nutch updatedb crawl/crawldb $s2

nutch generate crawl/crawldb crawl/segments -topN 1000
s3=`ls -d crawl/segments/2* | tail -1`
echo $s3
nutch fetch $s3
nutch parse $s3
nutch updatedb crawl/crawldb $s3


