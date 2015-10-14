#Workflow

## Exact Duplicate
Run the detectExactDuplicate.py script. 
```
python3 detectExactDuplicate.py <segmentDirectory>
```

## Near Duplicate

Becasuse nutch dump will not preserve the url information for us, we have to manually download the images. Improvement required.

* Retrieve image urls from the crawlDb
```
python3 retrieveImgUrls.py <crawlDbDataFile> <outputImgUrlFile>
```
* Download all the images and create the url-uuid map
```
python3 downloadImageFile.py <urlFile> <outputImageDir> <outputMapFileName>
```
* Detect near duplicate
```
python3 detectNearDuplicateWithMap.py <imageDirectory> <mapFile> <duplicateStatOutput>
```

