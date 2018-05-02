# !/usr/bin/env python
import json
from core.base.vector_data_holder import vector_data_holder
import os
import ricco
import ConfigParser
class base_vector():
    base_path = os.path.dirname(os.path.realpath(ricco.__file__))
    ricco_conf = ConfigParser.ConfigParser()
    ricco_ini_path = base_path +"/core/ricco.ini"
    ricco_conf.readfp(open(ricco_ini_path))

    def prepare(self, target):
        pass

    def execute(self):
        pass

    def output(self):
        name_of_class = self.__class__.__name__
        # item_result = {
        #     "banner": self.banner,
        #     "header": self.header,
        #     "result": self.result
        # }
        # class_result = (name_of_class, item_result)
        vector_result = vector_data_holder(name_of_class, self.banner, self.header, self.result)
        return vector_result
