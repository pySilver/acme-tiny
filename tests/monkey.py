import os, sys
from tempfile import NamedTemporaryFile
from subprocess import Popen
try:
    from urllib.request import urlopen # Python 3
except ImportError:
    from urllib2 import urlopen # Python 2

# domain with server.py running on it for testing
DOMAIN = os.getenv("TRAVIS_DOMAIN", "travis-ci.gethttpsforfree.com")

# generate account and domain keys
def gen_keys():
    # good account key
    account_key = NamedTemporaryFile()
    Popen(["openssl", "genrsa", "-out", account_key.name, "2048"]).wait()

    # weak 1024 bit key
    weak_key = NamedTemporaryFile()
    Popen(["openssl", "genrsa", "-out", weak_key.name, "1024"]).wait()

    # good domain key
    domain_key = NamedTemporaryFile()
    domain_csr = NamedTemporaryFile()
    Popen(["openssl", "req", "-newkey", "rsa:2048", "-nodes", "-keyout", domain_key.name,
        "-subj", "/CN={0}".format(DOMAIN), "-out", domain_csr.name]).wait()

    # subject alt-name domain
    san_csr = NamedTemporaryFile()
    san_conf = NamedTemporaryFile()
    san_conf.write(open("/etc/ssl/openssl.cnf").read().encode("utf8"))
    san_conf.write("\n[SAN]\nsubjectAltName=DNS:{0}\n".format(DOMAIN).encode("utf8"))
    san_conf.seek(0)
    Popen(["openssl", "req", "-new", "-sha256", "-key", domain_key.name,
        "-subj", "/", "-reqexts", "SAN", "-config", san_conf.name,
        "-out", san_csr.name]).wait()

    # invalid domain csr
    invalid_csr = NamedTemporaryFile()
    Popen(["openssl", "req", "-new", "-sha256", "-key", domain_key.name,
        "-subj", "/CN=\xC3\xA0\xC2\xB2\xC2\xA0_\xC3\xA0\xC2\xB2\xC2\xA0.com", "-out", invalid_csr.name]).wait()

    # nonexistent domain csr
    nonexistent_csr = NamedTemporaryFile()
    Popen(["openssl", "req", "-new", "-sha256", "-key", domain_key.name,
        "-subj", "/CN=404.{0}".format(DOMAIN), "-out", nonexistent_csr.name]).wait()

    #account-signed domain csr
    account_csr = NamedTemporaryFile()
    Popen(["openssl", "req", "-new", "-sha256", "-key", account_key.name,
        "-subj", "/CN={0}".format(DOMAIN), "-out", account_csr.name]).wait()

    return {
        "account_key": account_key,
        "weak_key": weak_key,
        "domain_key": domain_key,
        "domain_csr": domain_csr,
        "san_csr": san_csr,
        "invalid_csr": invalid_csr,
        "nonexistent_csr": nonexistent_csr,
        "account_csr": account_csr,
    }
