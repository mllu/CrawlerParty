# Read statistics

Run readStatistics to retrieve the statistics from crawldb

# Dedupliction

Run the readContentParseTextParseData.py to read the content, parse data and parse text from what we crawled.
Then run the duplicateExactNear.py to determine the duplicate.
```
python readContentParseTextParseData.py segmentDir outputDir
python duplicateExactNear.py inputDir isExact
```
The output of duplicateExactNear will go to standard output. isExact should be either true or false.

## Idea of deduplication
We extract three features from the data we crawled: content, metadata and parse text. For metadata, we exclude the information about the crawler, i.e. crawling time etc, and we focus on the document itself.
We then compute 5 hash value for each record: md5 of content, md5 of parsed text, simhash of content, simhash of parsed text, simhash of metadata.
If the md5 hash of content or the md5 of parsed text are the same for two documents, we consider they are exact duplicate.
If at least of of the following three metrics, the simehash of content, simhash of parsed text or simhash of metadata, are the same for two documents. We consider they are near duplicates.



##Deprecated 
After you crawl the data, use the retrieveImgUrls.py script to read all the urls from the crawldb. Then download all these urls. Do some merging, like put all the images together in the same directory. Then run the duplicationWithUrlMapFile.py script.

```
python3 retrieveImgUrls.py <crawlDbDataFile> <outputImgUrlFile>
python3 downloadImageFile.py <outputImgUrlFile> <outputImageDir> <outputMapFileName> 

python3 duplicateWithUrlMapFile.py <ImageDir> <is_exact> <mapFile> <duplicateStatOutput> 

```

Dump the images file to wherever you like using the dumpImage.sh: 
```sh
$ bash dumpImage.sh segmentDir outputDir
```

Install distance, PIL for python script.
```
pip install PIL
(if PIL is not found for you, try pip install Pillow)
pip install distance
```
Then
```
python duplicate.py path [is_exact]
```
The argument path should be the outputDir created by the above sh script. It can read recursively.
The is_exact should be "true" or "false" to indicate whether we are detecting exact_duplicate or near_duplicate.



