#!/usr/bin/env python

from utils import general_utilities, search_utilities
from core.base.abstract_vector import base_vector
import utils.scraper as scraper


class location_info(base_vector):
    result = []
    banner = general_utilities.generate_banner("Get Coordinates From address")
    header = ['lat', 'lng', 'formatted_address']

    def prepare(self, target, vector_args):
        self.target = target

    def execute(self):
        query = self.target
        if  self.ricco_conf.has_option('ApiKeys','Google'):
            api_key = self.ricco_conf.get('ApiKeys','Google')
        else:
            api_key = None
        search = search_utilities.Google(api_key=api_key)
        search.fetch_geocoding(query)
        geocoding = search.get_geocoding()
        status = geocoding["status"]
        results = geocoding["results"]
        if status == "OK":
            for res in results:
                values = res.values()
                self.result.append(values)
        else:
            self.result = None
