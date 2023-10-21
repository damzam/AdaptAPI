"""
A spider to scrape the moderately messy carrier data which spans multiple pages
and log the data extracted from each page to the console.
"""
import json
import logging
import re
from urllib.parse import urlparse

import scrapy
from scrapy_splash import SplashRequest 

SEED_URL = 'https://scraping-interview.onrender.com/placeholder_carrier/f02dkl4e/policies/1'
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class MockCarrierSpider(scrapy.Spider):
    name = 'mock_carrier'

    def __init__(self, domain=None, *args, **kwargs):
        self.url = domain + '/policies/1'  # the seed url also includes /policies/1
        self.carrier_data = {}
        self.policies = []

    def start_requests(self):
        yield SplashRequest(self.url,
                            callback=self.parse,
                            args={'wait': 0.5})  # wait until dynamic content renders

    def parse(self, response):

        # Agent details data is cleanly formatted
        agent_keys = response.css('.agency-details label::attr(for)').getall()
        agent_vals = response.css('.agency-details span::text').getall()
        key_translations = {  # Snake case for Python (I have no religious ideology on case)
            'name': 'name',   # ...this is nice to use for validation given that we have "for" attrs
            'producer_code': 'producerCode',
            'agency_name': 'agencyName',
            'agency_code': 'agencyCode'
        }
        js_formatted_dict = dict(zip(agent_keys, agent_vals))  # Perform a matrix transformation to create dict
        self.carrier_data['agent_details'] = {k: js_formatted_dict[v] for (k, v) in key_translations.items()}
        
        # Customer details data is *not* as consistently formatted as agent details, but let's try to get it!
        customer = {}
        for i, key in enumerate(['name', 'id', 'ssn']):  # SSN is hidden, but let's capture it!
            customer[key] = response.css('.customer-details span::text').getall()[i]
        try:  # The email isn't part of the document tree, but we can still capture it.
            customer['email'] = re.findall(EMAIL_REGEX, response.css('.customer-details div').get())[0]
        except IndexError:  # Don't crash if the email is invalid!
            customer['email'] = None
        customer['address'] = response.css('.customer-details div::text').getall()[-1].replace('Address: ', '')
        self.carrier_data['customer_details'] = customer

        # Now get data for policies
        policies = []
        for policy in response.css('.policy-info-row'):
            keys = ['id', 'premium', 'status', 'effective_date', 'termination_date']
            table_data_rows = policy.css('td::text').getall()
            policies.append(dict(zip(keys, table_data_rows)))
        # get policy details too...
        details_rows = response.css('.details-row div').getall()
        for i, details in enumerate(details_rows):
            details_item = {}
            try:  # This isn't ideal, but let's use regular expressions to capture errant data
                details_item['last_payment_date'] = re.findall(r'\d+/\d+/\d+', details)[0]
                details_item['commission_rate'] = re.findall(r'\d+%', details)[0]
                details_item['number_of_insureds'] = re.findall(r'Insureds: (\d+)', details)[0]
            except IndexError:  # Note, if one of these is missing, none will be captured
                pass
            policies[i]['details'] = details_item

        self.policies.extend(policies)

        # Let's check to see if there are more pages to scrape :)
        next_page_url = None
        for a in response.css('a'):
            if a.css('::text').get() == 'Next >':  # If "Next >" is actually a link...
                href = a.css('::attr(href)').get()
                next_page_url = urlparse(SEED_URL)._replace(path=href).geturl()

        if next_page_url:  # If there's more work to do, let's keep the party going!
            yield scrapy.Request(next_page_url, self.parse)
        else:  # we're finished!
            self.carrier_data['policies'] = self.policies
            logging.info('Logging output for PLACEHOLDER_CARRIER:')
            logging.info(json.dumps(self.carrier_data, indent=4))
        
