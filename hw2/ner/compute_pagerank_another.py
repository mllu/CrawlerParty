import json
import sys
import os
import networkx as nx
import re

__author__ = 'Taichi1'

if len(sys.argv) < 4:
    print "Synopsis: %s directory outputFileForPagerank propertyname" % sys.argv[0]
    sys.exit(0)


def get_state(string):
    if len(string) > 0:
        result = re.search(r', ([A-Z]{2}) \d', string)
        if result:
            return result.group(1)
    return ""


def get_day(string):
    if len(string) > 0:
        index = str(string).find("T")
        return str(string)[:index]
    return ""


def _page_rank(propertyDict, propertyName, jsonDict):
    print "Number of the propertyDict(Group)", len(propertyDict)
    with open(outputFile, "w") as output:
        for key in propertyDict:
            print "Length of the group", len(propertyDict[key])
            number = 0
            for i in range(0, len(propertyDict[key])):
                for j in range(i + 1, len(propertyDict[key])):
                    elementI = propertyDict[key][i]
                    elementJ = propertyDict[key][j]
                    number += 1
                    if number % 10000 == 0:
                        print(number)
                    if elementI['id'] == elementJ['id']:
                        continue
                    else:
                        # G.add_edge(elementI['id'], elementJ['id'])
                        output.write(elementI['id'] + " => " + elementJ['id']+"\n")
                        # print "Done add edges, calculating page rank"
                        # pageRank = nx.pagerank(G)
                        # print "Done calculating page rank"
                        # # print pageRank
                        # for jsonId in pageRank:
                        #     jsonDict[jsonId]["add"]["doc"]["pagerank_" + propertyName] = pageRank[jsonId]
                        # # output this json file, ready to post to solr
                        # outputJsonList = []
                        # for jsonId in jsonDict:
                        #     outputJsonList.append(jsonDict[jsonId])
                        # with open(outputFile, "w") as f:
                        #     f.write(json.dumps(outputJsonList, indent=4, separators=(',', ': ')))


# read in json file from a directory:
directory = sys.argv[1]
outputFile = sys.argv[2]
classifier = sys.argv[3]
dirs = os.listdir(directory)
jsonList = []
jsonDict = {}
for filename in dirs:
    if ".json" not in filename:
        continue
    filepath = os.path.join(directory, filename)
    with open(filepath) as f:
        jsonList += json.load(f)

for jsonElement in jsonList:
    # if json["add"]["doc"]["id"] in jsonDict:
    # print "Duplicates Found"
    # print jsonDict[json["add"]["doc"]["id"]]
    # print json
    jsonDict[jsonElement["add"]["doc"]["id"]] = jsonElement
print len(jsonList), len(jsonDict)

# no need to worry about deduplication for now. Solr will handle that when we index
# Not sure about the direction though. For now, just use the undirected graph. The implementation should be able to
# handle this by just writing both edges to the input file. This might not be very accurate as you can assume.

# G = nx.DiGraph()
# G = nx.Graph()
# # number = 0
# # for i in range(0, len(jsonList)):
# #     for j in range(i + 1, len(jsonList)):
# #         number += 1
# # print "All combinations: ", number
# print "Add Nodes"
# for i in range(0, len(jsonList)):
#     G.add_node(jsonList[i]["add"]["doc"]["id"])
# number = 0
# isBreak = False
# print "Done: Added Nodes"

if classifier == "location":
    locationDict = {}
    for i in range(0, len(jsonList)):
        jsonElement = jsonList[i]["add"]["doc"]
        if "location" not in jsonElement:
            continue
        statename = get_state(jsonElement["location"])
        locationList = locationDict.get(statename, [])
        locationList.append(jsonElement)
        locationDict[statename] = locationList
    _page_rank(locationDict, "location", jsonDict)
elif classifier == "time":
    timeDict = {}
    for i in range(0, len(jsonList)):
        jsonElement = jsonList[i]["add"]["doc"]
        # print jsonElement
        if "startTime" not in jsonElement:
            continue
        day = get_day(jsonElement["startTime"])
        timeList = timeDict.get(day, [])
        timeList.append(jsonElement)
        timeDict[day] = timeList
    _page_rank(timeDict, "startTime", jsonDict)

elif classifier == "gunCategory":
    gunTypeDict = {}
    for i in range(0, len(jsonList)):
        jsonElement = jsonList[i]["add"]["doc"]
        if "gunCategory" not in jsonElement:
            continue
        gunType = jsonElement["gunCategory"]
        gunTypeList = gunTypeDict.get(gunType, [])
        gunTypeList.append(jsonElement)
        gunTypeDict[gunType] = gunTypeList
    _page_rank(gunTypeDict, "gunCategory", jsonDict)
# for i in range(0, len(jsonList)):
#     for j in range(i + 1, len(jsonList)):
#         number += 1
#         if number % 10000 == 0:
#             print number
#             # isBreak = True
#             # break
#         jsonI = jsonList[i]["add"]["doc"]
#         jsonJ = jsonList[j]["add"]["doc"]
#         # assign different weight to the edges if they share the same property in different ways
#         similarity = 0
#         if jsonI['gunCategory'] == jsonJ['gunCategory']:
#             similarity += 3
#         if get_state(jsonI["location"]) == get_state(jsonJ['location']):
#             similarity += 5
#         # print jsonI, jsonJ
#         if "startTime" in jsonI and "startTime" in jsonJ and get_day(jsonI['startTime']) == get_day(jsonJ['startTime']):
#             similarity += 1
#         if jsonI['seller'] == jsonJ['seller'] and "A+" not in jsonI['seller']:
#             similarity += 0.5
#         if jsonI['price'] != 0.00 and jsonJ['price'] != 0.00 and abs(jsonI['price'] - jsonJ['price']) < 20:
#             similarity += 0.3
#         if similarity > 0:
#             # edgeList = [(jsonI['id'], jsonJ['id'], similarity), (jsonJ['id'], jsonI['id'], similarity)]
#             edgeList = [(jsonI['id'], jsonJ['id'], similarity)]
#             if number % 10000 == 0:
#                 print edgeList
#             G.add_weighted_edges_from(edgeList)
#
#     if isBreak:
#         break
# # print G
# # add the page rank to the document
# pageRank = nx.pagerank(G)
# # print pageRank
# for jsonId in pageRank:
#     jsonDict[jsonId]["add"]["doc"]["pagerank"] = pageRank[jsonId]
#     jsonDict[jsonId]["add"]["boost"] = pageRank[jsonId]
# # output this json file, ready to post to solr
# outputJsonList = []
# for jsonId in jsonDict:
#     outputJsonList.append(jsonDict[jsonId])
# with open(outputFile, "w") as f:
#     f.write(json.dumps(outputJsonList, indent=4, separators=(',', ': ')))
