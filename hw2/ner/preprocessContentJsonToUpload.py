import json
import sys


def generate_new_content_json(jsonfilename, outputFile):
    with open(jsonfilename) as f:
        jsonList = json.load(f)
    outputJsonList = []
    for jsonElement in jsonList:
        newDict = {}
        for jsonId in jsonElement:
            newDict["id"] = jsonId
            newDict['content'] = jsonElement[jsonId]
        outputJsonList.append(newDict)
    with open(outputFile, "w") as f:
        f.write(json.dumps(outputJsonList, indent=4, separators=(',', ': ')))


inputFile = sys.argv[1]
outputFile = sys.argv[2]
generate_new_content_json(inputFile, outputFile)
