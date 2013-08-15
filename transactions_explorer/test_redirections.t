my $test = TxEx->new();
$test->input_file("redirections-updated.csv");
$test->output_file("redirections-checked.csv");
$test->output_error_file("redirections-errors.csv");
$test->run_tests();
exit;


package TxEx;
use base 'IntegrationTest';

use v5.10;
use strict;
use warnings;
use Test::More;


sub test {
    my $self = shift;
    
    my ( $passed, $response, $test_response ) = $self->is_redirect_response(@_);
    
    if ( -1 == $passed ) {
        ( $passed, $response, $test_response ) = $self->is_gone_response(@_);
        if ( -1 == $passed ) {
            ( $passed, $response, $test_response ) = $self->is_ok_response(@_);
        }
    }
    
    return ( 
        $passed, 
        $response, 
        $test_response 
    );
}