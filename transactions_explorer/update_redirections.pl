#!/usr/bin/env perl
use Modern::Perl;
use IO::All;
use Text::CSV;

use constant BASE_URL => 'https://www.gov.uk/performance/transactions-explorer';
my %DIRECTIONS = (
    'asc'  => 'ascending',
    'desc' => 'descending',
);
my %COLUMNS = (
    'body'                    => 'by-agency',
    'category'                => 'by-category',
    'costPerTransaction'      => 'by-cost-per-transaction',
    'datacoverage'            => 'by-data-coverage',
    'dept'                    => 'by-department',
    'digitaltakeup'           => 'by-digital-takeup',
    'mostRecentDigitalTakeUp' => 'by-digital-takeup',
    'mostRecentTotalCost'     => 'by-cost',
    'nameOfService'           => 'by-name',
    'totalcost'               => 'by-cost',
    'volume'                  => 'by-transactions-per-year',
);




my $csv = Text::CSV->new();
open my $input, '<:encoding(utf8)', 'redirections.csv'
    or die;

my $names = $csv->getline( $input );
die unless scalar @$names;

$csv->column_names( @$names );

my @rows;
while ( my $row = $csv->getline_hr($input) ) {
    my $old_url = $row->{'Old URL'};
    my $new_url = get_redirection($old_url);
    
    $row->{'New URL'} = $new_url
        if defined $new_url;
    
    say " ** $old_url"
        if $row->{'Status'} eq '301'
           and length $row->{'New URL'} == 0;
    
    push @rows, [
            $row->{'Old URL'},
            $row->{'New URL'},
            $row->{'Status'},
            $row->{'Suggested Link'},
            $row->{'Archive Link'},
        ];
}
close $input;

open my $output, '>:encoding(utf8)', 'redirections-updated.csv'
    or die;
print $output "Old URL,New URL,Status,Suggested Link,Archive Link\n";
foreach my $row ( @rows ) {
    $csv->print( $output, $row );
    print $output "\n";
}
exit;



sub get_redirection {
    my $old_url = shift;
    
    return
        unless $old_url =~ s{^http://transactionsexplorer.cabinetoffice.gov.uk}{};
    
    return BASE_URL . '/about-data'
        if $old_url eq '/aboutData';
    
    return get_service_details_redirection($old_url)
        if $old_url =~ m{^/serviceDetails/};
    return get_all_transactions_redirection($old_url)
        if $old_url =~ m{^/allservices};
    return get_high_volume_transactions_redirection($old_url)
        if $old_url =~ m{^/highVolumeTransactions};
    return get_department_redirection($old_url)
        if $old_url =~ m{^/department/};
    
    return;
}
sub get_high_volume_transactions_redirection {
    my $old_url = shift;
    
    return get_csv_redirection()
        if $old_url =~ s{format=csv}{};
    
    $old_url =~ s{/highVolumeTransactions}{};
    
    $old_url =~ s{orderBy=(\w+)}{};
    my $column = $1 // 'costPerTransaction';
    
    $old_url =~ s{direction=(\w+)}{};
    my $direction = $1 // 'desc';
    
    $old_url =~ s{format=csv}{};
    $old_url =~ s{[&?]}{}g;
    die $old_url if length $old_url;
    
    return sprintf '%s/high-volume-transactions/%s/%s',
                BASE_URL,
                $COLUMNS{$column},
                $DIRECTIONS{$direction};
}
sub get_all_transactions_redirection {
    my $old_url = shift;
    
    return get_csv_redirection()
        if $old_url =~ s{format=csv}{};
    
    $old_url =~ s{/allservices}{};
    
    $old_url =~ s{orderBy=(\w+)}{};
    my $column = $1 // 'costPerTransaction';
    
    $old_url =~ s{direction=(\w+)}{};
    my $direction = $1 // 'desc';
    
    $old_url =~ s{format=csv}{};
    $old_url =~ s{[&?]}{}g;
    die $old_url if length $old_url;
    
    return sprintf '%s/all-services/%s/%s',
                BASE_URL,
                $COLUMNS{$column},
                $DIRECTIONS{$direction};
}
sub get_department_redirection {
    my $old_url = shift;
    
    return get_csv_redirection()
        if $old_url =~ s{format=csv}{};
    
    $old_url =~ s{direction=(\w+)}{};
    my $direction = $1 // 'desc';
    
    $old_url =~ s{orderBy=(\w+)}{};
    my $column = $1 // 'costPerTransaction';
    
    $old_url =~ s{/department/([\w\-]+)}{};
    my $department = $1;
    
    $old_url =~ s{[&?]}{}g;
    die $old_url if length $old_url;
    
    return sprintf '%s/department/%s/%s/%s',
                BASE_URL,
                $department,
                $COLUMNS{$column},
                $DIRECTIONS{$direction};
}
sub get_service_details_redirection {
    my $old_url = shift;
    
    # correct serviceDetails URLs
    $old_url =~ s{/serviceDetails/}{/service-details/};
    $old_url =~ s{/hmrc-pay-as-you-earn-paye-}{/hmrc-pay-as-you-earn-paye};
    $old_url =~ s{/bis-apply-for-student-finance-full-time-study-}{/bis-apply-for-student-finance-full-time-study};
    $old_url =~ s{/bis-director-and-mortgage-detail-searches}{/bis-director-mortgage-detail-searches};
    $old_url =~ s{/bis-land-register-updates-including-transfers-of-ownership-}{/bis-land-register-updates-including-transfers-of-ownership};
    $old_url =~ s{/bis-learning-records-service-organisation-portal-provider-creates-manages-unique-learner-number-uln-}{/bis-learning-records-service-organisation-portal-provider-creates-manages-unique-learner-number-uln};
    $old_url =~ s{/bis-other-document-filing-filing-transactions-}{/bis-other-document-filing-filing-transactions};
    $old_url =~ s{/bis-search-of-the-index-map-land-registry-}{/bis-search-of-the-index-map-land-registry};
    $old_url =~ s{/bis-search-of-whole-land-registry-}{/bis-search-of-whole-land-registry};
    $old_url =~ s{/defra-cattle-tracing-system-cts-}{/defra-cattle-tracing-system-cts};
    $old_url =~ s{/defra-endemic-disease-surveillance-animals-tested-}{/defra-endemic-disease-surveillance-animals-tested};
    $old_url =~ s{/defra-single-payment-scheme-sps-claims-}{/defra-single-payment-scheme-sps-claims};
    $old_url =~ s{/dft-destruction-of-vehicles-certificates-and-notifications-}{/dft-destruction-of-vehicles-certificates-notifications};
    $old_url =~ s{/dft-lost-or-stolen-registration-certificate-v5-}{/dft-lost-or-stolen-registration-certificate-v5};
    $old_url =~ s{/dft-notifications-sent-via-electronic-service-delivery-for-abnormal-loads-esdal-}{/dft-notifications-sent-via-electronic-service-delivery-for-abnormal-loads-esdal};
    $old_url =~ s{/dft-statutory-off-road-notice-sorn-}{/dft-statutory-off-road-notice-sorn};
    $old_url =~ s{/dft-vehicle-excise-duty-vehicle-tax-}{/dft-vehicle-excise-duty-vehicle-tax};
    $old_url =~ s{/dwp-adviser-interventions-jobsearch-advice-}{/dwp-adviser-interventions-jobsearch-advice};
    $old_url =~ s{/dwp-employment-and-support-allowance-esa-new-claims}{/dwp-employment-support-allowance-esa-new-claims};
    $old_url =~ s{/dwp-incapacity-benefit-employment-and-support-allowance-esa-claims-maintained}{/dwp-incapacity-benefit-employment-support-allowance-esa-claims-maintained};
    $old_url =~ s{/dwp-jobsearch-reviews-signing-on-}{/dwp-jobsearch-reviews-signing-on};
    $old_url =~ s{/dwp-jobseeker-s-allowance-jsa-claims-maintained}{/dwp-jobseekers-allowance-jsa-claims-maintained};
    $old_url =~ s{/dwp-jobseeker-s-allowance-jsa-new-claims}{/dwp-jobseekers-allowance-jsa-new-claims};
    $old_url =~ s{/dwp-social-fund-grants-and-loans}{/dwp-social-fund-grants-loans};
    $old_url =~ s{/hmrc-construction-industry-scheme-cis-}{/hmrc-construction-industry-scheme-cis};
    $old_url =~ s{/hmrc-payments-made-banking-}{/hmrc-payments-made-banking};
    $old_url =~ s{/hmrc-payments-received-banking-}{/hmrc-payments-received-banking};
    $old_url =~ s{/hmrc-stamp-duty-land-tax-sdlt-}{/hmrc-stamp-duty-land-tax-sdlt};
    $old_url =~ s{/hmrc-stamp-duty-reserve-tax-sdrt-}{/hmrc-stamp-duty-reserve-tax-sdrt};
    $old_url =~ s{/home-office-ordering-certificates-births-adoptions-marriages-civil-partnerships-deaths-}{/home-office-ordering-certificates-births-adoptions-marriages-civil-partnerships-deaths};
    $old_url =~ s{/home-office-visa-applications-temporary-permanent-migration-}{/home-office-visa-applications-temporary-permanent-migration};
    
    return BASE_URL . $old_url;
}
sub get_csv_redirection {
    return BASE_URL . '/transaction-volumes.csv';
}
