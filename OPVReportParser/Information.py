class Information(object):
    def __init__(self, info=[]):
        self.info = info
        if info:
            self.severity, self._id, self.data = self.info

    def getSeverity(self):
        return self.severity.text
    def setSeverity(self, s):
        self.severity = s

    def getId(self):
        return self._id.text
    def setId(self, i):
        self._id = i

    def getData(self):
        return self.data.text.lstrip().rstrip()
    def setData(self, d):
        self.data = d

## ----------------------------------------------
import unittest
class TestInformation(unittest.TestCase):
    def setUp(self):
        from elementtree import ElementTree as et
        from com.finnean.io.reader import XMLReader

        reader = XMLReader.XMLReader(r'D:\Lib\Butters\new-results.xml')
        root = et.XML(reader.read())
        results = root.findall('results')
        result = results[0].findall('result')
        host, date, ports = result[0].getchildren()
        p = ports[0]
        service, information = p.getchildren()

        self.info = Information(information.getchildren())

    def testConstructorArguments(self):
        self.failIf(type(self.info.info) != type([]))

    def testSeverityData(self):
        self.failIf(self.info.getSeverity() is None)
    def testSeverityValue(self):
        self.failUnless(type(self.info.getSeverity()) == type(''))

    def testIdData(self):
        self.failIf(self.info.getId() is None)
    def testIdValue(self):
        self.failUnless(type(self.info.getId()) == type(''))

    def testDataData(self):
        self.failIf(self.info.getData() is None)
    def testDataValue(self):
        self.failUnless(type(self.info.getData()) == type(''))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

