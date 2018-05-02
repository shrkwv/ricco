#!/usr/bin/env python

import re

from ipwhois import IPWhois

from utils import general_utilities
from core.base.abstract_vector import base_vector


class ip_whois_info(base_vector):
    result = []
    banner = general_utilities.generate_banner("IP Whois Info")
    header = []

    def prepare(self, target, vector_args):
        if "://" in target:
            target = general_utilities.get_domain(target)
            target = general_utilities.get_ip_by_host(target)
        elif re.match(r"[^0-9\.]", target):
            target = general_utilities.get_ip_by_host(target)

        self.target = target

    def execute(self):
        addr = self.target
        obj = IPWhois(addr)
        self.result = obj.lookup_rws()
        print self.result
        # def output(self):
        #
        #     banner = general_utilities.generate_banner("IP Whois Info")
        #     header = []
        #
        #     return banner, self.result, header
