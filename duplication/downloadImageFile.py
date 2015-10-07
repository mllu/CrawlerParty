import urllib.request
import shutil
import sys
import os
from uuid import uuid4


def main():
    urlFile = sys.argv[1]
    outputDir = sys.argv[2]
    mapFilename = sys.argv[3]
    urlFileOpened = open(urlFile, "r")
    mapFile = open(mapFilename, 'w')
    for line in urlFileOpened:
        url = line
        file_name = uuid4()
        mapFile.write(url + str(file_name) + "\n")
        filepath = os.path.join(outputDir, str(file_name))
        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(url) as response, open(filepath, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)


if __name__ == '__main__':
    def usage():
        print("Synopsis: %s urlFile outputImageDir outputMapFileName " % sys.argv[0])
        sys.exit(1)


    if len(sys.argv) < 4:
        usage()
    main()
