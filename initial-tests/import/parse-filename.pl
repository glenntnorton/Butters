#!/usr/bin/perl

# grab filename and create csv
use Parse::Nessus::Plugin;

my @files = glob "/usr/lib/openvas/plugins/nvt/*.nasl";
foreach $f (@files) {   
    $plugin = Parse::Nessus::Plugin->new || undef;
    if(!$plugin) {
        die("It wasn't posible to initialize parser");
    }
    $plugin->parse_file($f);

    print("NULL|".$plugin->id."|".$plugin->filename."\n");
}
