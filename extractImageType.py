import os
import sys
import nutchpy

# path = os.path.dirname(nutchpy.__file__)
# path = os.path.join("crawl", "segments", "20150922153703", "content","part-00000", "data")
path = sys.argv[1]
data = nutchpy.sequence_reader.read(path)
imageUrls = set()
urlset = set()
imageTypes = set()
for i in range(0, len(data)):

	
	keyValues = data[i][1].split("\n")
	valueDict = {}
	for keyValuePair in keyValues:
		keyValueArray = keyValuePair.split(": ")
		# print(keyValuePair)
		# print(keyValueArray)
		if len(keyValueArray) >= 2:
			valueDict[keyValueArray[0]] = keyValueArray[1]
			if "contentType" in valueDict:
				# print(data[i][0]+" has contentType")
				if "image" in valueDict["contentType"]:
					print(data[i][0]+" has contentType of image: " + valueDict["contentType"])
						# print (len(urlset))
					imageTypes.add(valueDict["contentType"])
					imageUrls.add(data[i][0])
					urlset.add(data[i][0])

print(imageUrls)
print(imageTypes)
# assert len(data) == 5

# data = nutchpy.sequence_reader.slice(5,20,path)
# # print(data)
# # assert len(data) == 2

# #hadoop fs -text path <-- equivalent
# data = nutchpy.sequence_reader.read(path)
# print(data)
# assert len(data) == 8