import re
import os
import sys
from uuid import uuid4
from tika import parser
from bs4 import BeautifulSoup
import ner
import json
import nltk


def list_path_and_add_file(toAddlist, path):
    if os.path.isdir(path) and ".idea" not in path:
        for childpath in os.listdir(path):
            list_path_and_add_file(toAddlist, os.path.join(path, childpath))
    elif not os.path.isdir(path):
        if "DS_Store" not in path:
            toAddlist.append(path)


def get_location(soup):
    # print soup.find_all("td", id="Location")
    elementList = soup.find_all(id='Location')
    # print(elementList)
    if len(elementList) > 0:
        return elementList[0].b.getText().strip()
    return ""


def parse_time(time_tuple_list):
    hour = int(time_tuple_list[3])
    if time_tuple_list[6] == "PM":
        hour = int(time_tuple_list[3]) + 12
    return "%s-%02d-%02dT%d:%s:%sZ" % (
        time_tuple_list[2], int(time_tuple_list[0]), int(time_tuple_list[1]), hour, time_tuple_list[4],
        time_tuple_list[5])


def get_seller(soup):
    seller = soup.find(id='SellerName')
    # print seller
    if seller:
        # print seller.getText().strip()
        return seller.getText().strip()
    return ""


def get_seller_rating(soup):
    def match_rating(tag):
        return tag.name == "a" and "href" in tag.attrs and re.match(
            "http://www.gunbroker.com/Auction/ViewUserFeedback.aspx|ViewUserFeedback", tag["href"])

    rating = soup.find(match_rating)

    if rating:
        # print rating.getText().strip()
        return rating.getText().strip()
    return ""


def get_bidder(soup):
    element = soup.find(id="ctl00_ctlPagePlaceHolder_spNonParticipantHighBidder2")

    # print element.getText().strip().split([" ", "\t", "\n"])
    if element:
        string_list = re.split(r" |\t|\n|\r", element.getText().strip())
        string_list = filter(None, string_list)
        return " ".join(string_list)
    return ""


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

gunInfoList = []
# fOutput.write("<add>\n")

if len(sys.argv) < 2:
    print "Synopsis: python2 %s inputDir outputJson" % sys.argv[0]
    sys.exit(0)
directory = sys.argv[1]

outputJson = "output.json"
if len(sys.argv) > 2:
    outputJson = sys.argv[2]
htmlPathList = []
list_path_and_add_file(htmlPathList, directory)
print "Number of htmls", len(htmlPathList)

# tagger = ner.SocketNER(host='localhost', port=9191, output_format='slashTags')
count = 0
for htmlFileName in htmlPathList:
    count += 1
    if count % 1000 == 0:
        print(count)
    # for each input file, do something like the following
    # htmlFileName = './a'
    try:
        parsed = parser.from_file(htmlFileName)
    except Exception as e:
        print htmlFileName
        print e
        continue
    # if it is not a item page, continue
    if ":" not in parsed["metadata"]["title"]:
        continue

    gunInfoDict = {}
    # print parsed["metadata"]["Description"]
    # fOutput.write("\t<doc>\n")
    # print parsed["content"].encode("utf-8")
    # print parsed["metadata"]["title"]

    if "title" in parsed["metadata"]:
        modelCategoryTuple = str(parsed["metadata"]["title"].encode("utf-8")).split(":")
        modelname = str(modelCategoryTuple[0]).strip()
        category = str(modelCategoryTuple[1].strip())
        gunInfoDict["id"] = str(uuid4())
        gunInfoDict['title'] = ":".join(modelCategoryTuple)
        gunInfoDict['gunModel'] = modelname
        gunInfoDict['gunCategory'] = re.sub(" at GunBroker.com", "", category)
    # print parsed["content"]
    # print parsed.keys()
    # print parsed["metadata"]

    # print location
    # tagged = tagger.get_entities(parsed["content"])
    # statesSet = set(statesMap.keys())
    # statesFrequency = {}
    # if "LOCATION" in tagged and len(tagged["LOCATION"]) > 0:
    #     print(tagged["LOCATION"])
    #     for location in tagged["LOCATION"]:
    #         # print(statesSet)
    #         if str(location) in statesSet:
    #             # print location
    #
    #             fq = statesFrequency.get(location, 0)
    #             fq += 1
    #             statesFrequency[location] = fq
    #     sortedDict = sorted(statesFrequency.items(), key=lambda item: item[1], reverse=True)
    #     # print(sortedDict)
    #     if len(sortedDict) > 0:
    #         mostFrequentState = sortedDict[0][0]
    #         gunInfoDict['location'] = mostFrequentState

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
    # get the time. Should use the SUTime module from stanford. Works well on other computer, for some reason not
    # on mine.
    # For now just use the regular expression to match the time

    timePattern = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2}):(\d{1,2}):(\d{1,2}) ([A|P]M)')
    timeList = timePattern.findall(parsed["content"])

    if len(timeList) == 2:
        gunInfoDict['startTime'] = parse_time(timeList[0])
        gunInfoDict['endTime'] = parse_time(timeList[1])
        # gunInfoDict['timeRange'] = "[%s TO %s]" % (gunInfoDict['startTime'], gunInfoDict['endTime'])

    # get seller name. for now, that's all we can get
    with open(htmlFileName) as f:
        htmlText = f.read()
        soup = BeautifulSoup(htmlText, "html.parser")
        seller = get_seller(soup)
        if len(seller) > 0:
            gunInfoDict['seller'] = seller
        sellerRating = get_seller_rating(soup)
        if len(sellerRating) > 0:
            gunInfoDict['sellerRating'] = sellerRating
        location = get_location(soup)
        if len(location) > 0:
            gunInfoDict['location'] = location
        bidder = get_bidder(soup)
        if len(bidder) > 0:
            gunInfoDict['bidder'] = bidder

    gunInfoList.append({"add": {"doc": gunInfoDict}})
# print json.dumps(gunInfoList, indent=4, separators=(',', ': '))
print "Length of GunInfo", len(gunInfoList)
fOutput = open(outputJson, "w")
with open(outputJson, "w") as output:
    output.write(json.dumps(gunInfoList, indent=4, separators=(',', ': ')))
# print json.dumps({"add": {"doc": gunInfoDict}}, indent=4, separators=(',', ': '))
# print ","
# if boosting
# gunInfoList.append({"add": {"doc": gunInfoDict, "overwrite": False, "boost": 3.45, }})

# print json.dumps(gunInfoList, indent=4, separators=(',', ': '))
