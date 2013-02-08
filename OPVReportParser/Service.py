class Service(object):
    def __init__(self, data):
        self.data = data
        self.conf = None
        self.method = None
        self.name = None

        if self.data is not None:
            self.conf = self.data.get('conf')
            self.method = self.data.get('method')
            self.name = self.data.get('name')

    def getConf(self):
        return self.conf
    def setConf(self, c):
        self.conf = c

    def getMethod(self):
        return self.method
    def setMethod(self, m):
        self.method = m

    def getName(self):
        return self.name
    def setName(self, n):
        self.name = n

## ----------------------------------------------
import unittest
class TestService(unittest.TestCase):
    def setUp(self):
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
        self.s = Service(service)

    def testConstructorArguments(self):
        self.failIf(type(self.s.data) is None)

    def testConfData(self):
        self.failIf(self.s.getConf() is None)
    def testConfValue(self):
        self.failUnless(type(self.s.getConf()) == type(''))

    def testMethodData(self):
        self.failIf(self.s.getMethod() is None)
    def testMethodValue(self):
        self.failUnless(type(self.s.getMethod()) == type(''))

    def testNameData(self):
        self.failIf(self.s.getName() is None)
    def testNameValue(self):
        self.failUnless(type(self.s.getName()) == type(''))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

