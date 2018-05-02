#!/usr/bin/env python
import socket

from  core.base.abstract_vector import base_vector
from utils import general_utilities, validators


class suffixes_fuzzing(base_vector):
    result = []
    banner = general_utilities.generate_banner("Available Suffixes for Domain")
    header = ["host"]

    def prepare(self, target, vector_args=None):

        if "://" in target:
            target = general_utilities.get_domain()
        elif validators.is_ipv4(target):
            target = general_utilities.get_host_by_ip(target)

        self.target = target
        suffixes_list= self.base_path +  "/static-data/suffixes.txt"
        with open(suffixes_list, 'r') as f:
            suffixes = f.read()
            self.suffixes = suffixes.split("\n")
        self.target = general_utilities.get_domain_without_suffix(target, suffixes=suffixes_list)

    def execute(self):

        url = str(self.target)

        counter = 0
        for suffix in self.suffixes:

            uri = url + "." + suffix
            counter += 1
            if counter > 3:
                break
            try:
                socket.gethostbyname(uri)
                uri_result = []
                uri_result.append(uri.lower())
                self.result.append(uri_result)
            except socket.error, e:
                pass

                # def output(self):
                #
                #
                #     banner = general_utilities.generate_banner("Available Suffixes for Domain")
                #     header = ["host"]
                #     return banner, self.result, header
