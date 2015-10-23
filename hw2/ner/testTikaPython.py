from tika import parser

import ner
import nltk


def get_states():
    statesMap = {}
    with open("states_abbreviation.txt") as f:
        for line in f:
            abbreviationTuple = line.split("\t")
            # print line
            statesMap[abbreviationTuple[1].strip()] = abbreviationTuple[0].strip()
    return statesMap


statesMap = get_states()
outputXml = "documents.xml"
fOutput = open(outputXml, "w")
fOutput.write("<add>\n")


# for each input file, do something like the following
parsed = parser.from_file('../test2.html')
# print parsed["metadata"]["Description"]
fOutput.write("\t<doc>\n")
print parsed["metadata"]["title"]

if "title" in parsed["metadata"]:
    modelCategoryTuple = str(parsed["metadata"]["title"]).split(":")
    modelname = str(modelCategoryTuple[0]).strip()
    category = str(modelCategoryTuple[1].strip())
    fOutput.write('\t\t<field name="id">%s</field>\n' % modelname)
    fOutput.write('\t\t<field name="title">%s</field>\n' % ":".join(modelCategoryTuple))
    fOutput.write('\t\t<field name="gunModel">%s</field>\n' % modelname)
    fOutput.write('\t\t<field name="gunCategory">%s</field>\n' % category)
# print parsed["content"]
# print parsed.keys()
# print parsed["metadata"]

tagger = ner.SocketNER(host='localhost', port=9191, output_format='slashTags')
tagged = tagger.get_entities(parsed["content"])

print(tagged["LOCATION"])
statesSet = set(statesMap.keys())
statesFrequency = {}
if len(tagged["LOCATION"]) > 0:
    for location in tagged["LOCATION"]:
        # print(statesSet)
        if str(location) in statesSet:
            print location

            fq = statesFrequency.get(location, 0)
            fq += 1
            statesFrequency[location] = fq
    sortedDict = sorted(statesFrequency.items(), key=lambda item: item[1], reverse=True)
    # print(sortedDict)
    if len(sortedDict) > 0:
        mostFrequentState = sortedDict[0][0]
        fOutput.write('\t\t<field name="%s">%s</field>\n' % ("location", mostFrequentState))
fOutput.write("\t</doc>\n")



# print(tagged.keys())
# {'LOCATION': ['California', 'United States'],
# 'ORGANIZATION': ['University of California']}
# print(tagger.json_entities("Alice went to the Museum of Natural History."))
# '{"ORGANIZATION": ["Museum of Natural History"], "PERSON": ["Alice"]}
