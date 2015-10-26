import json
import sys
import os
import networkx as nx
import re

__author__ = 'Taichi1'

if len(sys.argv) < 3:
    print "Synopsis: %s directory outputJson" % sys.argv[0]


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


# read in json file from a directory:
directory = sys.argv[1]
outputFile = sys.argv[2]
dirs = os.listdir(directory)
jsonList = []
jsonDict = {}
for filename in dirs:
    if ".json" not in filename:
        continue
    filepath = os.path.join(directory, filename)
    with open(filepath) as f:
        jsonList += json.load(f)

for json in jsonList:
    if json["add"]["doc"]["id"] in jsonDict:
        print "Duplicates Found"
        print jsonDict[json["add"]["doc"]["id"]]
        print json
    jsonDict[json["add"]["doc"]["id"]] = json
print len(jsonList), len(jsonDict)

# no need to worry about deduplication for now. Solr will handle that when we index
# Not sure about the direction though. For now, just use the undirected graph. The implementation should be able to
# handle this by just writing both edges to the input file. This might not be very accurate as you can assume.

G = nx.DiGraph()
for i in range(0, len(jsonList)):
    for j in range(i + 1, len(jsonList)):
        jsonI = jsonList[i]["add"]["doc"]
        jsonJ = jsonList[j]["add"]["doc"]
        # assign different weight to the edges if they share the same property in different ways
        similarity = 0
        if jsonI['gunCategory'] == jsonJ['gunCategory']:
            similarity += 3
        if get_state(jsonI["location"]) == get_state(jsonJ['location']):
            similarity += 5
        if get_day(jsonI['startTime']) == get_day(jsonJ['startTime']):
            similarity += 1
        if jsonI['seller'] == jsonJ['seller'] and "A+" not in jsonI['seller']:
            similarity += 0.5
        if jsonI['price'] != 0.00 and jsonJ['price'] != 0.00 and abs(jsonI['price'] - jsonJ['price']) < 20:
            similarity += 0.3
        edgeList = [(jsonI['id'], jsonJ['id'], similarity), (jsonJ['id'], jsonI['id'], similarity)]
        G.add_weighted_edges_from(edgeList)

# add the page rank to the document
pageRank = nx.pagerank(G)
for jsonId in pageRank:
    jsonDict[jsonId]["add"]["boost"] = pageRank[jsonId] * 1000
# output this json file, ready to post to solr
with open(outputFile, "w") as f:
    f.write(json.dump(jsonDict))
