#!/usr/bin/env python
import sys
import os

if len(sys.argv) !=3:
    print ('python %s <step1.IS.ID.list from step1> <outdir> for https://www-is.biotoul.fr/search.php' % (sys.argv[0]))
    sys.exit()
from  bs4 import BeautifulSoup
from Bio import SeqIO
import requests
import string
import re
import time

rq = requests.Session()
lists, outdir = sys.argv[1:]
lists_h = open(lists, 'r')
ids = {}
uncomplete = open(outdir+'/unfinish.task.list', 'w')
for line in lists_h:
    line = line.strip()
    arr = line.split('name=')
    ids[arr[1]] = line
    print('start:'+line)
    r = rq.get(line)
    if r.status_code == 200:
        IS_text = r.text
        print('get:'+line)
        out = outdir+'/'+ arr[1]+'.html'
        open(out, 'w').write(IS_text)
        IS_html = BeautifulSoup(IS_text, "html.parser")
        IS_seq = IS_html.find('div', class_="seq").text
        out = outdir+'/'+ arr[1]+'.seq.fa'
        open(out, 'w').write(">"+arr[1]+'\n'+IS_seq+'\n')
        print(out)
        time.sleep(2)
    else:
        print('error:'+str(r.status_code)+':'+line)
        uncomplete.write(line)


uncomplete.close()
print("warn:please check the file "+outdir+'/unfinish.task.list!!!!')

        

    





