import urllib.request
from urllib.request import Request
import shutil
import sys
import os
from uuid import uuid4


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


def main():
    urlFile = sys.argv[1]
    outputDir = sys.argv[2]
    mapFilename = sys.argv[3]
    urlFileOpened = open(urlFile, "r")
    mapFile = open(mapFilename, 'w')
    count = 0
    for line in urlFileOpened:
        count += 1
    print(count)
    lineNumber = 1

    urlFileOpened.seek(0)

    for line in urlFileOpened:
        if lineNumber % 1000 == 0:
            print(lineNumber)
        # if lineNumber > 3:
        #     break
        url = line.strip()
        file_name = uuid4()
        mapFile.write(url + "\n" + str(file_name) + "\n")
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        filepath = os.path.join(outputDir, str(file_name))
        # Download the file from `url` and save it locally under `file_name`:
        # with urllib.request.urlopen(url) as response, open(filepath, 'wb') as out_file:
        #     shutil.copyfileobj(response, out_file)
        if "avatar" not in url and "discover" not in url:
            try:
                print(url.encode())
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                          'Chrome/34.0.1847.137 Safari/537.36'})
                with open(filepath, "wb") as f:
                    f.write(urllib.request.urlopen(req).read())
            except urllib.error.HTTPError as e:
                print("Oops, an Http Error", e)
            except urllib.error.URLError as e:
                print("Oops, an Url Error", e)
            except Exception as e:
                print("whatever Error", e)

        lineNumber += 1


if __name__ == '__main__':
    def usage():
        print("Synopsis: %s urlFile outputImageDir outputMapFileName " % sys.argv[0])
        sys.exit(1)


    if len(sys.argv) < 4:
        usage()
    main()
