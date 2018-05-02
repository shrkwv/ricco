#!/usr/bin/env python
import json
import shlex
import subprocess
# import cStringIO
# from xmlutils.xml2json import xml2json
import xmltodict


class NmapScanner(object):
    def __init__(self, nmap_path='nmap'):
        self.scan_result = ''
        self.nmap_path = nmap_path
        self.parsed_scan_results = None
        self.parsed_raw_scan_results = None
        self.nmap_err =None
        self.command = None
        self.version = None

    def scan(self, hosts='127.0.0.1', ports=None, arguments='', sudo=False):

        for redirecting_output in ['-oX', '-oA']:
            assert not redirecting_output in arguments, 'Xml output can\'t be redirected from command line.\nYou can access it after a scan using:\nnmap.nm.get_nmap_last_output()'

        h_args = shlex.split(hosts)

        if arguments:
            f_args = shlex.split(arguments)

        # Launch scan
            args = [self.nmap_path, '-oX', '-'] + h_args + ['-p', ports] * (ports != None) + f_args
        else:
            args = [self.nmap_path, '-oX', '-'] + h_args + ['-p', ports] * (ports != None)

        if sudo:
            args = ['sudo'] + args

        p = subprocess.Popen(args, bufsize=100000, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        # wait until finished
        # get output
        (self.scan_result, nmap_err) = p.communicate()
        self.nmap_err = nmap_err

        self.parsed_raw_scan_results = self.analyse_nmap_xml_scan()
        self.parsed_scan_results = self.parsed_raw_scan_results.values()[0]
        del self.parsed_scan_results["debugging"]
        del self.parsed_scan_results["verbose"]

        self.basic_extractor()

    def analyse_nmap_xml_scan(self):
        """

        :param nmap_xml_output: xml string to analyse
        :returns: scan_result as dictionnary
        """

        nmap_xml_output = self.scan_result
        # with cStringIO.StringIO() as f:
        #     f.write(nmap_xml_output)
        #     nmap_xml_file = f
        # json_results = xml2json(nmap_xml_file)
        # xml2json.c
        nmap_as_dict = xmltodict.parse(nmap_xml_output)

        json_results = json.dumps(nmap_as_dict)
        json_object = json.loads(json_results)
        return json_object

    def basic_extractor(self):
        """
        extract all basic data

        :return:
        """
        self.command = self.parsed_scan_results['@args']
        self.version = self.parsed_scan_results['@version']


    def get_json_results(self):
        """

        :return: scan result as dictionary
        """
        return self.parsed_scan_results


    def get_raw_json_results(self):

        return self.parsed_raw_scan_results

    def get_hosts(self):
        """

        :return:list of hosts
        """
        return self.hosts

    def get_command(self):

        return self.command

    def get_version(self):

        return self.version


    def get_all_hosts(self):

        result = []
        hosts = self.parsed_scan_results['host']
        for host in hosts:
            result.append(host['address']['@addr'])
        return result

    def __getitem__(self, addr):
        result = ()
        hosts = self.parsed_scan_results['host']
        if isinstance(hosts,list):
            for host in hosts:
                if host['address']['@addr'] == addr:
                    result  = (addr,host)
        else:
            if hosts['address']['@addr'] == addr:
                result  = (addr,hosts)


        return result
