import re

def is_ipv4(addr):
    """
    check if addr is a valid ipv4
    :param addr:
    :return:boolean
    """
    ipv4_regex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    if re.match(ipv4_regex,addr):
        return True
    else:
        return False
