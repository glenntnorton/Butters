#!D:/python/python.exe

import sys; sys.path.insert(0, r'D:\Lib')
import cgi
import time

from Cheetah.Template import Template
from com.finnean.database.connection import SQLiteConnection
from com.finnean.web.session import SQLiteSession
from com.finnean.web.cgi import CGI
from com.finnean.object.map import DictionaryToAttributeMapper
from com.finnean.util.generator import KeyGenerator
from objects import NewAccount

database = SQLiteConnection.SQLiteConnection()
connection = database.connect(r'D:\wamp\apps\sqlitemanager1.2.0\Butters.db')
mapper = DictionaryToAttributeMapper.DictionaryToAttributeMapper()
sid = KeyGenerator.KeyGenerator().generate(length=32)
session = SQLiteSession.SQLiteSession(connection, sid)

cgi = CGI.CGI()
new_account = NewAccount.NewAccount()
mapper.map(new_account, cgi.params())
session['new_account'] = new_account

html = Template(file=r'templates\terms.html')
html.sid = sid
print "Content-type: text/html\n"
print html
