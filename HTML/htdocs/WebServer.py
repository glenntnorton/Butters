#####
#
# FSSCLibrary Resource
# Copyright (C) 2010 Finnean-SSC. All Rights Reserved.
# 
# Author: Glenn Norton
# 
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#
# 3. This notice may not be removed or altered from any source distribution.
#
#####

import sys
import BaseHTTPServer
import CGIHTTPServer
class WebServer(object):
    def __init__(self, host='', port=8080, cgi_dir='/cgi-bin'):
        self._host = host
        self._port = port
        self._cgi_dir = cgi_dir

        self._cgi_handler = CGIHTTPServer.CGIHTTPRequestHandler

        self._cgi_handler.cgi_directories.append(self._cgi_dir)
        self._server_addr = ((self._host, self._port))
        self._httpd = BaseHTTPServer.HTTPServer(self._server_addr, self._cgi_handler)
    
    def run(self):
        try:
            self._httpd.serve_forever()
        except KeyboardInterrupt:
            self._httpd.server_close()
            sys.exit(0)


if __name__ == '__main__':
    WebServer().run()

# END WebServer
