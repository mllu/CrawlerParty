

import sys
# import os
import re
import requests
from lxml import etree
from dateutil import parser
import datetime

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

from Queue import PriorityQueue
class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item


if len(sys.argv) < 2:
    print "Synopsis: %s queryWord" % sys.argv[0]
    sys.exit(0)

now = datetime.datetime.now()
# print "Current month: %d" % now.month
monthinteger = now.month

base = "http://localhost:8983/solr/techproducts/select?"
query = sys.argv[1]
searchFields = "title+seller+sellerRating+bidder+gunModel+location+startTime+endTime+pagerank_gunCategory+pagerank_location+pagerank_temporal"
filterQuery = "startTime:[* TO NOW]"
url = base + "q=" + query + "&fq=" + filterQuery + "&fl=" + searchFields
print "URL: " + url
page = requests.get(url)
xml = page.content
# print xml
root = etree.fromstring(xml)
numFound = int(root.xpath('//result/@numFound')[0])
print "{0} results found" .format(str(numFound))

list_ads_time = []
list_ads_spatial_temporal = []
list_bidder_time = []
list_bad_bidder_spatial_temporal = []
list_nr_seller_temporal = []
dict_seller_rating = {}


debug = 0

# classified in month
for i in range(1, 7):
    month = datetime.date(now.year, monthinteger - i, now.day).strftime('%B')

    filterQuery = "startTime:[NOW-{0}MONTHS TO NOW-{1}MONTHS]" .format(i, i-1)
    # print filterQuery
    url = base + "q=" + query + "&fq=" + filterQuery + "&fl=" + searchFields
    # print "URL: " + url
    page = requests.get(url)
    xml = page.content
    # print xml
    root = etree.fromstring(xml)
    numFound = int(root.xpath('//result/@numFound')[0])
    # print "ads in {0}: {1}" .format(month, str(numFound))
    list_ads_time.append(numFound)

    if debug == 1:
        numFound = 2220

    dict_ads_geo = {}
    dict_bidder_geo = {}
    dict_bad_bidder_geo = {}
    cnt_bidder = 0
    cnt_nr_bidder = 0
    cnt_nr_seller = 0


    for cnt in range(0, numFound/10+1):
        start = cnt*10
        # print start
        url = base + "q=" + query + "&fq=" + filterQuery + "&fl=" + searchFields + "&rows=10" + "&start=" + str(start)
        # print url

        page = requests.get(url)
        xml = page.content
        root = etree.fromstring(xml)
        doc = root.xpath('//doc')

        for d in doc:
            title = d.xpath('./arr[@name="title"]/str/text()')
            # print "title: " + title[0]
            startTime = d.xpath('./date[@name="startTime"]/text()')
            # print "startTime: " + startTime[0]
            dt = parser.parse(startTime[0])
            # print str(dt.year) + "/" +str(dt.month) + "/" + str(dt.day)
            location = d.xpath('./str[@name="location"]/text()')
            # print location
            loc = re.split(', ',location[0])
            loc = loc[1].split(' ')[0]
            # print "location: " + loc
            if loc in dict_ads_geo:
                cnt = dict_ads_geo[loc]
                dict_ads_geo[loc] = cnt + 1
            else:
                dict_ads_geo[loc] = 1


            # NR seller = underage
            seller = d.xpath('./str[@name="sellerRating"]/text()')
            text = str(seller[0])
            # initialize regEx with the pattern like "(content)"
            regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
            m = regEx.match(text)
            while m:
              text = m.group(1) + m.group(2)
              m = regEx.match(text)
            # print text
            if text in dict_seller_rating:
                dict_seller_rating[text]+=1
            else:
                dict_seller_rating[text] = 1

            if "NR" in str(seller[0]):
                cnt_nr_seller = cnt_nr_seller + 1


            bidder = d.xpath('./str[@name="bidder"]/text()')
            if bidder:
                cnt_bidder = cnt_bidder+1
                bidderInfo = bidder[0].replace(u'\xa0', u' ')
                # print "bidder: " + bidderInfo

                if loc in dict_bidder_geo:
                    cnt = dict_bidder_geo[loc]
                    dict_bidder_geo[loc] = cnt + 1
                else:
                    dict_bidder_geo[loc] = 1
                # print "Num of bidders in {0} are {1}." .format(loc, str(dict_bidder_geo[loc]))
                # print "\n"

                if "NR" in bidderInfo:
                    # print "bad_bidder: " + bidderInfo

                    cnt_nr_bidder += 1
                    if loc in dict_bad_bidder_geo:
                        dict_bad_bidder_geo[loc] += 1
                    else:
                        dict_bad_bidder_geo[loc] = 1


    list_ads_spatial_temporal.append(dict_ads_geo)
    list_bad_bidder_spatial_temporal.append(dict_bad_bidder_geo)

    # print "buyer in {0}: {1}" .format(month, str(cnt_bidder))
    list_bidder_time.append(cnt_bidder)
    # print "underage/non-verified seller in {0}: {1}\n" .format(month, str(cnt_nr_seller))
    list_nr_seller_temporal.append(cnt_nr_seller)


'''
# print different type of seller rating
for key, value in dict_seller_rating.iteritems():
    print key
'''

# amount of weapons sold in different month
with open("Ads_Spatial_Temporal.txt", "w") as f:
    for idx, dict_geo in enumerate(list_ads_spatial_temporal, start = 1):
        queue = MyPriorityQueue()
        month = datetime.date(now.year, monthinteger - idx, now.day).strftime('%B')
        spatial_temporal_stat = month + "\t" + str(dict_geo)

        # print "\n" + month
        # print("loc\tFrequency")
        for key, value in dict_geo.iteritems():
            geo_stat = key + "\t" + str(value)
            queue.put(key, -1*value)
            # print geo_stat

        f.write("\n"+month+"\n")
        f.write("Location\tFrequency\n")

        while not queue.empty():
            key = queue.get()
            geo_temp_stat = key + "\t" + str(dict_geo[key])
            # print geo_temp_stat
            f.write(geo_temp_stat + "\n")

# amount of weapons sold in different month
with open("Bad_Buyer_Spatial_Temporal.txt", "w") as f:
    for idx, dict_geo_temporal in enumerate(list_bad_bidder_spatial_temporal, start = 1):
        queue = MyPriorityQueue()
        month = datetime.date(now.year, monthinteger - idx, now.day).strftime('%B')
        spatial_temporal_stat = month + "\t" + str(dict_geo_temporal)

        # print "\n" + month
        # print("loc\tFrequency")
        for key, value in dict_geo_temporal.iteritems():
            geo_temporal_stat = key + "\t" + str(value)
            queue.put(key, -1*value)
            # print geo_temporal_stat

        f.write("\n"+month+"\n")
        f.write("Location\tFrequency\n")

        while not queue.empty():
            key = queue.get()
            geo_temp_stat = key + "\t" + str(dict_geo_temporal[key])
            # print geo_temp_stat
            f.write(geo_temp_stat + "\n")

with open("Buyer_Temporal.txt", "w") as f:
    # print("Month\tFrequency")
    f.write("Month\tFrequency\n")
    for idx, value in enumerate(list_bidder_time, start = 1):
        month = datetime.date(now.year, monthinteger - idx, now.day).strftime('%B')
        stat = month + "\t" + str(value)
        # print stat
        f.write(stat+"\n")

with open("Ads_Temporal.txt", "w") as f:
    # print("Month\tFrequency")
    f.write("Month\tFrequency\n")
    for idx, value in enumerate(list_ads_time, start = 1):
        month = datetime.date(now.year, monthinteger - idx, now.day).strftime('%B')
        stat = month + "\t" + str(value)
        # print stat
        f.write(stat+"\n")

with open("Bad_Seller_Temporal.txt", "w") as f:
    # print("Month\tFrequency")
    f.write("Month\tFrequency\n")
    for idx, value in enumerate(list_nr_seller_temporal, start = 1):
        month = datetime.date(now.year, monthinteger - idx, now.day).strftime('%B')
        stat = month + "\t" + str(value)
        # print stat
        f.write(stat+"\n")
