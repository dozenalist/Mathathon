import urllib.request, urllib.parse, sys, xml.etree.ElementTree as ET
ids=sys.argv[1]
url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"id_list":ids,"max_results":10})
d=urllib.request.urlopen(url,timeout=60).read().decode()
r=ET.fromstring(d); ns={'a':'http://www.w3.org/2005/Atom'}
for e in r.findall('a:entry',ns):
    print('TITLE:',e.find('a:title',ns).text.strip())
    print('ID:',e.find('a:id',ns).text,' PUB:',e.find('a:published',ns).text[:10])
    print('AUTHORS:',', '.join(a.find('a:name',ns).text for a in e.findall('a:author',ns)))
    print('ABSTRACT:',e.find('a:summary',ns).text.strip())
    print('='*80)
