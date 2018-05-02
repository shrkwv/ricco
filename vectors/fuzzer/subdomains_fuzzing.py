#!/usr/bin/env python
import socket

from  core.base.abstract_vector import base_vector
from utils import general_utilities


class subdomains_fuzzing(base_vector):
    result = []
    banner = general_utilities.generate_banner("Available Sub-Domains")
    header = ["host"]

    def prepare(self, target, vector_args=None):

        if "://" in target:
            target = target.split("://")[1]
        self.target = target
        self.hosts_list =self.base_path + "/static-data/hosts-list.txt"

    def execute(self):
        url = str(self.target)
        with open(self.hosts_list, 'r') as f:
            wordlist = f.read()
            wordlist = wordlist.split("\n")
        counter = 0

        if url.endswith("/"):
            url = url[:-1]
        if "://" in url:
            url = url.split("://")[1]

        for word in wordlist:

            uri = word + "." + url
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
                #     banner = general_utilities.generate_banner("Available Sub-Domains")
                #     header = ["host"]
                #     return banner, self.result, header
