import unittest

from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest
from test.features.support.splinter_matchers import has_text, has_class


class test_search(BrowserTest):

    def test_search_page(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        assert_that(self.browser.find_by_css('#wrapper h1').text,
                    is_('Search results'))

        assert_that(self.browser.find_by_css('tbody tr'), has_length(7))

    def test_default_sorting(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        assert_that(self.browser.find_by_css('.sorted'), has_text('Transactions per year'))
        assert_that(self.browser.find_by_css('.sorted'), has_class('descending'))

    def test_sorting_search_results_by_transactional_service(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        self.browser.click_link_by_text('Transactional service')

        assert_that(self.browser.find_by_css('.sorted'), has_text('Transactional service'))
        assert_that(self.browser.find_by_css('.sorted'), has_class('ascending'))

    def test_sorting_search_results_by_category(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        self.browser.click_link_by_text('Category')

        assert_that(self.browser.find_by_css('.sorted'), has_text('Category'))
        assert_that(self.browser.find_by_css('.sorted'), has_class('ascending'))

    def test_sorting_search_results_by_agency(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        self.browser.click_link_by_text('Agency / body')

        assert_that(self.browser.find_by_css('.sorted'), has_text('Agency / body'))
        assert_that(self.browser.find_by_css('.sorted'), has_class('ascending'))

    def test_sorting_twice_the_same_column_reverses_the_order(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        self.browser.click_link_by_text('Transactional service')
        self.browser.click_link_by_text('Transactional service')

        assert_that(self.browser.find_by_css('.sorted'), has_text('Transactional service'))
        assert_that(self.browser.find_by_css('.sorted'), has_class('descending'))

    def test_default_order_is_ascending_after_changing_column(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        self.browser.click_link_by_text('Transactional service')
        self.browser.click_link_by_text('Category')

        assert_that(self.browser.find_by_css('.sorted'), has_text('Category'))
        assert_that(self.browser.find_by_css('.sorted'), has_class('ascending'))

    def test_default_volume_order_is_descending(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        self.browser.click_link_by_text('Transactional service')
        self.browser.click_link_by_text('Transactions per year')

        assert_that(self.browser.find_by_css('.sorted'), has_text('Transactions per year'))
        assert_that(self.browser.find_by_css('.sorted'), has_class('descending'))

    def test_link_column_is_not_sortable(self):
        self.browser.visit("http://0.0.0.0:8000/search?keyword=gds")

        assert_that(self.browser.find_by_xpath('//th[text()="Web link"]'), has_length(greater_than(0)))
        assert_that(self.browser.find_link_by_text("Web link"), has_length(0))
