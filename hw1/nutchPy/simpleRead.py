import nutchpy
import sys
# usage python read.py DATA_PATH
# ex:
# python read.py "./crawl/merged/20150922030212/content/part-00000/data"

#print sys.argv[1]
node_path = sys.argv[1]
seq_reader = nutchpy.sequence_reader
count = seq_reader.count(node_path)
print("count of data: %d" % count)
#print(seq_reader.head(1,node_path))
f = open('tempRead.log','w')
cnt = 10
iteration = count / cnt;
slice = []
#for i in range(1,iteration):
for i in range(9):
    print i
    slice = seq_reader.slice(i*cnt,(i+1)*cnt,node_path)
    print str(slice)
    f.write(str(slice))
f.close()
