#!/usr/bin/env python

# import nmap
import utils.nmap_wraper as nmap
from utils import general_utilities
from core.base.abstract_vector import base_vector


class nmap_banner(base_vector):
    result = []
    banner = general_utilities.generate_banner("nmap Banner Grabbing Script")
    header = ['target', 'port', 'protocol', 'state', 'service', 'product', 'hostname', 'banner']

    def prepare(self, target, vector_args):
        if "://" in target:
            target = general_utilities.get_domain(target)
            target = general_utilities.get_ip_by_host(target)

        self.target = target

    def execute(self):
        addr = self.target
        # nm = nmap.PortScanner()
        nm = nmap.NmapScanner()
        nm.scan(addr, arguments='-sV --script=banner')

        # self.result = nm._scan_result

        raw_results = nm[addr][1]
        for port in raw_results['ports']['port']:
            p_hostname = None
            p_product = None
            p_script = None
            p_result = []
            p_num = port['@portid']
            p_protocol = port['@protocol']
            p_service = port['service']['@name']

            p_state = port['state']['@state']
            # print 'script' in port
            if 'script' in port:
                p_script = port['script']['@output']
            if '@product' in port['service']:
                p_product = port['service']['@product']
            if '@hostname' in port['service']:
                p_hostname = port['service']['@hostname']

            p_result = [addr, p_num, p_protocol, p_state, p_service, p_product, p_hostname, p_script]
            self.result.append(p_result)

        # print self.result
