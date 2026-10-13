#!/usr/bin/env python3

import re

from utils import general_utilities, whois_utilities
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
            self.result = whois_utilities.get_whois_raw(domain)
        except whois_utilities.WhoisError:
            self.result = "Domain Not Found"

            # def output(self):
            #
            #     banner = general_utilities.generate_banner("Domain Whois Info")
            #     header = []
            #
            #     return banner, self.result, header
