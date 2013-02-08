#!/usr/bin/env python
from __future__ import with_statement
from time import strftime, strptime
import re
import sys


#   tissynbe.py
#   Copyright (C) 2008-2009  Marcin Wielgoszewski (tssci-security.com)
#
#   Thanks to the following people for their contributions:
#   Romain Gaucher (rgaucher.info)
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__  = 'Marcin Wielgoszewski'
__version__ = '1.5'

DB_HOST   = 'hostname'
DB_UNAME  = 'username'
DB_PASSWD = 'password'


"""Compiled regular expression objects.

These are the compiled regex's we want to keep around for performing string
substitution.
"""

DOTS     = re.compile('( \.|\.\. )')
FIX      = re.compile('(10180|10287|10330|10386|10662|10761|10863|10919|'
                        +'11011|11033|11153|11936|12053|12245|12634|14773|'
                        +'17975|18261|18528|19506|22964|'
                        +'11040|11822|11865|14674)\\|(1|2|3)')
GMT      = re.compile('GMT(\!|\.)')
PIPE     = re.compile('[ ]*\\|[ ]*')
SOLUTION = re.compile('(Solution:|Risk factor:|CVSS|Plugin output:|See also:|'
                        +'CVE:|BID:)')
SYNDESC  = re.compile('( *Synopsis: *| *Description:)')
COMPL    = re.compile('21156\\|(1|2|3)\\|(Syntax error \([\w\d ]*\)|\"(.*)\"): ')
COMPL2   = re.compile('21156\\|(1|2|3)\\|\"(.*)\"\\|')
SNMP     = re.compile('(with the community name: [\w]+ )')
REPLACEMENTS =  [
    (' :',':'),
    ('the the','the'),
    (' interfer ',' interfere '),
    ('Security Note','1'),
    ('Security Warning','2'),
    ('Security Hole','3'),
    ('\\\\','\\'),
    ('10862|3|','10862|3|The SQL Server has a common password for one or '
     +'more accounts. These accounts may be used to gain access to the '
     +'records in the database or even allow remote command execution.|'),
    ('21725|3|','21725|3|The remote host has an out-dated version of the '
     +'Symantec Corporate virus signatures, or Symantec AntiVirus '
     +'Corporate is not running.|'),
    ('22035|2|','22035|2|The version of Adobe Acrobat installed on the '
     +'remote host is earlier than 6.0.5 and is reportedly affected by a '
     +'buffer overflow that may be triggered when distilling a specially-'
     +'crafted file to PDF.|'),
    ('34252|1|','34252|1|A Windows service is listening on this port.|'),
]


def clean_nbe(data):
    """Perform string replacements and substitutions on Nessus data.

    This function performs much needed cleanup and does some prettifying of
    Nessus results information.  It removes double spaces, adds descriptions to
    plugins missing them, and splits the plugin synopsis and description from
    the vulnerability solutions.  The order in which operations appear is
    semi-important, so don't try to change them around.
    
    """
    data = data.replace('\\n', ' ')
    data = ' '.join(data.split())
    for i, j in REPLACEMENTS:
        data = data.replace(i, j)
    data = DOTS.sub('.', data)
    data = SYNDESC.sub('', data)
    data = GMT.sub('GMT\\1|Renew the SSL certificate for the remote server.',
                   data, count=1)
    data = SOLUTION.sub('|\\1', data, count=1)
    data = COMPL.sub('21156|\\1|\\2|', data, count=1)
    data = COMPL2.sub('21156|\\1|\\2|', data)
    data = SNMP.sub('\\1|', data)
    data = PIPE.sub('|', data)
    data = FIX.sub('\\1|\\2|', data)
    data = data.rstrip(' ')
    return data


def parse_nbe(nbe):
    """Open an nbe file, parse, then split into fields.
    
    This code opens our input file we specified gracefully.  It then begins to
    process our data by calling clean_nbe() and then finally splits each line 
    on the pipe-delimiter.  If a line has less fields than required, it will 
    print the line to stdout.  Copy stdout to a file and send to
    tissynbe _at_ tssci-security.com.  I'll update the script to account for 
    these errors in processing.

    """
    with open(nbe, 'rU') as file:
        print """Processing""", nbe + """..."""
        results = []
        timestamps = []
        problems = []
        t_problems = []
        plugins = []

        for line in file:
            # Create a nested results list
            if line.startswith("results"):
                line = line.rstrip()
                line = clean_nbe(line)
                line = line.split('|',7)
                if len(line) > 7:
                    results.append(line[1:])
                elif len(line) > 4 and len(line) < 8:
                    issue = "Line length (%s/8):\t%s" % (len(line), '|'.join(line))
                    issue = issue.replace('\n', ' ')
                    problems.append(issue)
                    plugins.append(line[4])

            # Create a nested timestamps list
            elif line.startswith("timestamps"):
                line = line.rstrip('|\n')
                line = line.split('|')
                try:
                    line[4] = strftime("%Y-%m-%d %H:%M:%S", strptime(line[4]))
                except ValueError, e:
                    print "Error: %s" % (e)
                    continue
                except IndexError:
                    issue = "Line length (%s/5):\t%s" % (len(line), '|'.join(line))
                    t_problems.append(issue)
                    continue
                timestamps.append(line[2:])

        if problems:
            print """tissynbe.py had trouble parsing the following results:"""
            for issue in problems:
                print issue
        if t_problems:
            print """tissynbe.py had trouble parsing the following lines:"""
            for line in t_problems:
                print issue
        if plugins:
            print """The following plugins potentially cauesd an issue during parsing:"""
            print ','.join(list(set(plugins)))
        
        return results, timestamps


def insert_nbe(results,timestamps,database):
    """Insert parsed Nessus data into MySQL database.
    
    This block of code will insert our processed Nessus data into the MySQL
    database specified with the -d option on the command line.  Before doing 
    so, ensure you have the proper database schema.  After doing our SQL 
    INSERTs, the number of rows inserted into each table is printed for 
    reference. For database schema information see 
    http://www.tssci-security.com/upload/tissynbe_py/nessusdb.sql
    
    """
    import MySQLdb
    print """Executing SQL INSERT..."""

    try:
        db = MySQLdb.connect(DB_HOST,DB_UNAME,DB_PASSWD,database)
    except MySQLdb.Error, e:
        print """Error %d: %s""" % (e.args[0], e.args[1])
        sys.exit (1)

    c = db.cursor()
    results_rows = 0
    timestamps_rows = 0

    while results:
        small_results, results = results[:100], results[100:]   
        c.executemany("""INSERT INTO results 
                      (domain, host, service, scriptid, riskval, msg1, msg2) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s)""", (small_results))
        results_rows += c.rowcount

    while timestamps:
        small_timestamps, timestamps = timestamps[:100], timestamps[100:]
        c.executemany("""INSERT INTO timestamps 
                      (host,progress,timestamp) 
                      VALUES (%s, %s, %s)""", (small_timestamps))
        timestamps_rows += c.rowcount

    db.commit()
    print """Number of rows inserted: %d results""" % results_rows
    print """Number of rows inserted: %d timestamps""" % timestamps_rows


def select_nbe(database, risk, order, sort):
    """Perform SQL SELECT query.
    
    This section of code is used to perform a SQL SELECT query of Nessus data 
    already in a database specified using the -d option on the command line.

    """
    import MySQLdb
    print """Executing SQL SELECT..."""

    try:
        db = MySQLdb.connect(DB_HOST,DB_UNAME,DB_PASSWD,database)
    except MySQLdb.Error, e:
        print """Error %d: %s""" % (e.args[0], e.args[1])
        sys.exit (1)

    c = db.cursor()

    c.execute("""SELECT domain, host, service, scriptid, riskval, msg1, msg2 
              FROM results WHERE riskval >= %s 
              ORDER BY %s %s""", (risk, order, sort))

    results = c.fetchall()
    return results


def count_nbe(database, risk):
    """Perform SQL SELECT query displaying plugins by count.

    This function is similar to select_nbe(), except that it does not record
    domain or host information, instead performs a tally of plugins by count.  
    It is only called when --count is specified with a database on the command 
    line.
    
    """
    import MySQLdb
    print """Executing SQL SELECT with COUNT..."""

    try:
        db = MySQLdb.connect(DB_HOST,DB_UNAME,DB_PASSWD,database)
    except MySQLdb.Error, e:
        print """Error %d: %s""" % (e.args[0], e.args[1])
        sys.exit (1)

    c = db.cursor()

    c.execute("""SELECT riskval, COUNT(scriptid) AS count, 
              scriptid, msg1, msg2, service 
              FROM results GROUP BY scriptid HAVING riskval >= %s 
              ORDER BY riskval DESC, count DESC, scriptid DESC""", (risk))

    results = c.fetchall()
    return results


def write_csv(file,data):
    """Write to CSV file.

    Used with the -o option on the command line.
    
    """
    import csv
    if data:
        print """Writing""", file + """..."""
        writer = csv.writer(open(file,"wb"))
        writer.writerow(('Network', 'Host', 'Service', 'PluginID', 'Severity', 
                         'Risk Description', 'Risk Recommendation'))
        writer.writerows(data)
    else:
        print """Error occurred while processing: no data to write!"""


def main():
    """The main() function that contains our use cases."""
    if opt.infile and opt.database and opt.outfile:
        results, timestamps = parse_nbe(opt.infile)
        insert_nbe(results,timestamps,opt.database)
        write_csv(opt.outfile,results)
    elif opt.infile and opt.database:
        results, timestamps = parse_nbe(opt.infile)
        insert_nbe(results,timestamps,opt.database)
    elif opt.database and opt.outfile:
        if opt.count:
            results = count_nbe(opt.database,opt.risk)
        else:
            results = select_nbe(opt.database,opt.risk,opt.order,opt.sort)
        write_csv(opt.outfile,results)
    elif opt.infile and opt.outfile:
        results, timestamps = parse_nbe(opt.infile)
        write_csv(opt.outfile,results)
    else:
        print parser.error("You are missing arguments, see usage or help")


if __name__ == "__main__":
    from optparse import OptionParser, make_option
    option_list = [
        make_option("-d", "--database", dest="database", 
                    help="query results from specified MySQL database"),
        make_option("-f", "--file", dest="infile", 
                    help="input nbe file to parse"),
        make_option("-o", "--output-file", dest="outfile", 
                    help="output to CSV file"),
        make_option("-r", "--risk", type="choice", dest="risk", default="1", 
                    help="minimum risk criticality to query", 
                    choices=["1","2","3"]),
        make_option("--count", action="store_true", dest="count", 
                    help="output results by count"),
        make_option("--order", type="choice", dest="order", default="host", 
                    help="order database query by column", 
                    choices=["host","service","scriptid","riskval"]),
        make_option("--sort", type="choice", dest="sort", default="", 
                    help="sort results descending", choices=["","desc"])
    ]

    usage  = """usage: tissynbe.py [options] args
tissynbe.py -d database -f results.nbe
tissynbe.py -d database -o output.csv
tissynbe.py -d database -o output.csv --order scriptid --sort desc
tissynbe.py -d database -o output.csv --count
tissynbe.py -f results.nbe -o output.csv
tissynbe.py -f results.nbe -d database -o output.csv"""
    parser = OptionParser(usage,option_list=option_list)
    opt, args = parser.parse_args()
    main()

