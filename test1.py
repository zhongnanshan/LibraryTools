#--coding:utf-8--

import matplotlib.pyplot as plt
import networkx as nx
import librarydoor as libdr

def mytest1():
    tall = libdr.TemporalAll()
    dyn1 = tall.getDynasties()[0]
    print dyn1.getLabel()+" "+str(dyn1.getReignTime())

def mytest2():
    zhang = libdr.FamilyName("张")
    print zhang.getID()
    zhang1 = libdr.ResFromURI(zhang.getID())
    print zhang1.getJSON()['description']
    zhangyi = libdr.Person("张良")
    if zhangyi.getPersons() != None:
        for p in zhangyi.getPersons():
            print p.getID()
        zhangliang = libdr.ResFromURI(zhangyi.getPersons()[0].getID())
        print zhangliang.getJSON()
    else:
        print "未查询到数据"

if __name__ == '__main__':
    mytest2()
    