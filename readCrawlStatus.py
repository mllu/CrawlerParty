import nutchpy
import sys

# path = 'path-to-nutch/nutch/runtime/local/crawl/crawldb/current/part-00000/data'
if len(sys.argv) < 4:
    print("python3 printCrawlStatistic.py crawlDbDataFile failUrlFile contentTypeFile statisticFile")
    exit()
path = sys.argv[1]
failUrlOutputFile = sys.argv[2]
contentTypeOutputFile = sys.argv[3]
statisticFile = sys.argv[4]

count = nutchpy.sequence_reader.count(path)
print(count)
data = nutchpy.sequence_reader.read_iterator(path)
i = 0
statusTypeSet = set()
contentTypeSet = set()
imageTypeSet = set()
failUrllist = []
urlStatistics = []
failUrlOutput = open(failUrlOutputFile, "w")
contentTypeOutput = open(contentTypeOutputFile, "w")
statisticFile = open(statisticFile, "w")

imageCount = 0

for list_item in data:
    # if i < 10:
    # print(list_item[0])  # Prints the url
    # print(list_item[1])  # Prints details abt the url
    i += 1
    if i % 10000 == 0:
        print(i)
    # print(type(list_item[1]))
    for key in list_item[1]:
        # print(list_item[1])
        if "Status" in key:
            statusTypeSet.add(list_item[1][key])
            # urlStatistics.append((str(list_item[0]), list_item[1][key]))
            if "db_fetched" not in list_item[1][key] and "db_unfetched" not in list_item[1][key] \
                    and "db_duplicate" not in list_item[1][key]:
                url = list_item[0]
                failUrllist.append((str(url), list_item[1][key]))
        if "Content-Type" in key:
            contentTypeSet.add(list_item[1][key])
            if "image" in list_item[1][key]:
                imageTypeSet.add(list_item[1][key])
                imageCount += 1

            if "Status" in list_item[1] and "db_unfetched" not in list_item[1]["Status"] \
                    and "db_duplicate" not in list_item[1]["Status"]:
                urlStatistics.append([str(list_item[0]), str(list_item[1]["Status"]), list_item[1][key]])

for item in failUrllist:
    print(item)
    # print(str(item[0]), str(item[1]))
    failUrlOutput.write(str(item[0]) + "\n" + str(item[1]) + "\n")

print()

failUrlOutput.write("All Db status:\n")
for item in statusTypeSet:
    # print(item)
    failUrlOutput.write(item + "\n")
failUrlOutput.close()
for item in urlStatistics:
    statusCode = "200"
    if "fetched" in item[1]:
        statusCode = "200"
    elif "perm" in item[1]:
        statusCode = "301"
    elif "temp" in item[1]:
        statusCode = "302"
    elif "gone" in item[1]:
        statusCode = "404"
    # print(item)
    statisticFile.write(str(item[0]) + "\n" + statusCode + "\n" + str(item[2]) + "\n")
    statisticFile.write("\n")

contentTypeOutput.write("ImageCount: " + str(imageCount)+"\n")
for item in imageTypeSet:
    print(item)
    contentTypeOutput.write(item + "\n")
    contentTypeOutput.write("\n")

print()
print()
for item in contentTypeSet:
    print(item)
    contentTypeOutput.write(item + "\n")

# print(failList)
