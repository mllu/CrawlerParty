import nutchpy

#node_path = "/Users/mllu/workspace/CrawlerParty/crawl/merged/20150922030212/parse_data/part-00000/data"
node_path = "./crawl/merged/20150922030212/content/part-00000/data"
seq_reader = nutchpy.sequence_reader
print(seq_reader.head(10,node_path))
print(seq_reader.slice(10,20,node_path))
