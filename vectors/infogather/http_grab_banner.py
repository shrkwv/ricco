#!/usr/bin/env python3
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
        CRLF = "\r\n\r\n"
        for port in ports:
            try:
                with socket.create_connection((host, port), timeout=1) as s:
                    s.sendall(("GET / HTTP/1.0%s" % (CRLF)).encode("ascii"))
                    grabbed_banner = s.recv(1024).decode("utf-8", errors="replace")
                    self.result.append([port, grabbed_banner])
            except OSError:

                continue

                # def output(self):
                #
                #
                #
                #     banner = general_utilities.generate_banner("Banner Grabbing")
                #     header = ["Port","target"]
                #
                #     return banner, self.result, header
