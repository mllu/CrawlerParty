import nutchpy
import sys

# path = 'path-to-nutch/nutch/runtime/local/crawl/crawldb/current/part-00000/data'
if len(sys.argv) < 3:
    print("python3 retrieveImgUrls.py crawlDbDataFile outputImgUrlFile")
    exit()
path = sys.argv[1]
outputImgUrlFile = sys.argv[2]

count = nutchpy.sequence_reader.count(path)
print(count)
data = nutchpy.sequence_reader.read_iterator(path)
i = 0
imageOutput = open(outputImgUrlFile, "w")

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
        if "Content-Type" in key:
            if "image" in list_item[1][key]:
                imageOutput.write(str(list_item[0]) + "\n")
                imageCount += 1

print()
print(imageCount)
# print(failList)
