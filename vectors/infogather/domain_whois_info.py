#!/usr/bin/env python

import re

import pythonwhois

from utils import general_utilities
from core.base.abstract_vector import base_vector


class domain_whois_info(base_vector):
    result = []
    banner = general_utilities.generate_banner("Domain Whois Info")
    header = []

    def prepare(self, target, vector_args):
        if "://" in target:
            target = general_utilities.get_domain(target)
        elif re.match(r"[0-9\.]", target):
            target = general_utilities.get_host_by_ip(target)

        self.target = target

    def execute(self):
        domain = self.target
        try:
            whois_data = pythonwhois.get_whois(domain)
            # TODO parse result
            assert whois_data.has_key("raw")
            whois_data = str(whois_data["raw"][0])
            self.result = whois_data
        except pythonwhois.shared.WhoisException:
            self.result = "Domain Not Found"

            # def output(self):
            #
            #     banner = general_utilities.generate_banner("Domain Whois Info")
            #     header = []
            #
            #     return banner, self.result, header
