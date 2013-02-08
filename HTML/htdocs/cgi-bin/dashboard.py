#!C:/python/python.exe

import sys; sys.path.insert(0, r'D:\Lib')
import cgi
import time
import Encryption
from Cheetah.Template import Template
from com.finnean.database.connection import SQLiteConnection
from com.finnean.database.cursor import SQLiteDictionaryCursor
from com.finnean.database.query import SQLiteQuery
from objects import Login


# encryption key
pass_key = 'rcCE3qqHyD3LSNH73vKzPhW3aURH4nSH'
enc = Encryption.Encryption(passkey=pass_key)

# database
database = SQLiteConnection.SQLiteConnection()
connection = database.connect(r'D:\wamp\apps\sqlitemanager1.2.0\Butters.db')
cursor = SQLiteDictionaryCursor.SQLiteDictionaryCursor(connection).get()

query = SQLiteQuery.SQLiteQuery()
query.setCursor(cursor)
query.setExceptionHandler(database.getExceptionHandler())


# cgi
form = cgi.FieldStorage()
username = form.getvalue('username')
passwd = form.getvalue('passwd')

login_ok = False
results = query.select(
    query="""SELECT * FROM login WHERE username=?""", 
    arg_list=[username]
)
if results:
    if enc.decrypt(results[0]['passwd']) == passwd:
        login_ok = True


#enc_passwd = enc.encrypt(passwd)
#login = Login()
#login.username = username
#login.passwd = enc_passwd
#login.created = int(time.time())
#query.insert(table='login', object=login)


html = Template(file=r'templates\dashboard.html')
if not login_ok:
    html = Template(file=r'templates\login.html')
    html.msg = 'Login Failed.'
print "Content-type: text/html\n"
print html
