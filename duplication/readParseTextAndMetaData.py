import os
import sys
import nutchpy

__author__ = 'Taichi1'

if len(sys.argv) < 3:
    print('''Synopsis: %s segmentDir outputDir
    segmentDir: crawl/segments
    ''' % sys.argv[0])
segmentDir = sys.argv[1]
outputDir = sys.argv[2]
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
dirs = os.listdir(segmentDir)

urlDict = {}
filename = "url"
urlMap = {}
# This would print all the files and directories
for segment in dirs:
    parseTextFile = os.path.join(segmentDir, segment, "parse_text", "part-00000", "data")
    parseDataFile = os.path.join(segmentDir, segment, "parse_data", "part-00000", "data")

    contentFile = os.path.join(segmentDir, segment, "content", "part-00000", "data")

    # read parseText
    count = nutchpy.sequence_reader.count(parseTextFile)
    print(count)
    data = nutchpy.sequence_reader.read_iterator(parseTextFile)

    lineNumber = 0
    for list_item in data:
        if lineNumber % 1000 == 0:
            print(lineNumber)
        # if lineNumber > 1:
        #     break
        # print(type(list_item))
        # # print(list_item)
        # print(str(list_item[0]).encode())
        #
        # print(type(list_item[1]))
        url = str(list_item[0]).encode()
        parseText = []
        for key, value in dict(list_item[1]).items():
            parseText.append(key.strip())
            parseText.append(value.strip())

        lineNumber += 1
        newDict = urlDict.get(url, {"content": "", "metadata": "", "parseText": ""})
        newDict["parseText"] = " ".join(parseText)
        urlDict[url] = newDict

    # read metadata
    count = nutchpy.sequence_reader.count(parseDataFile)
    print(count)
    data = nutchpy.sequence_reader.read_iterator(parseDataFile)

    lineNumber = 0
    for list_item in data:
        if lineNumber % 1000 == 0:
            print(lineNumber)
        # if lineNumber > 1:
        #     break
        # print(type(list_item))
        # # print(list_item)
        # print(str(list_item[0]).encode())
        #
        # print(type(list_item[1]))
        url = str(list_item[0]).encode()
        parseMetadata = []
        for key, value in dict(list_item[1]).items():
            if "Parse Metadata" in key:
                parseMetadata.append(key.strip())
                parseMetadata.append(value.strip())
            elif "Content Metadata" in key:
                parseMetadata.append(key.strip())
                parseMetadata.append(value.strip())
            elif "Title" in key:
                parseMetadata.append(key.strip())
                parseMetadata.append(value.strip())

        lineNumber += 1
        newDict = urlDict.get(url, {"content": "", "metadata": "", "parseText": ""})
        newDict["metadata"] = " ".join(parseMetadata)
        urlDict[url] = newDict

    # read content

    count = nutchpy.sequence_reader.count(contentFile)
    print(count)
    data = nutchpy.sequence_reader.read_iterator(contentFile)

    lineNumber = 0
    for list_item in data:

        if lineNumber % 1000 == 0:
            print(lineNumber)
        # if lineNumber > 1:
        #     break
        # print(type(list_item))
        # # print(list_item)
        # print(str(list_item[0]).encode())
        #
        # print(type(list_item[1]))
        url = str(list_item[0]).encode()
        if url not in urlDict:
            continue
        content = []
        for key in list_item[1]:

            if key != "metadata":
                # for html, key and value are the same, so we just add the keys.
                content.append(key.strip())
                # print("keys")
                # print(key)
                # print(type(key))
                # print("values")
                # print(list_item[1][key])

        lineNumber += 1
        newDict = urlDict.get(url, {"content": "", "metadata": "", "parseText": ""})
        newDict["content"] = " ".join(content)
        urlDict[url] = newDict
        # print("item1", list_item[1])


        # break
for url, valueDict in urlDict.items():
    print(url)
    print(valueDict["content"])
    print(valueDict["metadata"])
    print(valueDict['parseText'])
    print()
