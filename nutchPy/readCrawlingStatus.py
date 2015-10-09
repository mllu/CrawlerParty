import os
import sys
import nutchpy

# segmentPath = os.path.join("crawl", "segments", "20150922153703")
segmentPath = sys.argv[1]
path = os.path.join(segmentPath, "crawl_fetch","part-00000", "data")
data = nutchpy.sequence_reader.read(path)

statusDict = {}
for i in range(0, len(data)):
	keyValues = data[i][1].split("\n")
	print(keyValues)
	valueDict = {}
	isFailed = False
	for keyValuePair in keyValues:
		keyValueArray = keyValuePair.split(": ")
		if len(keyValueArray) >= 2:
			if keyValueArray[0] == "Status":
				status = keyValueArray[1]
				if "67 (linked)" not in status and "33 (fetch_success)" not in status:
					isFailed = True
					statusDict[data[i][0]] = {}
					statusDict[data[i][0]]["status"] = status
			if isFailed:
				metadataIndex = data[i][1].index("Metadata")
				statusDict[data[i][0]]["metadata"] = data[i][1][metadataIndex:]

# you can easily redirect to a output file
for key, value in statusDict.items():
	print()
	print(key)
	print("status: " + value["status"])
	print("metadata: " +value["metadata"])
	print()
