#!C:/python/python.exe

import sys; sys.path.insert(0, r'D:\Lib')
from Cheetah.Template import Template
html = Template(file=r'templates\login.html')
print "Content-type: text/html\n"
print html
