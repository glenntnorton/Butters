#!/usr/bin/env python

import sys; sys.path.insert(0, r'D:\Lib')
from Cheetah.Template import Template
html = Template(file=r'templates\new_infr_scheme.html')
print "Content-type: text/html\n"
print html
