#!/usr/bin/env python
import json
from pprint import pprint
import importlib

import concurrent.futures

from concurrent.futures import Future
from utils.tabulate import tabulate
from utils import general_utilities


class ricco_manager(object):
    result = []
    banner = []
    header = []

    def __init__(self, target, strategy=None, vector=None, strategy_args=None, vector_args=None, strategies_conf=None,
                 vectors_conf=None, output_format=None):
        self.target = target
        self.strategy = strategy
        self.strategy_args = strategy_args
        self.vector = vector
        self.vector_args = vector_args
        self.vectors_conf = vectors_conf
        self.strategies_conf = strategies_conf
        self.output_format = output_format

    def prepare_vectors_list(self):

        vectors_instances = []
        if self.strategy:
            vectors_list = self.strategies_conf[self.strategy]["vectors"]
        elif self.vector:
            vectors_list = [self.vector]

        # create vectors.json instance
        import_base_path = "vectors"
        for v in vectors_list:
            module_name = [import_base_path]

            module_name.append(str(self.vectors_conf[v]["group"]))
            module_name.append(v)
            package = '.'.join(module_name)
            module = importlib.import_module(package)
            class_ = getattr(module, v)
            v_instance = class_()
            vectors_instances.append(v_instance)
        return vectors_instances

    def process(self, vectors_instances):
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            tmp_futures = []
            for vector in vectors_instances:
                cur_future = executor.submit(vector.prepare, self.target, self.vector_args)
                tmp_futures.append(cur_future)
            concurrent.futures.wait(tmp_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)

            tmp_futures = []
            for vector in vectors_instances:
                cur_future = executor.submit(vector.execute)
                tmp_futures.append(cur_future)
            concurrent.futures.wait(tmp_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)

            tmp_futures = []
            for vector in vectors_instances:
                cur_future = executor.submit(vector.output)
                tmp_futures.append(cur_future)

            concurrent.futures.wait(tmp_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
            # strategy_results = {}


            # for cur_future in tmp_futures:
            #     try:
            #         class_name, vector_results = cur_future.result()
            #         strategy_results[class_name] = vector_results
            #     except Exception as exc:
            #         sys.stderr.write('%r generated an exception: %s' % (class_name, exc))
            #
            # self.print_output(strategy_results,self.output_format)
            strategy_results = []
            for cur_future in tmp_futures:
                vector_result = cur_future.result()
                strategy_results.append(vector_result)
            self.print_output(strategy_results, self.output_format)

    def print_output(self, strategy_results, output_format=None):

        if output_format is None:
            for vector_result in strategy_results:

                vector_name = vector_result.class_name
                header = vector_result.header
                banner = vector_result.banner
                output = vector_result.output
                if output:

                    print banner

                    if all(isinstance(i, list) for i in output) or all(isinstance(i, tuple) for i in output):
                        print tabulate(output, headers=header)
                    elif isinstance(output, str):
                        print "\n"
                        print output
                        print "\n"
                    else:
                        pprint(output)
                else:
                    print banner
                    print "No results Found."

        elif output_format is 'json':
            json_result = {}

            for vector_result in strategy_results:
                vector_name = vector_result.class_name
                header = vector_result.header
                output = vector_result.output
                if output and header:
                    cur_dict = {}

                    cur_json = general_utilities.list_and_headers_to_json(header, output)
                    cur_dict[vector_name] = cur_json
                    json_result.update(cur_dict)

            if json_result:
                json_result = json.dumps(json_result)
            else:
                json_result = {"result":[{"status":"No Results"}]}
                json_result = json.dumps(json_result)

            print json_result

        elif output_format is 'xml':
            # TODO
            pass
