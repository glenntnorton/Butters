###############################################################################
# OpenVAS Vulnerability Test
# $Id: qwerty_cms_sql_injection.nasl 81 2009-03-05 12:50:35Z mime $
#
# Qwerty CMS 'index.php' SQL Injection Vulnerability
#
# Authors:
# Michael Meyer
#
# Copyright:
# Copyright (c) 2009 Greenbone Networks GmbH
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# (or any later version), as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################

if (description)
{
 script_id(100013);
 script_bugtraq_id(33885);
 script_version ("1.0");
 script_tag(name:"risk_factor", value:"Medium");

 script_name("Qwerty CMS 'index.php' SQL Injection Vulnerability");
 desc = "

 Overview:
  Qwerty CMS is prone to an SQL-injection vulnerability because it fails to
  sufficiently sanitize user-supplied data before using it in an SQL query.

  Exploiting this issue could allow an attacker to compromise the application,
  access or modify data, or exploit latent vulnerabilities in the underlying
  database. 

 Risk factor : Medium";

 script_description(desc);
 script_summary("Determine if Qwerty CMS is vulnerable to SQL Injection");
 script_category(ACT_GATHER_INFO);
 script_family("Web application abuses");
 script_copyright("This script is Copyright (C) 2009 Greenbone Networks GmbH");
 script_dependencie("find_service.nes", "http_version.nasl");
 script_require_ports("Services/www", 80);
 script_exclude_keys("Settings/disable_cgi_scanning");
 exit(0);
}

include("http_func.inc");
include("http_keepalive.inc");

port = get_http_port(default:80);

if(!get_port_state(port))exit(0);
if(!can_host_php(port:port))exit(0);

dir = make_list("/cms","/qwerty", cgi_dirs()); 
 
foreach d (dir)
{ 
 url = string(d, "/index.php?act=publ&id=-3+UNION+SELECT+1,2,3,4,0x4f70656e5641532d53514c2d496e6a656374696f6e2d54657374");
 req = http_get(item:url, port:port);
 buf = http_keepalive_send_recv(port:port, data:req, bodyonly:1);
 if( buf == NULL )continue;
 
 if( buf =~ ".*OpenVAS-SQL-Injection-Test.*" )
   {    
    security_warning(port:port);
    exit(0);
   }
}
exit(0);
