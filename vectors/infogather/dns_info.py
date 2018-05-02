# !/usr/bin/env python
from utils import general_utilities

import utils.dns_utilities as dns_utilities
from core.base.abstract_vector import base_vector


class dns_info(base_vector):
    result = []
    banner = general_utilities.generate_banner("Dns Information")
    header = ["Type", "Host"]

    def prepare(self, target, vector_args=None):
        if "://" in target:
            target = general_utilities.get_domain(target)
        self.target = target

    def execute(self):
        host = self.target
        MX_records = dns_utilities.get_MX_records(host)
        # mx_result = tabulate(MX_records,headers=header)
        NS_records = dns_utilities.get_NS_records(host)
        # ns_result = tabulate(NS_records, headers=header)
        A_records = dns_utilities.get_A_records(host)
        AAAA_records = dns_utilities.get_AAAA_records(host)
        # alias_result = tabulate(alias_records,headers=header)

        # result = mx_result+ns_result+alias_result
        if A_records:
            self.result += [(item[0],item[1].address) for item in A_records]
        if AAAA_records:
            self.result += [(item[0],item[1].address) for item in AAAA_records]
        if MX_records:
            self.result += [(item[0],item[1].address) for item in MX_records]
        if NS_records:
            self.result += [(item[0],item[1].address) for item in NS_records]

            # def output(self):
            #
            #     banner = general_utilities.generate_banner("Dns Information")
            #     header = ["Type", "Host"]
            #
            #     return banner, self.result, header
