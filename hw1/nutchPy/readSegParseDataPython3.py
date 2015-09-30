import os
import re
import sys
import nutchpy

'''
    :param path: system path to segmentDir/content/part-xxxxx/data 
'''

if len(sys.argv) != 2:
    print ("usage: python readSegContentData.py segmentDir/content/part-xxxxx/data")
    sys.exit()

path = sys.argv[1]
#data = nutchpy.sequence_reader.read(path)
# Debug: read only two data
seq_reader = nutchpy.sequence_reader
#data = seq_reader.head(2,path)
imageUrls = set()
urlset = set()
image_types = set()
all_types = set()

count = seq_reader.count(path)
print("count of data: %d" % count)
#print(seq_reader.head(1,node_path))
f = open('temp.log','w')
print("MIME type:")
f.write("MIME type: \n")

cnt = 10
iteration = count / cnt;
for i in range(1,iteration):
#for i in range(1):
    #print i
    slice = seq_reader.slice(i*cnt, (i+1)*cnt, path)
    #print str(slice)
    #f.write(str(slice))

    #for d in data:
    for s in slice:
        #header = d[1]
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
            print (meta_data_list['Content-Type']) 
            f.write(meta_data_list['Content-Type']+"\n")
            if "image" in meta_data_list['Content-Type']:
                image_types.add(meta_data_list['Content-Type'])

print "\nAll MIME type:"
for type in all_types:
    str = "\ttype: %s\n"% type
    print (str)
    f.write(str)
print "Unique Image MIME type:"
for type in image_types:
    str = "\ttype: %s\n"% type
    print (str)
    f.write(str)
    #print "\t%s" % "type", "%s"% type

f.close()
