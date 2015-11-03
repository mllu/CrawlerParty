


import requests
from lxml import etree
from dateutil import parser
import re


base = "http://localhost:8983/solr/techproducts/select?"
query = "*"
filterQuery = "startTime:[*%20TO%20NOW]"
searchFields = "title+seller+sellerRating+bidder+gunModel+location+startTime+endTime+pagerank_gunCategory+pagerank_location+pagerank_temporal"
url = base + "q=" + query + "&fq=" + filterQuery + "&fl=" + searchFields
print "URL: " + url
# url + "&start=2220"
page = requests.get(url)
xml = page.content
# print xml
root = etree.fromstring(xml)
numFound = int(root.xpath('//result/@numFound')[0])
print "numFound: " + str(numFound) + "\n"

# numFound = 2220
dict_ads_geo = {}
dict_bidder_geo = {}

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
            bidderInfo = bidder[0].replace(u'\xa0', u' ')
            # print "bidder: " + bidderInfo

            if loc in dict_bidder_geo:
                cnt = dict_bidder_geo[loc]
                dict_bidder_geo[loc] = cnt + 1
            else:
                dict_bidder_geo[loc] = 1
            # print "Num of bidders in {0} are {1}." .format(loc, str(dict_bidder_geo[loc]))
            # print "\n"

# dump buyer vs spatial for rifle
with open("Buyer_Spatial.txt", "w") as f:
    print("loc\tfreq")
    f.write("loc\tfreq\n")
    for key, value in dict_bidder_geo.iteritems():
        stat = key + "\t" + str(value)
        print stat
        f.write(stat+"\n")

with open("Ads_Spatial.txt", "w") as f:
    print("loc\tfreq")
    f.write("loc\tfreq\n")
    for key, value in dict_ads_geo.iteritems():
        stat = key + "\t" + str(value)
        print stat
        f.write(stat+"\n")
