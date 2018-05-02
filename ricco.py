#!/usr/bin/env python
import os
import sys
import argparse

from core.ricco_manger import ricco_manager
from utils import general_utilities
from utils.tabulate import tabulate


def argparser():
    parser = argparse.ArgumentParser(description="Recon tool to gather informatation about target",
                                     argument_default=None)

    # mandatory
    parser.add_argument("--target", type=str, help="Target - domain, company, host, ip")
    parser.add_argument("--strategy", type=str,
                        help="Attack strategy - domain_recon, company_passive_info...[--show-strategies to see all options]")
    parser.add_argument("--vector", type=str,
                        help="Attack Vector - dns_info, suffixes_fuzzing... [--show-vectors.json to see all options]")


    # optional
    # parser.add_argument("--strategy-args", dest="strategy_args", type=str, nargs='+', help="Arguments for strategy")
    parser.add_argument("--vector-args", dest="vector_args", type=str, nargs='+', help="Arguments for vector")

    parser.add_argument("--output-json", action='store_const', dest='output', const='json',
                        help="Output results as json")
    # parser.add_argument("--output-xml", action='store_const', dest='output', const='xml', help="Output results as xml")
    # parser.add_argument("--output-html", action='store_const', dest='output', const='html',
    #                     help="Output results as html")
    # parser.add_argument("--output-report", action='store_const', dest='output', const='report',
    #                     help="Output results as report")

    parser.add_argument("--help-vector", nargs='+', dest='help_vector', help="help about specific vector")
    parser.add_argument("--help-strategy", nargs='+', dest='help_strategy', help="help about specific vector")

    parser.add_argument("--show-vectors", action='store_const', dest='show', const='vectors',
                        help="Show all available vectors.json")
    parser.add_argument("--show-strategies", action='store_const', dest='show', const='strategies',
                        help="Show all available strategies")
    args = vars(parser.parse_args())

    return args, parser


def main():
    args, parser = argparser()
    # if not args["target"] is None:
    #     target = ' '.join(args["target"])
    target = args["target"]
    strategy = args["strategy"]
    vector = args["vector"]
    # startegy_args = args["strategy_args"]
    vector_args = args["vector_args"]
    output_format = args["output"]
    show = args["show"]
    help_vector = args["help_vector"]
    help_strategy = args["help_strategy"]



    # const
    base_dir = os.path.dirname(os.path.realpath(__file__))
    vectors_file = base_dir + "/core/vectors.json"
    strategies_file = base_dir + "/core/strategies.json"
    # show!

    if show:
        if show == "vectors":
            vectors_conf, err = general_utilities.load_json(vectors_file)

            vectors_names = vectors_conf.keys()
            header = ["Vector", "Description", "Arguments"]
            data = []
            for vector_name in vectors_names:
                args = ', '.join(vectors_conf[vector_name]["args"])
                data.append([vector_name,vectors_conf[vector_name]["description"],args])

            print tabulate(data, headers=header, tablefmt="pipe")
            exit(0)
        elif show == "strategies":
            strategies_info = {}
            header = ["Strategy", "Vectors in Strategy"]
            strategies_info_list = []

            strategies_conf, err = general_utilities.load_json(strategies_file)
            for strategy_name in strategies_conf.keys():
                cur_item = []
                strategy_vectors = strategies_conf[strategy_name]["vectors"]
                strategies_vectors = ', '.join(strategy_vectors)
                cur_item.append(strategy_name)
                cur_item.append(strategies_vectors)
                strategies_info_list.append(cur_item)

            print tabulate(strategies_info_list, headers=header)
            exit(0)

    elif help_vector:

        vectors_conf, err = general_utilities.load_json(vectors_file)
        for vector_name in help_vector:
            if vector_name in vectors_conf.keys():
                print "%s:\n%s" % (vector_name, vectors_conf[vector_name]["description"])
            else:
                sys.stderr.write("%s: %s" % (vector_name, "not exist"))
                exit(1)
        exit(0)
    elif help_strategy:
        strategies_conf, err = general_utilities.load_json(strategies_file)

        for strategy_name in help_strategy:
            if strategy_name in strategies_conf.keys():
                print "%s:\n%s" % (strategy_name, strategies_conf[strategy_name]["description"])
            else:
                sys.stderr.write("%s: %s" % (strategy_name, "not exist"))
                exit(1)
        exit(0)
    else:

        if vector and strategy:
            sys.stderr.write("choose strategy or vector.")
            parser.print_help()
            exit(1)
        elif not vector and not strategy:
            sys.stderr.write("choose strategy or vector.")
            parser.print_help()
            exit(1)
        elif vector:
            vectors_conf, err = general_utilities.load_json(vectors_file)
            if err:
                sys.stderr.write(err)
                exit(1)
            else:
                if vector in vectors_conf.keys():
                    manager = ricco_manager(target, vector=vector, vector_args=vector_args, vectors_conf=vectors_conf,
                                            output_format=output_format)
                else:
                    sys.stderr.write("Vector not exist %s\n" % (vector,))
                    exit(1)

        elif strategy:
            vectors_conf, err = general_utilities.load_json(vectors_file)

            strategies_conf, err = general_utilities.load_json(strategies_file)
            if err:
                sys.stderr.write(err)
                exit(1)
            else:
                if strategy in strategies_conf.keys():
                    manager = ricco_manager(target=target, strategy=strategy,
                                            strategies_conf=strategies_conf, vectors_conf=vectors_conf,
                                            output_format=output_format)
                else:
                    sys.stderr.write("Strategy not exist %s\n" % (strategy,))
                    exit(1)

        vectors_instances = manager.prepare_vectors_list()
        manager.process(vectors_instances)


if __name__ == '__main__':
    main()
