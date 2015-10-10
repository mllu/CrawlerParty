import os
import sys
from uuid import uuid4
import nutchpy

__author__ = 'Taichi1'

if len(sys.argv) < 3:
    print('''Synopsis: %s segmentDir outputDir
    segmentDir: crawl/segments
    ''' % sys.argv[0])
    exit()
segmentDir = sys.argv[1]
dirs = os.listdir(segmentDir)
outputDir = sys.argv[2]
contentDir = os.path.join(outputDir, "content")
metadataDir = os.path.join(outputDir, "metadata")
textDir = os.path.join(outputDir, "text")

if not os.path.exists(outputDir):
    os.makedirs(outputDir)
if not os.path.exists(contentDir):
    os.makedirs(contentDir)
if not os.path.exists(metadataDir):
    os.makedirs(metadataDir)
if not os.path.exists(textDir):
    os.makedirs(textDir)

# urlDict = {}
filename = "url"
urlMap = {}
# This would print all the files and directories
for segment in dirs:
    if "DS_Store" in segment:
        continue
    parseTextFile = os.path.join(segmentDir, segment, "parse_text", "part-00000", "data")
    parseDataFile = os.path.join(segmentDir, segment, "parse_data", "part-00000", "data")

    contentFile = os.path.join(segmentDir, segment, "content", "part-00000", "data")

    # read parseText
    count = nutchpy.sequence_reader.count(parseTextFile)
    print(count)
    data = nutchpy.sequence_reader.read_iterator(parseTextFile)

    lineNumber = 0
    for list_item in data:
        lineNumber += 1
        # print(lineNumber)
        if lineNumber % 1000 == 0:
            print(lineNumber)
        # if lineNumber > 1:
        #     break
        # print(type(list_item))
        # # print(list_item)
        # print(str(list_item[0]).encode())
        #
        # print(type(list_item[1]))
        url = str(list_item[0])
        # print(url)
        print(str(list_item[0]).encode())
        urlFilename = urlMap.get(url, str(uuid4()))
        urlMap[url] = urlFilename

        urlFilePath = os.path.join(textDir, urlFilename)
        # print(urlFilePath)
        parseText = []
        for key, value in dict(list_item[1]).items():
            parseText.append(key.strip())
            parseText.append(value.strip())

        with open(urlFilePath, 'w') as f:
            f.write(url + "\n")
            f.write(" ".join(parseText))

            # newDict = urlDict.get(url, {"content": "", "metadata": "", "parseText": ""})
            # newDict["parseText"] = " ".join(parseText)
            # urlDict[url] = newDict

    # read metadata
    count = nutchpy.sequence_reader.count(parseDataFile)
    print(count)
    data = nutchpy.sequence_reader.read_iterator(parseDataFile)

    lineNumber = 0
    for list_item in data:
        lineNumber += 1
        if lineNumber % 1000 == 0:
            print(lineNumber)
        # if lineNumber > 1:
        #     break
        # print(type(list_item))
        # # print(list_item)
        print(str(list_item[0]).encode())
        #
        # print(type(list_item[1]))
        url = str(list_item[0])

        urlFilename = urlMap.get(url, str(uuid4()))
        urlMap[url] = urlFilename
        parseMetadata = []
        for key, value in dict(list_item[1]).items():
            if "Parse Metadata" in key:
                # parseMetadata.append(key.strip())
                # stripe the value of irrelevant values:
                items = value.split(" ")
                parseMetadata.append(value.strip())
            elif "Content Metadata" in key:
                print("ContentMetadata", value)
                # parseMetadata.append(key.strip())
                # parseMetadata.append(value.strip())
                items = value.split("=")
                metadataKeyValuePair = {}
                previousValue = ""
                nextKey = ""
                for item in items:
                    indexOfSpace = item.rfind(" ")
                    if indexOfSpace == -1:
                        if nextKey == "" and previousValue == "":
                            #         at the beginning:
                            nextKey = item
                            continue
                        else:
                            previousValue = item
                            metadataKeyValuePair[nextKey] = previousValue
                            continue
                    # either it is start or the end of the metadata
                    previousValue = item[:indexOfSpace]
                    metadataKeyValuePair[nextKey] = previousValue
                    nextKey = item[indexOfSpace + 1:]
                toDeleteKeys = []
                for metadatakey, metadatavalue in metadataKeyValuePair.items():
                    if "nutch" in metadatakey:
                        toDeleteKeys.append(metadatakey)
                        # metadataKeyValuePair.pop(metadatakey)
                    elif "Server" in metadatakey:
                        toDeleteKeys.append(metadatakey)
                        # metadataKeyValuePair.pop(metadatakey)
                    elif "Date" in metadatakey:
                        toDeleteKeys.append(metadatakey)
                        # metadataKeyValuePair.pop(metadatakey)
                    elif "expire" in metadatakey:
                        toDeleteKeys.append(metadatakey)
                        # metadataKeyValuePair.pop(metadatakey)
                for toDeleteKey in toDeleteKeys:
                    metadataKeyValuePair.pop(toDeleteKey)
                sortedTuple = sorted(metadataKeyValuePair.items())
                toAppendStringArray = []
                for tupleItem in sortedTuple:
                    stringElement = " ".join(tupleItem)
                    toAppendStringArray.append(stringElement)
                outputString = " ".join(toAppendStringArray)
                parseMetadata.append(outputString.strip())

        urlFilePath = os.path.join(metadataDir, urlFilename)

        with open(urlFilePath, 'w') as f:
            f.write(url + "\n")
            f.write(" ".join(parseMetadata))

    # read content

    count = nutchpy.sequence_reader.count(contentFile)
    print(count)
    data = nutchpy.sequence_reader.read_iterator(contentFile)

    lineNumber = 0
    for list_item in data:
        lineNumber += 1
        if lineNumber % 1000 == 0:
            print(lineNumber)
        print(str(list_item[0]).encode())
        # if lineNumber > 1:
        #     break
        # print(type(list_item))
        # # print(list_item)
        # print(str(list_item[0]).encode())
        #
        # print(type(list_item[1]))
        url = str(list_item[0])
        if url not in urlMap:
            continue

        urlFilename = urlMap.get(url, str(uuid4()))
        urlMap[url] = urlFilename
        urlFilePath = os.path.join(contentDir, urlFilename)
        content = []
        # what if it is a image file that is encoded in bytes?
        for key in list_item[1]:

            if key != "metadata":
                content.append(key.strip())

        with open(urlFilePath, 'w') as f:
            f.write(" ".join(content))
for url, uuid in urlMap.items():
    print(url)
    print(uuid)
    print()
