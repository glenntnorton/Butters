from elementtree import ElementTree as et
from elementtree.ElementTree import tostring
from com.finnean.io.reader import XMLReader

reader = XMLReader.XMLReader(r'D:\Lib\Butters\new-results.xml')
root = et.XML(reader.read())
results = root.findall('results')
result = results[0].findall('result')
host, date, ports = result[0].getchildren()
p = ports[0]
service, information = p.getchildren()
severity, _id, data = information.getchildren()
