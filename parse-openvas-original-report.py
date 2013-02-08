from elementtree import ElementTree as et
from elementtree.ElementTree import tostring
from com.finnean.io.reader import XMLReader

reader = XMLReader.XMLReader(r'D:\Lib\Butters\results.xml')
root = et.XML(reader.read())
results = root.findall('results')

df = open(r'D:\Lib\Butters\new-results.xml', 'w')
df.write('''<?xml version="1.0"?>\n''')
df.write('''<report>\n''')
df.write(tostring(results[0]))
df.write('''</report>\n''')
df.close()
