#!/usr/bin/env python

import urllib2

from core.base.abstract_vector import base_vector
from utils import general_utilities


class dirs_fuzzing(base_vector):
    result = []
    banner = general_utilities.generate_banner("Avialable Dirs on Server")
    header = ["url", "http-code"]

    def prepare(self, target, vector_args=None):
        self.target = target
        if "://" not in target:
            target = "http://" + target
            self.target = target
        self.dirs_list = self.base_path + "/static-data/dirs-list.txt"

    def execute(self):
        url = str(self.target)
        with open(self.dirs_list, 'r') as f:
            wordlist = f.read()
            wordlist = wordlist.split("\n")
        counter = 0
        if url.endswith("/"):
            url = url[:-1]

        for word in wordlist:

            uri = url + "/" + word

            counter += 1
            # if counter > 3:
            #     break
            try:
                response = urllib2.urlopen(uri, timeout=3)
                if response:
                    self.result.append((uri, str(response.getcode())))

            except urllib2.HTTPError, e:
                if e.code == 401:
                    self.result.append((uri, e.code))
                elif e.code == 403:
                    self.result.append((uri, e.code))
            except urllib2.URLError, e:
                pass
