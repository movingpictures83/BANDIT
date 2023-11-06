import random
import sys
from disk_struct import Disk
from page_replacement_algorithm import  page_replacement_algorithm
from CacheLinkedList import  CacheLinkedList
import numpy as np

import BANDIT
import BANDIT2
import BANDIT3
import BANDIT_DOUBLE_HIST

import PyIO
import PyPluMA

class BANDITPlugin:
  def input(self, inputfile):
        self.parameters = PyIO.readParameters(inputfile)

  def run(self):
        pass

  def output(self, outputfile):
    n = int(self.parameters["n"])
    infile = open(PyPluMA.prefix()+"/"+self.parameters["infile"], 'r')
    kind = self.parameters["kind"]
    outfile = open(outputfile, 'w')
    outfile.write("cache size "+str(n))
    if (kind == "BANDIT"):
       bandit = BANDIT.BANDIT(n)
    elif (kind == "BANDIT2"):
       bandit = BANDIT2.BANDIT2(n)
    elif (kind == "BANDIT3"):
       bandit = BANDIT3.BANDIT3(n)
    else:
       bandit = BANDIT_DOUBLE_HIST.BANDIT_DOUBLE_HIST(n)
    page_fault_count = 0
    page_count = 0
    for line in infile:
        line = int(line.strip())
        outfile.write("request: "+str(line))
        if bandit.request(line) :
            page_fault_count += 1
        page_count += 1

    
    outfile.write("page count = "+str(page_count))
    outfile.write("\n")
    outfile.write("page faults = "+str(page_fault_count))
    outfile.write("\n")
