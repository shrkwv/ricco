#!/usr/bin/env python

###########################################################################
# GET LIST OF ACTIVE PROXIES
###########################################################################

##############################################################
# IMPORTS
##############################################################

import urllib2
import re
from lxml import html, etree
import argparse
import logging
import json
from tabulate import tabulate

##############################################################
# OPTION HANDLING
##############################################################
parser = argparse.ArgumentParser(description="Gets list of proxies from free-proxy-list.net")


parser.add_argument("-a",action='store_true', help="Get only anonymous proxies")

parser.add_argument("-c",type = str, help="Get only proxies in specified country")
parser.add_argument("--port",type = str, help="Get only proxies in specified port")
parser.add_argument("-t", type = str, help="Get only proxy type specified (elite,annonymous,transperent)")
parser.add_argument("-p", type = str, help="Get specified protocol")

parser.add_argument("-d", action='store_true', help="Get detailed list")

parser.add_argument("--alive", action='store_true', help="Check if proxy Alive")

parser.add_argument("--html", action='store_true', help="Output html format")

parser.add_argument("--json", action='store_true', help="Output json format")

parser.add_argument("-V", action='store_true', help="VERBOSE")
parser.add_argument("-D", action='store_true', help="DEBUGGING")


args = parser.parse_args()
anonymous = args.a
country = args.c
protocol = args.p
port = args.port
proxy_type = args.t
details = args.d
check_alive = args.alive

HTML = args.html
JSON = args.json
# logging
verbose = args.V
debug = args.D

if verbose:
    logging.basicConfig(level=logging.INFO)
if debug:
    logging.basicConfig(level=logging.DEBUG)

##############################################################
# FUNCTIONS
##############################################################
def get_page(url):
    pages = {}
    request = urllib2.Request(url)
    # proxy = urllib2.ProxyHandler()
    # opener = urllib2.build_opener(proxy)
    # urllib2.install_opener(opener)
    try:
        response = urllib2.urlopen(request)
        pages[url] = response.read()
        return pages
    except urllib2.URLError, e:
        print e
        logging.debug(url)
        logging.debug(e)
    except urllib2.HTTPError, e:
        print e
        logging.debug(url)
        logging.debug(e)
    except Exception, e:
        print e
        logging.debug(url)
        logging.debug("Unknown error")

def get_real_ip():
    """
    Returns the real public ip address from another site
    """
    ip = get_page("http://www.icanhazip.com")
    logging.debug("the ip is: " + ip)
    return ip



def check_proxy(protocol,proxy_url,real_ip):
    """
    Return True if proxy is alive and hiding ip
    """
    user_agent = 'Mozilla/5.0'
    ip_check_url = "http://ip.42.pl/raw"
#    real_ip = "81.65.154.11"
    try:
        logging.info("try proxy: " + proxy_url)
        proxy_handler = urllib2.ProxyHandler({protocol: proxy_url})
        logging.debug("ProxyHandler")
        opener = urllib2.build_opener(proxy_handler)
        logging.debug("build opener")
        opener.addheaders = [('User-agent', user_agent)]
        logging.debug("adding headers")
        urllib2.install_opener(opener)
        logging.debug("install opener")

        request = urllib2.Request(ip_check_url)
        logging.debug("Request")
        sock = urllib2.urlopen(request, timeout=5)
        logging.debug("urlopen")
        detected_ip = sock.read()
        logging.info("real ip: " + real_ip)
        logging.info("detected ip: " + detected_ip)
        if detected_ip is real_ip:
            return False
    except urllib2.HTTPError, e:
        logging.debug(e.code)
        return False
    except Exception, detail:
        logging.debug(detail)
        return False
    return True

def get_proxy_list(page):
    """
    Returns Dictionary of (IP:PORT) : COUNTRY
    """
    proxy_list = []
    tree = etree.HTML(page)

    items = tree.xpath("//table/tbody/tr")
    for item in items:
        proxy_item = item.xpath("td/text()")

        proxy_list.append(proxy_item)
    return proxy_list

def list_of_lists_to_json(list_of_lists, headers):
    result = []
    for l in list_of_lists:
        cur_result = dict(zip(headers, l))
        result.append(cur_result)

    return result

##############################################################
# HARD STUFF
##############################################################
result = []
pages = {}
p_list = []
# get all / anonymous only
if anonymous:

    pages = get_page("http://free-proxy-list.net/anonymous-proxy.html")
else:

    pages = get_page("http://free-proxy-list.net")
if pages:
    for link, html in pages.iteritems():
        p_list = get_proxy_list(html)



#################################
# PARSING RESULTS
#################################

# make custom list
proxy_list=[]

for proxy in p_list:
    if proxy[6] == "yes":
        proxy[6] = "https"
    else:
        proxy[6] = "http"

# filter result

if country or port or protocol or proxy_type:
    filtered_list = []
    searches = []
    if country:
        searches.append(country)
    if port:
        searches.append(port)
    if proxy_type:
        searches.append(proxy_type)
    if protocol:

        searches.append(protocol)
    for proxy in p_list:
        if all(x in proxy for x in searches):
            filtered_list.append(proxy)
    p_list = filtered_list

# clean unneeded data
for p in p_list:
    proxy = []
    proxy.append(p[0])
    proxy.append(p[1])
    proxy.append(p[2])
    proxy.append(p[3])
    proxy.append(p[4])
    proxy.append(p[6])
    proxy.append(p[7])
    proxy_list.append(proxy)

# check if proxy available
if check_alive:
    alive_list = []
    real_ip = get_real_ip()
    for proxy in proxy_list:

        logging.info("checking alive")
        protocol = proxy[4]
        ip = proxy[0]
        port = proxy[1]
        url = protocol+"://"+ip +":"+port
        check = check_proxy(protocol, url, real_ip)

        if check:
            alive_list.append(proxy)
        else:
            pass
    proxy_list = alive_list

#################################
# PRINTING
#################################
d_headers = ["ip","Port","Country Code","Country Name","Proxy Type","Protocol","Last checked"]
if HTML:
    json_for_web = {}
    json_for_web["data"] = list_of_lists_to_json(proxy_list, d_headers)
    json_results = json.dumps(json_for_web, ensure_ascii=True)
    print json_results

elif JSON:
    json_result = list_of_lists_to_json(proxy_list, d_headers)
    json_results = json.dumps(json_result, ensure_ascii=True)
    print json_results
else:
    json_result = list_of_lists_to_json(proxy_list, d_headers)
    json_results = json.dumps(json_result, ensure_ascii=True)
    print tabulate(json_result, headers="keys")

