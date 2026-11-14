import urllib.request, urllib.parse, sys, xml.etree.ElementTree as ET
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 25
url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":q,"start":0,"max_results":n,"sortBy":"submittedDate","sortOrder":"descending"})
d=urllib.request.urlopen(url,timeout=60).read().decode()
r=ET.fromstring(d)
ns={'a':'http://www.w3.org/2005/Atom'}
tot=r.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults')
print('total:',tot.text if tot is not None else '?')
for e in r.findall('a:entry',ns):
    t=e.find('a:title',ns).text.strip().replace('\n',' ')
    p=e.find('a:published',ns).text[:10]
    i=e.find('a:id',ns).text
    print(p,'|',t,'|',i)
