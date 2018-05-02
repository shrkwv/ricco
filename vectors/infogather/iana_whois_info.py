#!/usr/bin/env python
from utils import general_utilities

from core.base.abstract_vector import base_vector


class iana_whois_info(base_vector):
    result = []
    banner = general_utilities.generate_banner("IANA Whois Info")
    header = ["category", "info"]

    def prepare(self, target, vector_args):
        self.target = None
        if "://" in target:
            self.target = general_utilities.get_domain(target)
            self.target = general_utilities.get_domain_without_suffix(target)

        else:
            self.target = general_utilities.get_domain_without_suffix(target)
        self.iana_base_url = "http://www.iana.org/whois?"

    def execute(self):
        url = self.iana_base_url
        params = {"q": self.target}
        raw_iana, err = general_utilities.get_page(url, params)
        # TODO err
        raw_iana = raw_iana.split("<pre>")[1]
        raw_iana = raw_iana.split("</pre>")[0]
        self.result = raw_iana.split("\n\n",1)[1]
        # def output(self):
        #
        #     banner = general_utilities.generate_banner("IANA Whois Info")
        #     header = []
        #
        #
        #     return banner, self.result, header
