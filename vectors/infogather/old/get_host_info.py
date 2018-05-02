#!/usr/bin/env python
import argparse
import sys
import os
import socket
import logging
import json

from utils.tabulate import tabulate
import utils.scraper as scraper



###################################################
# options handle
###################################################

parser = argparse.ArgumentParser()
# mandatory
parser.add_argument("-d", type=str, help="The root domain.")
parser.add_argument("-s", type=str, help="File for the subdomains.")
# or
parser.add_argument("-i", nargs="*", help="Ip or list of ips or file contains ips.")

# flag options
# parser.add_argument("-t", type=str, help="Type of searcg (MX, A, NS")

parser.add_argument("--alive", action="store_true", help="Check if result hosts are pingable")
parser.add_argument("-R", action="store_true", help="search recursively after found host on ip ranges.")
parser.add_argument("-q", nargs='?', type=str, help="Serch for specified query (default domain name)")

parser.add_argument("--html", action='store_true', help="html")
parser.add_argument("--json", action='store_true', help="json")

parser.add_argument("-V", action='store_true', help="VERBOSE")
parser.add_argument("-D", action='store_true', help="DEBUGGING")

args = parser.parse_args()

###################################################
# VARS
###################################################
verbose = args.V
debug = args.D
if verbose:
    logging.basicConfig(level=logging.INFO)
if debug:
    logging.basicConfig(level=logging.DEBUG)

domain = args.d
sub_list = args.s

ip_list = args.i
# FLAGS
CHECK_ALIVE = args.alive
RECURSIVE = args.R
HTML = args.html
JSON = args.json

query = args.q
logging.debug(query)
if not args.q:
    query = domain
    logging.debug(query)


###################################################
# functions
###################################################

def check_ping(ips):
    pingable_result = []
    for ip in ips:
        response = os.system("ping -c1 -w1 " + ip + ">/dev/null 2>&1")

        if response == 0:
            pingable_result.append(ip)
    return pingable_result


def check_subdomains(subs, domain):
    sub_results = []
    for sub in subs:
        cur_host = ''.join(sub + "." + domain)
        try:
            # cur_host = str(cur_host)
            info = socket.gethostbyname_ex(cur_host)
            logging.debug(cur_host)
            logging.debug(info)


            # info = socket.getaddrinfo(cur_host)
            info_dic = {}
            cur_host = info[0]
            aliases = info[1]
            cur_ips = info[2]

            info_dic["hostname"] = cur_host
            info_dic["aliases"] = aliases
            info_dic["ips"] = cur_ips
            sub_results.append(info_dic)

        except socket.gaierror, err:
            # TODO
            logging.debug(err)
        except Exception, err:
            logging.debug(err)
    return sub_results


def get_class_c(ip_list):
    range_list = []
    for ip in ip_list:
        ip_cut = ip.split(".")
        del ip_cut[3]
        ip_range = ".".join(ip_cut)
        range_list.append(ip_range)

    range_list = list(set(range_list))

    return range_list


def check_ips(ips_list):
    range_list = []
    ip_results = []
    logging.debug("ip_list")
    logging.debug(ips_list)

    range_list = get_class_c(ips_list)

    logging.debug("range_list")
    logging.debug(range_list)
    for ip_range in range_list:
        for octale in xrange(1, 20):
            try:
                cur_ip = ''.join(ip_range + "." + str(octale))
                logging.debug(cur_ip)

                # cur_ip = str(cur_ip)
                info = socket.gethostbyaddr(cur_ip)
                info_dic = {}
                cur_host = info[0]
                aliases = info[1]
                cur_ips = info[2]
                info_dic["hostname"] = cur_host
                info_dic["aliases"] = aliases
                info_dic["ips"] = cur_ips
                ip_results.append(info_dic)

            except socket.gaierror, err:
                # TODO
                logging.debug(err)
            except Exception, err:
                logging.debug(err)

    return ip_results


def filter_results(results, query, CHECK_ALIVE=False):
    filtered_results = []
    if query:
        for item in results:
            cur_aliases = []
            cur_hostname = item["hostname"]
            cur_aliases = item["aliases"]
            cur_aliases.append(cur_hostname)

            query_in_alias = False
            for alias in cur_aliases:
                if query in alias:
                    query_in_alias = True
                    break

            if query_in_alias:
                filtered_results.append(item)

        if CHECK_ALIVE:
            for item in results:
                check_ips = item["ips"]
                if check_ips:
                    pingable_result = check_ping(check_ips)
                    item["ips"] = pingable_result
                    filtered_results.append(item)
    return filtered_results


###################################################
# CHECKERS
###################################################
ips = []
results = {}

if not (ip_list or ips) and not (sub_list and domain):
    print "sub list are for domain check"
    parser.print_help
    sys.exit(1)

# check if sub list available
if ip_list:
    ips_to_check = "\n".join(ip_list)

    tmp_list = scraper.get_ipv4(ips_to_check)

    if tmp_list:
        ips = tmp_list

    else:
        for path in ip_list:
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    f = f.read()
                    logging.debug("scraping ips from file")
                    ips.append(scraper.get_ipv4(f))

    if not ips:
        print "no ips found"
        parser.print_help
        sys.exit(1)

if sub_list:
    if not os.path.isfile(sub_list):
        print "list file not exist"
        parser.print_help
        sys.exit(1)
    else:
        with open(sub_list, 'r') as f:
            f = f.read().splitlines()
            sub_domains = f
else:
    sub_domains = None


###################################################
# THE HARD STUFF
###################################################

# get results

if sub_domains:
    results = check_subdomains(sub_domains, domain)


elif ips:

    results = check_ips(ips)

# filter result
results = filter_results(results, query, CHECK_ALIVE)

if RECURSIVE:
    ips_to_check = []
    logging.debug("################## recursive #######################3")
    for item in results:
        cur_ips = item["ips"]
        ips_to_check = ips_to_check + cur_ips

    tmp_ips = check_ips(ips_to_check)
    results += (tmp_ips)

    results = filter_results(results, query)




#########################
# PRINTING
#########################
if HTML:
    json_for_web = {}
    json_for_web["data"] = results
    json_results = json.dumps(json_for_web)
    print json_results
elif JSON:
    json_results = json.dumps(results)
    print json_results
else:
    print tabulate(results, headers="keys")
