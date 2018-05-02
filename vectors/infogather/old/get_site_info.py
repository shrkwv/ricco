#!/usr/bin/env python

import argparse
import logging
import urllib2
import json
import time

import utils.scraper as scraper
from utils.tabulate import tabulate
import utils.site2list as site2list


#######################################################
# OPTION Handling
#######################################################

parser = argparse.ArgumentParser(description="Tool for downloading sites")

# mandatory
parser.add_argument("-u", type=str, help="The URL to be downloaded (mandatory).")
# optional flags
parser.add_argument("-R", action='store_true',
                    help="Recursive download of the site (by default download the specified url only)")
parser.add_argument("-l", action='store_true', help='Return all "user seen links" in page')
parser.add_argument("-L", action='store_true', help="Return all urls in page")
parser.add_argument("-i", action='store_true', help="Return all links to images in page")
parser.add_argument("-e", action='store_true',
                    help="Return all emails in page and if possible the name seen by the user")
parser.add_argument("-p", action='store_true', help="Return all phone numbers in the page")
parser.add_argument("--html", action='store_true', help="Output html tables")
parser.add_argument("--json", action='store_true', help="Output as json")

parser.add_argument("-V", action='store_true', help="VERBOSE")
parser.add_argument("-D", action='store_true', help="DEBUGGING")

args = parser.parse_args()

# enable logging
verbose = args.V
debug = args.D
if verbose:
    logging.basicConfig(level=logging.INFO)
if debug:
    logging.basicConfig(level=logging.DEBUG)

URL = args.u
# flags
RECURSIVE = args.R
GET_LINKS = args.l
GET_HIDDEN_URLS = args.L
GET_IMAGES = args.i
GET_EMAILS = args.e
GET_PHONES = args.p
HTML = args.html
JSON = args.json


#######################################################
# FUNCTIONS
#######################################################

def download_page(url):
    page = {}
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request, timeout=5)
        page[url] = response.read()
        return page
    except urllib2.URLError, e:
        logging.debug(e)
        exit(1)
    except urllib2.HTTPError, e:
        logging.debug(e)
    except Exception:
        logging.debug("Unknown error")


def get_secondary_url(url):
    """
    returns the www / not www url for the entered url
    """
    if "://www." in url:
        second_url = url.split("://www.")
        second_url = second_url[0] + "://" + second_url[1]
    else:
        # TODO better one!
        second_url = url.split("://")
        second_url = second_url[0] + "://" + "www." + second_url[1]
    return second_url


def get_insite_links(start_html, url_site):
    second_url = get_secondary_url(url_site)
    urls = scraper.get_urls(start_html)
    links = scraper.get_a_hrefs(start_html, url_site)
    links = links.values()
    all_links = list(set(urls + links))
    site_links = []
    for link in all_links:
        if link.startswith(url_site) or link.startswith(second_url):
            site_links.append(link)
    return site_links


def download_site(url):
    pages = {}
    all_site_links = []
    # download first html to extract all the links
    html = download_page(url)
    html = html.values()
    html = html[0]
    # get all the urls in the html that starts with the url
    start_site_links = get_insite_links(html, url)
    # temporary list of all in site links
    all_site_links = start_site_links
    logging.debug("download page")
    logging.debug(start_site_links)
    # start looping in the site list
    for link in start_site_links:
        cur_html = download_page(link)
        if not cur_html:
            continue
        cur_html = cur_html.values()
        cur_html = cur_html[0]
        # check if there are more links in the site
        cur_site_links = get_insite_links(cur_html, url)
        if cur_site_links:
            cur_site_links = list(set(cur_site_links) - set(all_site_links))
            if cur_site_links:
                all_site_links = all_site_links + cur_site_links
                logging.debug("cur site link")
                logging.debug(cur_site_links)
                for l in cur_site_links:
                    cur_html = download_page(link)
                    if not cur_html:
                        continue
                    cur_html = cur_html.values()
                    cur_html = cur_html[0]
                    pages[l] = cur_html
            else:
                pages[link] = cur_html
    return pages


def crawl_links(pages, url):
    result = []
    for page_url, page in pages.iteritems():
        links = scraper.get_a_hrefs(page, url)
        data = [k + " : " + v for k, v in links.iteritems()]
        if data:
            for link in data:
                item = {}
                item["type"] = "link"
                item["url"] = page_url
                item["data"] = link
                result.append(item)
    return result


# crawl for urls
def crawl_hidden_urls(pages):
    result = []
    for page_url, page in pages.iteritems():
        hidden_urls = scraper.get_urls(page)
        if hidden_urls:
            for hidden_url in hidden_urls:
                item = {}
                item["type"] = "h_url"
                item["url"] = page_url
                item["data"] = hidden_url
                result.append(item)
    return result


def crawl_img_src(pages, start_url=None):
    result = []
    for page_url, page in pages.iteritems():
        if start_url:
            images = scraper.get_img_src(page, start_url)
        else:
            images = scraper.get_img_src(page)
        if images:
            for image in images:
                item = {}
                item["type"] = "image"
                item["url"] = page_url
                item["data"] = image
                result.append(item)
    return result


def crawl_emails(pages):
    result = []
    for page_url, page in pages.iteritems():
        emails = scraper.get_emails(page)
        if emails:
            for email in emails:
                item = {}
                item["type"] = "email"
                item["url"] = page_url
                item["data"] = email
                result.append(item)
    return result


def crawl_phones(pages):
    result = []
    for page_url, page in pages.iteritems():
        phones = scraper.get_phones(page)
        if phones:
            for phone in phones:
                item = {}
                item["type"] = "phone"
                item["url"] = page_url
                item["data"] = phone
                result.append(item)

    return result


#######################################################
# CHECKERS
#######################################################
# check mandatory options
if URL == None:
    parser.print_help()
    exit(1)

#######################################################
# THE BOMB
#######################################################

# download page / site
s_time = time.time()
if not RECURSIVE:
    downloader = site2list.Download(URL, 1, RECURSIVE=False)
    pages = downloader.getPages()
    # pages = download_page(URL)
else:
    downloader = site2list.Download(URL, 4, RECURSIVE=True)
    pages = downloader.getPages()
    # pages = download_site(URL)

results = []

# get all hyperlinks
if GET_LINKS:
    links = crawl_links(pages, URL)
    results += links
    # for title, cur_links in links.iteritems():

if GET_HIDDEN_URLS:
    hidden_urls = crawl_hidden_urls(pages)
    results += hidden_urls

# crawl for images
if GET_IMAGES:
    images = crawl_img_src(pages, URL)

    results += images

# crawl for emails
if GET_EMAILS:
    emails = crawl_emails(pages)
    results += emails

# crawl for phones
if GET_PHONES:
    phones = crawl_phones(pages)
    results += phones

if HTML:
    tmp = {}
    tmp["data"] = results
    json = json.dumps(tmp)
    print json
elif JSON:
    json = json.dumps(results)
    print json
else:
    print tabulate(results, headers="keys")
# print time.time()-s_time
