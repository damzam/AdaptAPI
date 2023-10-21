"""
A simple spider to collect indemnity data consisting of the agent,
the customer, and the policies.
"""
import json
import logging

import scrapy
from scrapy_splash import SplashRequest 


class MockIndemnitySpider(scrapy.Spider):
    name = 'mock_indemnity'

    def __init__(self, domain=None, *args, **kwargs):
        self.url = domain

    def start_requests(self):
        yield SplashRequest(self.url,
                            callback=self.parse,
                            args={'wait': 0.5})  # wait until dynamic content renders

    def parse(self, response):

        indemnity_data = {
            'agent': {
                'name': response.css('.agent-detail .value-name::text').get(),
                'producer_code': response.css('.agent-detail .value-producerCode::text').get(),
                'agency_name': response.css('.agent-detail .value-agencyName::text').get(),
                'agency_code': response.css('.agent-detail .value-agencyCode::text').get()
            },
            'customer': {
                'name': response.css('.customer-detail .value-name::text').get(),
                'id': response.css('.customer-detail .value-id::text').get(),
                'email': response.css('.customer-detail .value-email::text').get(),
                'address': response.css('.customer-detail .value-address::text').get()
            },
            'policies': []
        }

        for policy in response.css('.policy-ul .container'):
            policy_item = {}
            policy_item['id'] = policy.css('.id::text').get()
            policy_item['premium'] = policy.css('.premium::text').get()
            policy_item['status'] = policy.css('.status::text').get()
            policy_item['effective_date'] = policy.css('.effectiveDate::text').get()
            policy_item['termination_date'] = policy.css('.terminationDate::text').get()
            policy_item['last_payment_date'] = policy.css('.lastPaymentDate::text').get()

            indemnity_data['policies'].append(policy_item)

        logging.info('Logging output for MOCK_INDEMNITY:')
        logging.info(json.dumps(indemnity_data, indent=4))
        yield