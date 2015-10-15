from uuid import uuid4
import nutchpy
import sys
from collections import OrderedDict
import os

if len(sys.argv) < 2:
    sys.stderr.write(
        """SYNOPSIS: python3 %s <segmentDirectory> <outputDigestFile>\n""" % sys.argv[0])
    sys.exit(1)
segmentDir = sys.argv[1]
digestOutputFile = sys.argv[2]
dirs = os.listdir(segmentDir)
urlMap = {}
# digestDict = {}
digestDict = OrderedDict()
print("number of segments", len(dirs))
segmentNumber = 0
for eachSegment in dirs:
    if "DS_Store" in eachSegment:
        continue
    segmentNumber += 1
    print()
    print("segment ", segmentNumber)
    try:
        parseDataFile = os.path.join(segmentDir, eachSegment, "parse_data", "part-00000", "data")
        # read metadata
        print(os.path.join(segmentDir, eachSegment))
        count = nutchpy.sequence_reader.count(parseDataFile)
        print(count)
        data = nutchpy.sequence_reader.read_iterator(parseDataFile)
    except:
        continue

    lineNumber = 0
    for list_item in data:
        lineNumber += 1
        if lineNumber % 1000 == 0:
            print(lineNumber)
        # if lineNumber > 1:
        #     break
        # print(type(list_item))
        # # print(list_item)
        # print(str(list_item[0]).encode())
        #
        # print(type(list_item[1]))
        url = list_item[0].toString()

        # urlFilename = urlMap.get(url, str(uuid4()))
        parseMetadata = []
        for key, value in dict(list_item[1]).items():
            if "Content Metadata" in key:
                # print("ContentMetadata", value)
                # print(type(value))
                startIndexOfNutchDigest = str(value).index("nutch.content.digest=")
                endOfNutchDigest = str(value)[startIndexOfNutchDigest:].index(" ")
                digestValue = str(value)[startIndexOfNutchDigest:startIndexOfNutchDigest + endOfNutchDigest]
                # print(digestValue)
                if digestValue not in digestDict:
                    newSet = set()
                    newSet.add(url)
                    digestDict[digestValue] = newSet
                else:
                    print("Exact Duplicate")

                    digestDict[digestValue].add(url)
                    print(digestDict[digestValue])

digestOutput = open(digestOutputFile, "w")
numberOfDuplicates = 0
print("Print out Images")
for digestValue in digestDict:
    if len(digestDict[digestValue]) > 1:
        print(digestDict[digestValue])
        numberOfDuplicates += len(digestDict[digestValue]) - 1
        print()
for key in digestDict:
    digestOutput.write("%s %s\n%s" % (key, len(digestDict[key]), digestDict[key]))
    digestOutput.write("\n")
print()
print("Number Of Exact Duplicates", numberOfDuplicates)
