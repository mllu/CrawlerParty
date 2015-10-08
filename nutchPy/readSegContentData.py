import os
import re
import sys
import nutchpy

'''
    :param path: system path to segmentDir/content/part-xxxxx/data 
'''

if len(sys.argv) != 2:
    print "usage: python readSegContentData.py segmentDir/content/part-xxxxx/data"
    sys.exit()

path = sys.argv[1]
seq_reader = nutchpy.sequence_reader
#data = nutchpy.sequence_reader.read(path)
# Debug: read only two data
#seq_reader = nutchpy.sequence_reader
#data = seq_reader.head(2,path)
imageUrls = set()
urlset = set()
image_types = set()
all_types = set()

#print(seq_reader.head(1,node_path))
f = open('segContentData.log','w')
print("MIME type:")
f.write("MIME type: \n")

count = seq_reader.count(path)
print("count of data: %d" % count)
f.write("count of data: %d\n" % count)

cnt = 10
iteration = count / cnt + 1;
print("Total Run: %d" % iteration)
f.write("Total Run: %d\n" % iteration)

for i in range(0,iteration):
    print "\nround %d: from %d to %d"% (i+1, i*cnt, (i+1)*cnt-1) 
    f.write("\nround %d: from %d to %d\n"% (i+1, i*cnt, (i+1)*cnt-1))
    slice = seq_reader.slice(i*cnt, (i+1)*cnt-1, path)
    for s in slice:
        header = s[1]
        header_data = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\n", header))
        if header_data['contentType'] not in all_types:
            #import pdb; pdb.set_trace()
            all_types.add(header_data['contentType'])
            print header_data['contentType']
            f.write(header_data['contentType']+"\n")
            if "image" in header_data['contentType']:
                image_types.add(header_data['contentType'])

print "\nAll MIME type:"
f.write("\nAll MIME type:\n")
for type in all_types:
    print "\ttype: %s\n"% type
    f.write("\ttype: %s\n"% type)

print "Unique Image MIME type:"
f.write("\nUnique Image MIME type:\n")
for type in image_types:
    str = "\ttype: %s\n"% type
    print str
    f.write(str)
    #print "\t%s" % "type", "%s"% type

f.close()

