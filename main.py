# encoding: utf-8
__author__ = 'fanzhikang'
__date__ = '2018/10/2 22:21'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "jobbole"])
