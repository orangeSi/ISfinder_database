#!/usr/bin/env python
import sys
import os

if len(sys.argv) !=2:
    print ('python %s <prefix of output> for https://www-is.biotoul.fr/search.php' % (sys.argv[0]))
    sys.exit()
from  bs4 import BeautifulSoup
import requests
import string
import re
import time

rq = requests.Session()
def search_by_name_prefix(paras, url, prefix):
    header = {
            "Host": "www-is.biotoul.fr",
            "Connection": "keep-alive",
            "Content-Length": "358",
            "Cache-Control": "max-age=0",
            "Origin": "https://www-is.biotoul.fr",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "DNT": "1",
            "Referer": "https://www-is.biotoul.fr/search.php",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            }
    rq.get(search_url)
    r = rq.post(url, data=paras, headers=header)
    if r.status_code == 200:
        content = r.text
        #print('content:'+content)
        out = prefix+'.search.result.html'
        open(out, 'w').write(content)
        if re.search('No result in the database', content):
            print ('prefix:'+prefix+', has No result in the database')
        else:
            print (out+" done")
        
    else:
        print ('prefix:'+ prefix +', status err:'+str(r.status_code))
		
def download(html):
    base='https://www-is.biotoul.fr/scripts/'
    ids = ''
    search_num = 0
    html_code = open(html, 'r').read()
    if re.search('No result in the database', html_code):
        print(html+':No result in the database')
        return 0, ""

    print(html)
    raw = BeautifulSoup(html_code, "html.parser")
    line = ''
    for tr in raw.find_all('tr'):
        line += '\t'.join([td.text for td in tr.find_all('td')]) + '\n'
    out_table = html+'.table.txt'
    open(out_table, 'w').write(line)
    print(out_table)
    for link in raw('a'):
        href = link['href']
        if re.match('ficheIS.php\?name=IS', href):
            IS_id = re.sub('.*name=', '', href)
            print('IS_id:'+str(IS_id))
            ids = ids + base+href + "\n"
            print(base+href)
    for h3 in raw('h3'):
        if re.search('Result of your query: ', h3.text):
            search_num = re.sub('Result of your query:\s+', '', h3.text)
            search_num = int(search_num)
    return int(search_num), ids
    
	
	
	
    
pre = sys.argv[1]
IS_numbers = ["IS"+str(i) for i in range(10)]
IS_letters = ["IS"+letter for letter in list(string.ascii_lowercase)]
IS_Name_Prefix = IS_numbers + IS_letters
print ('IS_Name_Prefix is:'+str(IS_Name_Prefix))
print ('and then length is:'+str(len(IS_Name_Prefix)))

search_url = 'https://www-is.biotoul.fr/search.php'
#rq.get(search_url)
total_num = 0
ids = ''
for prefix in IS_Name_Prefix:
    paras = {"tout":"", "namecond":"contains", "name":'', "MGEtype":"all", "familycond":"contains", "family":"", "grpcond":"contains", "grp":"", "hostcond":"contains", "host":"", "accessioncond":"contains", "accession":"", "ir_lcond":"contains", "ir_l":"", "ir_rcond":"contains", "ir_r":"", "ircond":"egal", "ir":"", "drcond":"egal", "dr":"", "orfsizecond":"egal", "orfSize":"", "orffunctioncond":"contains", "orfFunction":"", "lengthcond":"egal", "length":"", "frameshift":"2", "output":"0", "Onsubmit":"Submit"}
    paras['name'] = prefix
    print('prefix:'+prefix)
    #IS_search_result_html = 
    search_by_name_prefix(paras, 'https://www-is.biotoul.fr/scripts/search-db.php', prefix)
    print('search done:'+prefix)
    print('start sleep 3s')
    time.sleep(3)
    print('end sleep 3s')
    seach_result_html = prefix+'.search.result.html'
    nums, id_list = download(seach_result_html)
    total_num += nums
    ids += id_list

print('total_num:'+str(total_num))
open(pre+'.IS.ID.list', 'w').write(ids)




