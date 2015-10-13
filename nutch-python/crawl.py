from nutch.nutch import Nutch
from nutch.nutch import SeedClient
from nutch.nutch import Server
from nutch.nutch import JobClient
import nutch
import sys

sv = Server('http://localhost:8081')
sc = SeedClient(sv)
seedFile = sys.argv[1]
rounds = 1
if len(sys.argv) > 2:
    rounds = sys.argv[2]
seed_urls = []
with open(seedFile) as f:
    for line in f:
        seed_urls.append(line.strip())
sd = sc.create('espn-seed', seed_urls)

nt = Nutch('default')
jc = JobClient(sv, 'test', 'default')
cc = nt.Crawl(sd, sc, jc, int(rounds))
while True:
    job = cc.progress()  # gets the current job if no progress, else iterates and makes progress
    if job is None:
        break
