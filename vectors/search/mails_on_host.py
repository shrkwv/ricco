#!/usr/bin/env python

from utils import general_utilities, search_utilities
from core.base.abstract_vector import base_vector
import utils.scraper as scraper


class mails_on_host(base_vector):
    result = []
    banner = general_utilities.generate_banner("Extract mails in domain from google search")
    header = ['url', 'email']

    def prepare(self, target, vector_args):
        # if "://" in target:
        #     target = general_utilities.get_domain(target)
        #     target = general_utilities.get_ip_by_host(target)

        self.target = target

    def execute(self):
        query = "intext:@" + self.target
        if  self.ricco_conf.has_option('ApiKeys','Google'):
            api_key = self.ricco_conf.get('ApiKeys','Google')
        else:
            api_key = None
        search = search_utilities.Google(pages=2,api_key=api_key)

        search.search(query)
        # self.result =  search.get_results()
        links = search.get_links_result()

        result_for_links = []
        for link in links:
            data, e = general_utilities.get_page(link)
            if data:
                emails = scraper.get_emails(data)
            if emails:
                for email in emails:
                    if self.target in email:
                        result_for_links.append([link, email])

        self.result = result_for_links
