#!/usr/bin/perl

use Parse::Nessus::NBE;
use Data::Dumper;
my $scan = Parse::Nessus::XML->new('results.xml');
my @results = $scan->results;
foreach my $result(@results) {
    print Dumper($result);
}


#my $plugin  = $scan->plugin(10964); # Parse::Nessus::XML::Plugin object
#my $name    = $plugin->name;
