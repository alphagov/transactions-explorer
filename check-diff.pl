#!/usr/bin/env perl
use Modern::Perl;
use Capture::Tiny   qw( capture_stdout );
use File::Basename;
use File::Next;
use File::Path  qw( mkpath );
use IO::All;
use HTTP::Lite;

use constant BASE_URL => 'http://transactionsexplorer.cabinetoffice.gov.uk/';
use constant CACHE_DIR => '/tmp/diff-cache/';

mkpath CACHE_DIR;

my $sources = File::Next::files('output/service-details');


diff_service_details_pages();
diff_page( 'aboutData', 'output/about-the-data.html');


sub diff_page {
    my $url  = BASE_URL . shift;
    my $file = shift;
    
    my $filename = basename $file;
    
    my $cached_original = CACHE_DIR . $filename;
    if ( ! -f $cached_original ) {
        my $http = HTTP::Lite->new();
        my $req  = $http->request($url);
        
        if ( $req != 200 ) {
            warn "** $req $url";
            return;
        }
        
        $http->body() > io $cached_original;
    }
    
    my $original = diffable_html( io($cached_original)->all() );
    my $generated = diffable_html( io($file)->all() );

    $original  > io(CACHE_DIR . 'original.html');
    $generated > io(CACHE_DIR . 'generated.html');
    
    my $diff = capture_stdout {
            system 'diff', '-U2', (CACHE_DIR . 'original.html'), 
                                  (CACHE_DIR . 'generated.html');
        };
    
    say "$url\n$diff"
        if length $diff;
}
sub diff_service_details_pages {
    FILE:
    while ( my $file = $sources->() ) {
        my $filename = basename $file, '.html';
        next FILE if $filename =~ m{^\.};
        
        my $url_file = $file;
        $url_file =~ s{^output}{};
        
        my $url = correct_special_cases( $url_file );
        
        # say " ** $url_file";
        # say "    $url";
        diff_page( $url, $file );
    }
}
sub diffable_html {
    my $text = shift;
    
    $text =~ s{\s+}{ }gs;
    $text =~ s{^\s*(.*?)\s*$}{$1}gm;
    $text =~ s{>\s*<}{>\n<}gs;
    $text =~ s{\&pound;}{£}gs;
    $text =~ s{class="(.*?)\s+"}{class="$1"}gs;
    
    return $text;
}
sub correct_special_cases {
    my $url = shift;
    
    $url =~ s{.html$}{};
    $url =~ s{/service-details/}{/serviceDetails/};
    $url =~ s{hmrc-pay-as-you-earn-paye}{hmrc-pay-as-you-earn-paye-};
    $url =~ s{bis-apply-for-student-finance-full-time-study}{bis-apply-for-student-finance-full-time-study-};
    $url =~ s{bis-director-mortgage-detail-searches}{bis-director-and-mortgage-detail-searches};
    $url =~ s{bis-land-register-updates-including-transfers-of-ownership}{bis-land-register-updates-including-transfers-of-ownership-};
    $url =~ s{bis-learning-records-service-organisation-portal-provider-creates-manages-unique-learner-number-uln}{bis-learning-records-service-organisation-portal-provider-creates-manages-unique-learner-number-uln-};
    $url =~ s{bis-other-document-filing-filing-transactions}{bis-other-document-filing-filing-transactions-};
    $url =~ s{bis-search-of-the-index-map-land-registry}{bis-search-of-the-index-map-land-registry-};
    $url =~ s{bis-search-of-whole-land-registry}{bis-search-of-whole-land-registry-};
    $url =~ s{defra-cattle-tracing-system-cts}{defra-cattle-tracing-system-cts-};
    $url =~ s{defra-endemic-disease-surveillance-animals-tested}{defra-endemic-disease-surveillance-animals-tested-};
    $url =~ s{defra-single-payment-scheme-sps-claims}{defra-single-payment-scheme-sps-claims-};
    $url =~ s{dft-destruction-of-vehicles-certificates-notifications}{dft-destruction-of-vehicles-certificates-and-notifications-};
    $url =~ s{dft-lost-or-stolen-registration-certificate-v5}{dft-lost-or-stolen-registration-certificate-v5-};
    $url =~ s{dft-notifications-sent-via-electronic-service-delivery-for-abnormal-loads-esdal}{dft-notifications-sent-via-electronic-service-delivery-for-abnormal-loads-esdal-};
    $url =~ s{dft-statutory-off-road-notice-sorn}{dft-statutory-off-road-notice-sorn-};
    $url =~ s{dft-vehicle-excise-duty-vehicle-tax}{dft-vehicle-excise-duty-vehicle-tax-};
    $url =~ s{dwp-adviser-interventions-jobsearch-advice}{dwp-adviser-interventions-jobsearch-advice-};
    $url =~ s{dwp-employment-support-allowance-esa-new-claims}{dwp-employment-and-support-allowance-esa-new-claims};
    $url =~ s{dwp-incapacity-benefit-employment-support-allowance-esa-claims-maintained}{dwp-incapacity-benefit-employment-and-support-allowance-esa-claims-maintained};
    $url =~ s{dwp-jobsearch-reviews-signing-on}{dwp-jobsearch-reviews-signing-on-};
    $url =~ s{dwp-jobseekers-allowance-jsa-claims-maintained}{dwp-jobseeker-s-allowance-jsa-claims-maintained};
    $url =~ s{dwp-jobseekers-allowance-jsa-new-claims}{dwp-jobseeker-s-allowance-jsa-new-claims};
    $url =~ s{dwp-social-fund-grants-loans}{dwp-social-fund-grants-and-loans};
    $url =~ s{hmrc-construction-industry-scheme-cis}{hmrc-construction-industry-scheme-cis-};
    $url =~ s{hmrc-payments-made-banking}{hmrc-payments-made-banking-};
    $url =~ s{hmrc-payments-received-banking}{hmrc-payments-received-banking-};
    $url =~ s{hmrc-stamp-duty-land-tax-sdlt}{hmrc-stamp-duty-land-tax-sdlt-};
    $url =~ s{hmrc-stamp-duty-reserve-tax-sdrt}{hmrc-stamp-duty-reserve-tax-sdrt-};
    $url =~ s{home-office-ordering-certificates-births-adoptions-marriages-civil-partnerships-deaths}{home-office-ordering-certificates-births-adoptions-marriages-civil-partnerships-deaths-};
    $url =~ s{home-office-visa-applications-temporary-permanent-migration}{home-office-visa-applications-temporary-permanent-migration-};
    
    return $url;
}