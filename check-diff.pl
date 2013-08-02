#!/usr/bin/env perl
use Modern::Perl;
use File::Basename;
use File::Next;
use IO::All;
use HTTP::Lite;

use constant BASE_URL => 'http://transactionsexplorer.cabinetoffice.gov.uk/serviceDetails/';
use constant CACHE_DIR => '/tmp/diff-cache/';

my $sources = File::Next::files('output/serviceDetails');

FILE:
while ( my $file = $sources->() ) {
    my $filename = basename $file, '.html';
    my $url      = BASE_URL . $filename;
    say "\n$url";
    
    my $cached_original = CACHE_DIR . $filename;
    if ( ! -f $cached_original ) {
        my $http = HTTP::Lite->new();
        my $req  = $http->request($url);
        
        if ( $req != 200 ) {
            warn "** $req $url";
            next FILE;
        }
        
        $http->body() > io $cached_original;
    }
    
    my $original = diffable( io($cached_original)->all() );
    my $generated = diffable( io($file)->all() );
    
    $original  > io(CACHE_DIR . 'original.html');
    $generated > io(CACHE_DIR . 'generated.html');
    system 'diff', '-U15', (CACHE_DIR . 'original.html'), 
                          (CACHE_DIR . 'generated.html');
    # last;
}

sub diffable {
    my $text = shift;
    
    $text =~ s{^\s*(.*?)\s*$}{$1}gm;
    $text =~ s{>\s*<}{>\n<}gs;
    $text =~ s{\&pound;}{£}gs;
    $text =~ s{class="(.*?)\s+"}{class="$1"}gs;
    
    return $text;
}