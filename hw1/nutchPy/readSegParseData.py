import os
import re
import sys
import nutchpy

'''
    :param path: system path to segmentDir/parse_data/part-xxxxx/data 
'''

if len(sys.argv) != 2:
    print "usage: python readSegParseData.py segmentDir/parse_data/part-xxxxx/data"
    sys.exit()

path = sys.argv[1]
#data = nutchpy.sequence_reader.read(path)
# Debug: read only two data
seq_reader = nutchpy.sequence_reader
#data = seq_reader.head(2,path)
image_types = set()
all_types = set()

f = open('segParseData.log','w')
print("MIME type:")
f.write("MIME type: \n")

count = seq_reader.count(path)
print("count of data: %d" % count)
f.write("count of data: %d\n" % count)
#print(seq_reader.head(1,node_path))

cnt = 10
iteration = count / cnt + 1;
print("Total Run: %d" % iteration)
f.write("Total Run: %d\n" % iteration)
for i in range(0,iteration):
    print("\nround %d: from %d to %d" % (i+1, i*cnt, (i+1)*cnt-1))
    f.write("\nround %d: from %d to %d\n" % (i+1, i*cnt, (i+1)*cnt-1))
    slice = seq_reader.slice(i*cnt, (i+1)*cnt-1, path)
    #print str(slice)
    #f.write(str(slice))

    for s in slice:
        header = s[1]
        header_data = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\n", header))
        #print header_data
        meta_data = header_data['Content Metadata']
        #print metaData
        meta_data_list = dict(re.findall(r"(?P<key>.*?)=(?P<value>.*?) ", meta_data))
        #print meta_data_list
        if "Content-Type" in meta_data_list and meta_data_list['Content-Type'] not in all_types:
            #import pdb; pdb.set_trace()
            all_types.add(meta_data_list['Content-Type'])
            print meta_data_list['Content-Type'] 
            f.write(meta_data_list['Content-Type']+"\n")
            if "image" in meta_data_list['Content-Type']:
                image_types.add(meta_data_list['Content-Type'])

print "\nAll MIME type:"
f.write("\nAll MIME type:\n")
for type in all_types:
    str = "\ttype: %s\n"% type
    print str
    f.write(str)

print "Unique Image MIME type:"
f.write("\nUnique Image MIME type:\n")
for type in image_types:
    str = "\ttype: %s\n"% type
    print str
    f.write(str)
    #print "\t%s" % "type", "%s"% type

f.close()
