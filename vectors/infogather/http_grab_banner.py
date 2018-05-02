#!/usr/bin/env python
import socket

from core.base.abstract_vector import base_vector
from utils import general_utilities


class http_grab_banner(base_vector):
    result = []
    banner = general_utilities.generate_banner("Banner Grabbing")
    header = ["Port", "target"]

    def prepare(self, target, vector_args):
        if "://" in target:
            target = general_utilities.get_domain(target)
        self.target = target

    def execute(self):
        host = self.target
        ports = [80, 443]
        http_versions = ["1.0", "1.1", "0.9"]
        CRLF = "\r\n\r\n"
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((host, port))
                s.send("GET / HTTP/1.0%s" % (CRLF))
                grabbed_banner = s.recv(1024)
                # print grabbed_banner
                self.result.append([port, str(grabbed_banner)])
            except:

                continue

                # def output(self):
                #
                #
                #
                #     banner = general_utilities.generate_banner("Banner Grabbing")
                #     header = ["Port","target"]
                #
                #     return banner, self.result, header
