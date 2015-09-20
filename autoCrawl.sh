#!/bin/sh
nutch inject crawl/crawldb urls
nutch generate crawl/crawldb crawl/segments
s1=`ls -d crawl/segments/2* | tail -1`
echo $s1
nutch fetch $s1
nutch parse $s1
nutch updatedb crawl/crawldb $s1

