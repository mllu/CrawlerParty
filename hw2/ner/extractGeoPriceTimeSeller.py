import re
from tika import parser

import ner
import json
import nltk


def parse_time(time_tuple_list):
    hour = int(time_tuple_list[3])
    if time_tuple_list[6] == "PM":
        hour = int(time_tuple_list[3]) + 12
    return "%s-%s-%sT%d:%s:%sZ" % (
        time_tuple_list[2], time_tuple_list[0], time_tuple_list[1], hour, time_tuple_list[4], time_tuple_list[5])


def get_seller(htmlfilename):
    from bs4 import BeautifulSoup

    with open(htmlfilename) as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    elementList = soup.find_all("a", id='SellerName')

    def match_rating(tag):
        return tag.name == "a" and "href" in tag.attrs and re.match(
            "http://www.gunbroker.com/Auction/ViewUserFeedback.aspx", tag["href"])

    ratingList = soup.find_all(match_rating)
    rtn = []

    if len(elementList) > 0:
        rtn.append(elementList[0].getText().strip())
    if len(ratingList) > 0:
        rtn.append(ratingList[0].getText().strip())
    return rtn


def parse_currency(currency_string):
    from re import sub
    from decimal import Decimal

    money = currency_string
    value = Decimal(sub(r'[^\d.]', '', money))
    return float(value)


def get_money_value(moneyList):
    moneyFreqDict = {}
    for moneyTuple in moneyList:
        if type(moneyTuple) == tuple:
            if len(moneyTuple[0]) == 0 or len(moneyTuple[1]) == 0:
                continue
            # print(moneyTuple)
            value = parse_currency(moneyTuple[0] + moneyTuple[1])
            freq = moneyFreqDict.get(value, 0)
            freq += 1
            moneyFreqDict[value] = freq
    sortedMoney = sorted(moneyFreqDict.items(), key=lambda item: item[1], reverse=True)
    return sortedMoney[0][0]


def get_states():
    statesMap = {}
    with open("states_abbreviation.txt") as f:
        for line in f:
            abbreviationTuple = line.split("\t")
            # print line
            statesMap[abbreviationTuple[1].strip()] = abbreviationTuple[0].strip()
    return statesMap


statesMap = get_states()
outputJson = "documents.json"
fOutput = open(outputJson, "w")
gunInfoList = []
# fOutput.write("<add>\n")


# for each input file, do something like the following
htmlFileName = './test2.html'
parsed = parser.from_file(htmlFileName)
gunInfoDict = {}
# print parsed["metadata"]["Description"]
# fOutput.write("\t<doc>\n")
# print parsed["content"].encode("utf-8")
# print parsed["metadata"]["title"]


if "title" in parsed["metadata"]:
    modelCategoryTuple = str(parsed["metadata"]["title"]).split(":")
    modelname = str(modelCategoryTuple[0]).strip()
    category = str(modelCategoryTuple[1].strip())
    gunInfoDict["id"] = modelname
    gunInfoDict['title'] = ":".join(modelCategoryTuple)
    gunInfoDict['gunModel'] = modelname
    gunInfoDict['gunCategory'] = re.sub(" at GunBroker.com", "", category)
# print parsed["content"]
# print parsed.keys()
# print parsed["metadata"]

tagger = ner.SocketNER(host='localhost', port=9191, output_format='slashTags')
tagged = tagger.get_entities(parsed["content"])

# print(tagged["LOCATION"])
# print(tagged["ORGANIZATION"])
statesSet = set(statesMap.keys())
statesFrequency = {}
if len(tagged["LOCATION"]) > 0:
    for location in tagged["LOCATION"]:
        # print(statesSet)
        if str(location) in statesSet:
            # print location

            fq = statesFrequency.get(location, 0)
            fq += 1
            statesFrequency[location] = fq
    sortedDict = sorted(statesFrequency.items(), key=lambda item: item[1], reverse=True)
    # print(sortedDict)
    if len(sortedDict) > 0:
        mostFrequentState = sortedDict[0][0]
        gunInfoDict['location'] = mostFrequentState


# get the price, doesn't work very well. for now just use the regular expression

# tagger = ner.SocketNER(host='localhost', port=9192, output_format='slashTags')
# # print parsed["content"].encode("utf-8").find("$")
# tagged = tagger.get_entities(parsed["content"].encode("utf-8").strip())
# # tagged = tagger.get_entities("   $2,450.00  \n")
#
# print(tagged.keys())
# if "MONEY" in tagged and len(tagged["MONEY"]) > 0:
#     money = []
#     for moneyString in tagged['MONEY']:
#         if str(moneyString).startswith("$"):
#             print(moneyString)
#             money.append(float(str(moneyString[1:]).strip()))
#         else:
#             money.append(moneyString)
#     print money
#     gunInfoDict['price'] = money


money = re.compile('|'.join([
    # r'\$[0-9\,]*(\.\d{1,2})?',         # e.g., $5.
    r"(\$[0-9\,]*)(\.[0-9]{1,2})?"
]))
#     r'\$[0-9][0-9\,]*(\.\d{1,2})?|\$[\.]([\d][\d]?)'

moneyList = money.findall(parsed["content"])

gunInfoDict['price'] = get_money_value(moneyList)
# print(gunInfoDict['price'])


# get the time. Should use the SUTime module from stanford. Works well on other computer, for some reason not on mine.
# For now just use the regular expression to match the time

timePattern = re.compile(r'(\d{2})/(\d{2})/(\d{4}) (\d{1,2}):(\d{2}):(\d{2}) ([A|P]M)')
timeList = timePattern.findall(parsed["content"])

if len(timeList) == 2:
    gunInfoDict['startTime'] = parse_time(timeList[0])
    gunInfoDict['endTime'] = parse_time(timeList[1])
    gunInfoDict['timeRange'] = "[%s TO %s]" % (gunInfoDict['startTime'], gunInfoDict['endTime'])


# get seller name. for now, that's all we can get
seller = get_seller(htmlFileName)
if len(seller) > 0:
    gunInfoDict['seller'] = seller[0]
    if len(seller) > 1:
        gunInfoDict['sellerRating'] = seller[1]
gunInfoList.append({"add": {"doc": gunInfoDict}})

# if boosting
# gunInfoList.append({"add": {"doc": gunInfoDict, "overwrite": False, "boost": 3.45, }})

print json.dumps(gunInfoList, indent=4, separators=(',', ': '))
