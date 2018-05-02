#!/usr/bin/env python

class vector_data_holder(object):
    

    def __init__(self,class_name, banner, header, output):
        self.__class_name = class_name
        self.__banner = banner
        self.__header = header
        self.__output = output

    @property
    def class_name(self):
        return self.__class_name

    @class_name.setter
    def class_name(self,class_name):
        self.__class_name = class_name

    @property
    def banner(self):
        return self.__banner

    @banner.setter
    def banner(self,banner):
        self.__banner = banner

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self,header):
        self.__header = header

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, output):
        self.__output = output