import tika
from tika import parser
import sys
import os

tika.initVM()

inputDir = sys.argv[1]
dirs = os.listdir(inputDir)
for eachFile in dirs:
    parsed = parser.from_file(os.path.join(inputDir, eachFile))
    print(parsed['metadata'])
    print(parsed['content'])
