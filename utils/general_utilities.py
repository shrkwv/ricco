#!/usr/bin/env python
from collections import OrderedDict
import json
import os
import random
import string
import urllib
import urllib2
from urlparse import urlparse
import socket
import math


def get_class_c(ip_list):
    range_list = []
    for ip in ip_list:
        ip_cut = ip.split(".")
        del ip_cut[3]
        ip_range = ".".join(ip_cut)
        range_list.append(ip_range)

    range_list = list(set(range_list))

    return range_list


def generate_banner(string_inside):
    banner_size = len(string_inside)
    seperator = "\n" + "=" * banner_size + "\n"
    banner = seperator + string_inside + seperator

    return banner


def check_ping(ips):
    pingable_result = []
    for ip in ips:
        response = os.system("ping -c1 -w1 " + ip + ">/dev/null 2>&1")

        if response == 0:
            pingable_result.append(ip)
    return pingable_result


def get_base_url(url):
    parsed_uri = urlparse(url)
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return base_url


def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain

def get_domain_without_suffix(url, suffixes = 'static-data/suffixes.txt'):
    with open(suffixes, 'r') as f:
        suffixes = f.read()
        suffixes = suffixes.split("\n")
        suffixes = [suffix.lower() for suffix in suffixes]
    parsed_uri = urlparse(url)
    if "://" in url:

        domain = '{uri.netloc}'.format(uri=parsed_uri)
    else:
        domain = '{uri.path}'.format(uri=parsed_uri)
    splitted_domain = str(domain).split(".")

    if len(splitted_domain) == 1:
        return domain
    elif len(splitted_domain) >= 2:
        tmp_splitted_domain = []
        tmp_splitted_domain = splitted_domain
        while tmp_splitted_domain[-1] in suffixes:
            del splitted_domain[-1]
        domain_without_suffixes = '.'.join(splitted_domain)

    return domain_without_suffixes

def get_host_by_ip(ip_address):
    try:
        host = socket.getfqdn(ip_address)
    except:
        return None

    return host

def get_ip_by_host(host):
    try:
        ip = socket.gethostbyname(host)
    except:
        return None

    return ip


def load_json(json_file_path, mode='r'):
    json_object = None
    err = None
    with open(json_file_path, mode) as f:
        try:
            json_object = json.load(f)
        except IOError, e:
            err = e
        except KeyError, e:
            err = e

    return json_object, err


def get_page(url, params = None):
    """
    download page and insert result to string
    :param url:
    :return:
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    if params:
        url = url + urllib.urlencode(params)
    result = None
    e = None
    try:
        request = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(request)
        result = response.read()
    except ValueError, e:
        return result, e

    return result, e


def get_bounding_box(latitude_in_degrees, longitude_in_degrees, half_side_in_meters):
    assert half_side_in_meters > 0
    assert latitude_in_degrees >= -180.0 and latitude_in_degrees  <= 180.0
    assert longitude_in_degrees >= -180.0 and longitude_in_degrees <= 180.0

    half_side_in_km = half_side_in_meters / 1000.0

    lat = math.radians(latitude_in_degrees)
    lon = math.radians(longitude_in_degrees)

    radius  = 6371
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - half_side_in_km/radius
    lat_max = lat + half_side_in_km/radius
    lon_min = lon - half_side_in_km/parallel_radius
    lon_max = lon + half_side_in_km/parallel_radius
    rad2deg = math.degrees

    box = {}
    box['lat_min'] = rad2deg(lat_min)
    box['lon_min'] = rad2deg(lon_min)
    box['lat_max'] = rad2deg(lat_max)
    box['lon_max'] = rad2deg(lon_max)

    return box

def get_random_str(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def list_and_headers_to_json(headers,list_of_lists):
    assert isinstance(headers, list)
    assert [isinstance(l,list) for l in list_of_lists]
    result = []
    for l in list_of_lists:
        assert len(l) == len(headers)
        dct = OrderedDict(zip(headers,l))
        result.append(dct)


    return result