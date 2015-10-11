import re
import sys
import nutchpy

__author__ = 'Taichi1'


def main():
    crawlDbFile = sys.argv[1]
    urlDomainFile = sys.argv[2]
    outputFile = sys.argv[3]

    urlDomainList = []

    with open(urlDomainFile, 'r') as f:
        for line in f:
            urlDomainList.append(line.strip())

    count = nutchpy.sequence_reader.count(crawlDbFile)
    print(count)
    data = nutchpy.sequence_reader.read_iterator(crawlDbFile)

    statisticDic = {}
    lineNumber = 0
    for list_item in data:
        #print list_item
        if lineNumber % 1000 == 0:
            print(lineNumber)
        #if lineNumber > 5:
        #    break
        
        # print type(list_item[0])
        # --> <class 'py4j.java_gateway.JavaObject'>
        # convert JavaObject to String with java API toString()
        url = list_item[0].toString()
        #print url.encode('utf-8')
        #print url

        #unable to handler unicode properly
        #url = str(list_item[0])
        domain = ""
        # print(urlDomainList)
        for key in urlDomainList:
            # print(domain)
            # print(url)
            if re.search(key, url):
                #print("matched")
                domain = key
                break
        # print(url)
        # print(domain)
        if domain != "":
            statisticPerUrl = statisticDic.get(domain,
                                               {"imageCount": 0, "urlCount": 0, "fetchSuccess": 0, "fetchUnfetched": 0,
                                                "fetchRedirectTemp": 0, "fetchGone": 0, "fetchRedirectPerm": 0})

            statisticPerUrl["urlCount"] += 1
            for key in list_item[1]:
                if "Status" in key:
                    if "db_fetched" in list_item[1][key]:
                        statisticPerUrl["fetchSuccess"] += 1
                    elif "db_unfetched" in list_item[1][key]:
                        statisticPerUrl["fetchUnfetched"] += 1
                    elif "db_redir_perm" in list_item[1][key]:
                        statisticPerUrl["fetchRedirectPerm"] += 1
                    elif "db_redir_temp" in list_item[1][key]:
                        statisticPerUrl["fetchRedirectTemp"] += 1
                    elif "db_gone" in list_item[1][key]:
                        statisticPerUrl["fetchGone"] += 1
                if "Content-Type" in key:
                    if "image" in list_item[1][key]:
                        statisticPerUrl["imageCount"] += 1
            statisticDic[domain] = statisticPerUrl
        lineNumber += 1
    with open(outputFile, 'w') as f:
        f.write("domain imageCount urlCount fetchSuccess fetchUnfetched fetchRedirectTemp fetchGone fetchRedirectPerm\n")
        # print(len(statisticDic))
        # print(statisticDic)
        for item in statisticDic:
            # print(statisticDic[item])
            tempDict = statisticDic[item]
            # print(type(tempDict))
            f.write(
                str(item) + " " + str(tempDict["imageCount"]) + " " + str(tempDict["urlCount"]) +
                " " + str(tempDict["fetchSuccess"]) + " " + str(tempDict["fetchUnfetched"]) + " " +
                str(tempDict["fetchRedirectTemp"]) + " " + str(tempDict["fetchGone"]) + " " +
                str(tempDict['fetchRedirectPerm']) + "\n")


if __name__ == '__main__':
    def usage():
        print('''Synopsis: %s crawlDbDateFile urlDomain outputFile
urlDomain file should be a list of key domain words:
gunsinternational
hipointfirearmsforums
iwanna
etc
    ''' % sys.argv[0])
        sys.exit(1)


    if len(sys.argv) < 3:
        usage()
    main()
