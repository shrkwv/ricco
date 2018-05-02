__author__ = 'john'
import ConfigParser
# base_path = os.path.dirname(os.path.realpath(ricco.__file__))
my_path = '/home/john/workspaces/projects/ricco-web/ricco/core/ricco.ini'
ricco_conf = ConfigParser.ConfigParser()
with open(my_path) as f:
    print f.read()
# ricco_conf.read(open(my_path))
ricco_conf.readfp(open(my_path))
print ricco_conf.sections()
