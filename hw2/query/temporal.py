
import requests
from lxml import etree
from dateutil import parser
import re
import datetime

now = datetime.datetime.now()
print "Current month: %d" % now.month
monthinteger = now.month

base = "http://localhost:8983/solr/techproducts/select?"
query = "*"
searchFields = "title+seller+sellerRating+bidder+gunModel+location+startTime+endTime+pagerank_gunCategory+pagerank_location+pagerank_temporal"

dict_ads_time = []
dict_bidder_time = []

for i in range(1, 7):
    month = datetime.date(now.year, monthinteger - i, now.day).strftime('%B')

    filterQuery = "startTime:[NOW-{0}MONTHS TO NOW-{1}MONTHS]" .format(i, i-1)
    # print filterQuery
    url = base + "q=" + query + "&fq=" + filterQuery + "&fl=" + searchFields
    print "URL: " + url
    page = requests.get(url)
    xml = page.content
    # print xml
    root = etree.fromstring(xml)
    numFound = int(root.xpath('//result/@numFound')[0])
    print "ads in {0}: {1}" .format(month, str(numFound))
    dict_ads_time.append(numFound)
    # numFound = 2220

    dict_ads_geo = {}
    dict_bidder_geo = {}
    cnt_bidder = 0
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

    print "buyer in {0}: {1}\n" .format(month, str(cnt_bidder))
    dict_bidder_time.append(cnt_bidder)


with open("Buyer_Temporal.txt", "w") as f:
    print("Month\tFrequency")
    f.write("Month\tFrequency\n")
    for idx, value in enumerate(dict_bidder_time, start = 1):
        month = datetime.date(now.year, monthinteger - idx, now.day).strftime('%B')
        stat = month + "\t" + str(value)
        print stat
        f.write(stat+"\n")
with open("Ads_Temporal.txt", "w") as f:
    print("Month\tFrequency")
    f.write("Month\tFrequency\n")
    for idx, value in enumerate(dict_ads_time, start = 1):
        month = datetime.date(now.year, monthinteger - idx, now.day).strftime('%B')
        stat = month + "\t" + str(value)
        print stat
        f.write(stat+"\n")
