import simhash
import sys
import os
import re
from simhash import Simhash, SimhashIndex

import hashlib


# Reference: http://joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/
def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def md5ChecksumWithString(stringinput):
    # print(stringinput)
    m = hashlib.md5()
    m.update(stringinput.encode())
    return m.hexdigest()


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


__author__ = 'Taichi1'

if len(sys.argv) < 3:
    print('''Synopsis: %s inputDir isExact
    isExact should be true or false
    ''' % sys.argv[0])
    exit()

inputDir = sys.argv[1]

is_exact = sys.argv[2]

hashDict = {}

record = {"url": "", "contentMD5Hash": "", "metadataSimHash": "", "textSimHash": "", "contentSimHash": "",
          "textMD5Hash": ""}

contentSimIndex = SimhashIndex([], k=3)
metadataSimIndex = SimhashIndex([], k=3)
textSimIndex = SimhashIndex([], k=3)
contentMd5Dict = {}
textMd5Dict = {}
contentSimDict = {}
metadataDict = {}
textDict = {}

contentDir = os.path.join(inputDir, "content")
metadataDir = os.path.join(inputDir, "metadata")
textDir = os.path.join(inputDir, "text")

dirs = os.listdir(contentDir)
print(len(dirs))
numberOfFiles = 0
for file in dirs:
    numberOfFiles += 1
    if numberOfFiles % 100 == 0:
        print(numberOfFiles)
    contentFilePath = os.path.join(contentDir, file)
    metadataFilePath = os.path.join(metadataDir, file)
    textFilePath = os.path.join(textDir, file)
    url = ""
    # read the content, metadata, parsetext into memory
    with open(metadataFilePath, "r") as f:
        url = f.readline()
        record["url"] = url.strip()
        record["metadataSimHash"] = Simhash(get_features(f.readline().strip()))
    with open(textFilePath, "r") as f:
        url = f.readline()
        record["url"] = url.strip()
        # record["text"] = f.readline().strip()
        text = f.readline().strip()
        # print(text, text == "Google Google")
        if text != "":
            record["textSimHash"] = Simhash(get_features(text))
            record["textMD5Hash"] = md5ChecksumWithString(text)
    with open(contentFilePath, "rb") as f:
        record["contentSimHash"] = Simhash(get_features(f.read().decode('cp437')))
    record["contentMD5Hash"] = md5Checksum(contentFilePath)

    contentSimIndex.add(record["url"], record["contentSimHash"])
    metadataSimIndex.add(record['url'], record["metadataSimHash"])
    textSimIndex.add(record['url'], record["textSimHash"])
    # print("record", record)
    hashDict[record["url"]] = record
    if is_exact.lower() == "true":
        if record["contentMD5Hash"] in contentMd5Dict or record["textMD5Hash"] in textMd5Dict:
            if record["contentMD5Hash"] in contentMd5Dict:
                print("exact\n", record["url"], contentMd5Dict[record["contentMD5Hash"]] )
                contentMd5Dict[record["contentMD5Hash"]].add(record["url"])
            elif record["textMD5Hash"] in textMd5Dict:
                print("exact\n", record["url"], textMd5Dict[record["textMD5Hash"]])
                textMd5Dict[record["textMD5Hash"]].add(record["url"])
                #             print out the exact duplicate and what it is a duplicate against
        else:
            # to handle the case that the texeMd5hash or contentMd5Hash is 0
            if record["contentMD5Hash"] != "" and record["textMD5Hash"] != "":
                contentMd5Dict[record["contentMD5Hash"]] = set()
                contentMd5Dict[record["contentMD5Hash"]].add(record["url"])
                textMd5Dict[record["textMD5Hash"]] = set()
                textMd5Dict[record["textMD5Hash"]].add(record["url"])
    else:
        duplicateSet = set()
        for url in contentSimIndex.get_near_dups(record["contentSimHash"]):
            # if url != record["url"] and (url in textSimIndex.get_near_dups(
            #         record["textSimHash"]) or url in metadataSimIndex.get_near_dups(record["metadataSimHash"])):
            #     print("near\n", url, record["url"])
            duplicateSet.add(url)
        for url in textSimIndex.get_near_dups(record["textSimHash"]):
            # if url != record["url"] and (url in textSimIndex.get_near_dups(
            #         record["textSimHash"]) or url in metadataSimIndex.get_near_dups(record["metadataSimHash"])):
            #     print("near\n", url, record["url"])
            duplicateSet.add(url)
        for url in metadataSimIndex.get_near_dups(record["metadataSimHash"]):
            duplicateSet.add(url)
        if len(duplicateSet) > 1:
            print("Near Duplicates: " + record["url"])
            for url in duplicateSet:
                if url != record["url"]:
                    print(url)
            print()
            print()
