#!/usr/bin/env python
###########################################################################
# SCRAPE TEXT FILES AND HTMLS
###########################################################################

##############################################################
# IMPORTS
##############################################################

import re
from lxml import etree


##############################################################
# FUNCTIONS
##############################################################

######################################
# GENERAL EXTRACTING
######################################

def get_urls(page, unique=True, query=None):
    """
    Returns all the urls in page.
    if unique false get all.
    if query = string searching for the query in the urls
    """
    url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)
    if unique:
        url = list(set(url))
    if query:
        url = list(filter(lambda x: query in x, url))
    return url


def get_emails(page, unique=True):
    """
    Return all emails in the page as list
    """
    emails_regex = re.compile(r"([\d\w\.\-\_]+@[\d\w\.\-\_]+\.[\w\-\.]{2,12})")
    # emails = re.findall(r"([a-z0-9!#$%&'*+=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)",page)
    emails = re.findall(emails_regex, page)

    if unique:
        emails = list(set(emails))
    return emails


def get_ipv4(page, unique=True):
    """
    Return list of all ipv4 in page
    """
    ips = re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', page)

    if unique:
        ips = list(set(ips))

    return ips


def get_cellphones(page):
    """
    Return list of all cellphone number inside the page
    """

    cellphones = re.findall(r'\(?\d{3}\)?[-\s\.]?\d{3}[-\s\.]?\d{4}$', page)
    cellphones = list(set(cellphones))
    return cellphones


def get_phones(page, unique=True):
    """
    Return list of all phone numbers inside the page
    """
    result = []
    # phones = re.findall(r'\(?\d{2}\)?[-\s\.]?\d{3}[-\s\.]?\d{4}$',page)
    # phones = re.findall(r'\s((?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?))\s',page)
    phones = re.findall(r'\s((?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?))\s',
                        page)
    for phone in phones:
        if phone[0]:
            result.append(phone[0])
    if unique:
        result = list(set(result))
    return result


def get_paths(page, unique=True):
    """
    Returns list of paths in file
    """
    # TODO
    paths = re.findall(r"(['/]?(?:/[^/]+)*['/])", page)
    if unique:
        paths = list(set(paths))

    return paths


######################################
# HTML EXTRACTING
######################################

def get_a_hrefs(html, start_url=None, query=None):
    """
    Returns Dictionary of title and links that visible to the user in html
    if start_url returns the absoulote paths
    """
    links = {}
    tree = etree.HTML(html)

    #    items = tree.xpath("//a/text() | //a/@href")
    a_tags = tree.xpath("//a[@*]")
    for a_tag in a_tags:
        title = a_tag.xpath("text()")
        link = a_tag.xpath("@href")
        if not title or not link or '#' in link:
            continue
        link = link[0]
        title = title[0]
        # add absoulute path
        if start_url and link[0] == '/':
            link = start_url + link
        if query and not query in link:
            print "query deletion"
            continue
        links[title] = link

    return links


def get_img_href(html):
    """
    Returns all image links in page
    """
    pass


def get_img_src(html, start_url=None):
    """
    Returns all images links
    """
    src_links = []
    tree = etree.HTML(html)
    image_links = tree.xpath("//img/@src")
    # make absoulote link
    for src_link in image_links:
        if start_url and not src_link.startswith("http"):
            if start_url and src_link[0] == '/':
                src_link = start_url + src_link
            else:
                src_link = start_url + "/" + src_link

        src_links.append(src_link)
    return src_links
