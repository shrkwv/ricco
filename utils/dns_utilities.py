import dns.resolver
import dns.reversename

def get_MX_records(host):
    result = []
    # header = ['Type', 'Mail Exchange', 'Prefrences']

    try:
        answers = dns.resolver.query(host,'MX')
        for rdata in answers:
            # result.append(('MX',rdata.exchange,rdata.preference))
            mx_server = "%s [%s]" %(str(rdata.exchange),str(rdata.preference))
            result.append(('MX',mx_server))

    except dns.resolver.NXDOMAIN, e:
        return None
    except dns.resolver.NoAnswer, e:
        return None
    except (dns.resolver.NoNameservers, dns.resolver.Timeout), e:
        return None

    return result

def get_NS_records(host):
    result = []
    # header = ['Type', 'Nameserver']
    try:
        answers = dns.resolver.query(host,'NS')
        for rdata in answers:
            result.append(('NS',rdata))

    except dns.resolver.NXDOMAIN, e:
        return None
    except dns.resolver.NoAnswer, e:
        return None
    except (dns.resolver.NoNameservers, dns.resolver.Timeout), e:
        return None

    return result

def get_A_records(host):
    result = []
    # header = ['Type','Alias']
    try:
        answers = dns.resolver.query(host,'A')
        for rdata in answers:
            result.append(('A', rdata))

    except dns.resolver.NXDOMAIN, e:
        return None
    except dns.resolver.NoAnswer, e:
        return None
    except (dns.resolver.NoNameservers, dns.resolver.Timeout), e:
        return None

    return result

def get_AAAA_records(host):
    result = []
    # header = ['Type','Alias']
    try:
        answers = dns.resolver.query(host,'AAAA')
        for rdata in answers:
            result.append(('AAAA', rdata))

    except dns.resolver.NXDOMAIN, e:
        return None
    except dns.resolver.NoAnswer, e:
        return None
    except (dns.resolver.NoNameservers, dns.resolver.Timeout), e:
        return None

    return result

def get_host_by_addr(ip_adress):

    host = dns.reversename.from_address(ip_adress)

    return host

def get_addr_by_host(host):

    addr = dns.reversename.to_address(host)

    return addr