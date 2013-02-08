#!/usr/bin/perl

# grab bugtraq and create csv
use Parse::Nessus::Plugin;
use Data::Dumper;

my @files = glob "/usr/lib/openvas/plugins/nvt/*.nasl";
foreach $f (@files) {   
    $plugin = Parse::Nessus::Plugin->new || undef;
    if(!$plugin) {
        die("It wasn't posible to initialize parser");
    }
    $plugin->parse_file($f);

    my $bugtraq = $plugin->bugtraq;
    if($bugtraq) {
        foreach my $bug (@{$bugtraq}) {
            print("NULL|".$plugin->id."|".$bug."\n");
        }
    }
}
