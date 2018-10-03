# encoding: utf-8
__author__ = 'fanzhikang'
__date__ = '2018/10/3 22:41'

import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf_8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()