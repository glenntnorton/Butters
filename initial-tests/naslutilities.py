import re

desc = re.compile(r'''^\s*desc\s*\=\s*\"\s*([^\"]*)\"\s*\;$''', re.MULTILINE)
#end = re.compile('^\s?Risk\s+', re.IGNORECASE)
#script_id = re.compile('script_id\((\d+)\);')
#cve_id = re.compile('script_cve_id\(\"(CVE-\d+-\d+)\"\)')
#name = re.compile('name = \"(\w+)\"')
#
#def getNaslDescription(filename):
#    fd = open(filename, 'r')
#    lines = fd.readlines()
#
#    s = e = 0
#    for i in range(0, len(lines)):
#        if re.match(start, lines[i]):
#            s = i
#        if re.match(end, lines[i]):
#            e = i
#
#    return ''.join(lines[s:e])
#
import glob
qfiles = glob.glob(r'/usr/lib/openvas/plugins/nvt/z*.nasl')
for q in qfiles:
    lines = file(q).read()
    match = re.search(desc, lines)
    if match:
        print match.groups()[0]

#http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2008-7064
