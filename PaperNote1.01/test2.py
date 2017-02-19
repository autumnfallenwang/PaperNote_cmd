#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:04:01 2016

@author: wangqiushi
"""
import os
import sys
import pickle
import bibtexparser
import re

path = os.path.abspath(os.path.dirname(sys.argv[0]))
args = sys.argv

def new():
    a = {'name':'I','age':'29'}
    return(a)
    
def str2list(string):
    outlist = []
    i1 = 0
    i2 = 0
    while i2 < len(string):
        while (i2 < len(string)) and (string[i2] != ';'):
            i2 = i2 + 1
        outlist.append(string[i1:i2])
        i1 = i2 + 1
        i2 = i1
    return(outlist)

def add(a, b=2):
    return(a + b)

def list2str(inputlist):
    outstr = ''
    for i in range(len(inputlist)):
        outstr = outstr + inputlist[i] + ';'
    return(outstr)        
        
    
if __name__ == '__main__':

    #print(type(args[1]))
 #   s = '王秋实'
  #  print(s)
   # print(type(s))
    #us = unicode(s, 'utf-8')
    #print(us)
    #print(type(us))
    #s2 = args[1]
    #print(s2)
    #print(type(s2))
    #us2 = s2.decode('gbk')
    #print(us2)
    #print(type(us2))
    a = os.name
    print(a)
    print(type(a))

     
#    a = [1,3,5,6,7,9]
#    for i in a:
#        print(i)
    
#    b = ['3','5','7']
#
#    
#    intIDlist = []
#    for i in range(len(b)):
#        intIDlist.append(int(b[i]))
    #print(str2list('agc'))

    
        
    