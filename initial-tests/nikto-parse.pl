#!/usr/bin/perl

use Nikto::Parser;

my $npx = new Nikto::Parser;
my $parser = $npx->parse_file("/tmp/results.xml");

foreach my $h ( $parser->get_all_hosts() ) {
    print "IP: " . $h->ip . "\n";
    foreach my $p ( $h->get_all_ports() ) {
        print "Port: " . $p->port . "\n";
        print "Banner: " . $p->banner . "\n";
        print "Description:\n";
        foreach my $i ( $p->get_all_items() ) {
            print "\t" . $i->description . "\n";
        }
    }   
    print "---\n";
}   
