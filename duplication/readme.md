#Workflow:
After you crawl the data, use the retrieveImgUrls.py script to read all the urls from the crawldb. Then download all these urls. Do some merging, like put all the images together in the same directory. Then run the duplicationWithUrlMapFile.py script.

```
python3 retrieveImgUrls.py <crawlDbDataFile> <outputImgUrlFile>
python3 downloadImageFile.py <outputImgUrlFile> <outputImageDir> <outputMapFileName> 

python3 duplicateWithUrlMapFile.py <ImageDir> <is_exact> <mapFile> <duplicateStatOutput> 

```

##Deprecate
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



