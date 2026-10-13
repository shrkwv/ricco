#!/usr/bin/env python3

import urllib.error
import urllib.request

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
                response = urllib.request.urlopen(uri, timeout=3)
                if response:
                    self.result.append((uri, str(response.getcode())))

            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    self.result.append((uri, e.code))
            except urllib.error.URLError:
                pass
