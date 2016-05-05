#--coding:utf-8--

import urllib2, urllib
import json
from pprint import pprint
from myprivate import getAPIKey

APIKey = getAPIKey()

##通用的UUID定义
UUID_LIBRARY = {
    'beginYear':'http://www.library.sh.cn/ontology/beginYear',
    'endYear':'http://www.library.sh.cn/ontology/endYear',
    'person':'http://data.library.sh.cn/jp/entity/person/',
}


##通过URI获取资源
class ResFromURI:
    def __init__(self, id):
        self.prefix = 'http://data.library.sh.cn/jp/data/json?uri='
        self.url = self.prefix+id+'&key='+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read(1024)
##        转换成Python对象
        self.json = json.loads(tt)

    def getJSON(self):
        return self.json


##姓氏
class FamilyName:
    def __init__(self, fname):
        self.prefix = 'http://data.library.sh.cn/jp/familyname/'
        self.url = self.prefix+fname+'?key='+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read(1024)
##        转换成Python对象
        tt1 = json.loads(tt)
##        解析内容
        self.id = tt1['@id']
        self.description = tt1['description']

    def getID(self):
        return self.id

    def getDescrip(self):
        return self.description

##具体的人
class ThePerson:
    def __init__(self, id, relatedWork):
        self.id = id
        self.relatedWork = relatedWork

    def getID(self):
        return self.id

    def getRelatedWork(self):
        return self.relatedWork

    def setRoleOfFamily(self,rof):
        self.roleOfFamily = rof
        
    def getRoleOfFamily(self):
        return self.roleOfFamily

    def setFamilyName(self,fn):
        self.familyName = fn
        
    def getFamilyName(self):
        return self.familyName

##姓名
    def setLabel(self, label):
        self.label = label

##性别
    def setGender(self, gender):
        self.gender = gender

##父亲
    def setFather(self, father):
        self.father = father

##妻子
    def setSpouses(self, spouses):
        self.spouses = spouses

##谱名（人在家谱上记载的谱名）
    def setGenealogyName(self, genealogyName):
        self.genealogyName = genealogyName

##字
    def setCourtesyName(self, courtesyName):
        self.courtesyName = courtesyName

##号
    def setPseudonym(self, pseudonym):
        self.pseudonym = pseudonym

##排行
    def setOrderOfSeniority(self, orderOfSeniority):
        self.orderOfSeniority = orderOfSeniority


##先祖名人
class Person:
    def __init__(self, pname):
        self.prefix = "http://data.library.sh.cn/jp/person/"
        self.url = self.prefix+pname+'?key='+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read(16384)
        if "未查询到数据" not in tt:
##            转换为Python对象
            tt1 = json.loads(tt)
##            家族参数
            self.familyName = tt1[0]['familyName']
##            个人参数
            self.persons = []
            for tt2 in tt1:
                id = tt2['@id']
                relatedWork = tt2['relatedWork']
                person = ThePerson(id, relatedWork)
                person.setRoleOfFamily(tt2['roleOfFamily'])
                person.setFamilyName(self.familyName)
                self.persons.append(person)
        else:
            self.familyName = None
            self.persons = None

    def getFamilyName(self):
        return self.familyName

    def getPersons(self):
        return self.persons

##（3）地名
class Place:
    def __init__(self, pname):
        self.prefix = "http://data.library.sh.cn/jp/place/"
        self.url = self.prefix+pname+'?key='+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read(8192)
##        转换为Python对象
        tt1 = json.loads(tt)
##        解析内容
        self.id = tt1['@id']
        self.province = tt1['province']
        self.city = tt1['city']
        self.county = tt1['county']
        if 'description' in tt1.keys():
            self.description = tt1['description']
        else:
            self.description = None
##        地理经度
        if 'long' in tt1.keys():
            self.long = float(tt1['long'])
        else:
            self.long = None
##        地理纬度
        if 'lat' in tt1.keys():
            self.lat = float(tt1['lat'])
        else:
            self.lat = None

    def getID(self):
        return self.id

    def getProvince(self):
        return self.province

    def getCity(self):
        return self.city

    def getCounty(self):
        return self.county

    def getDescription(self):
        return self.description

    def getLongLat(self):
        return (self.long, self.lat)

##（5）朝代
class Temporal:
    def __init__(self, tname):
        self.prefix = "http://data.library.sh.cn/jp/data/"
        self.url = self.prefix+tname+'.json?key='+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read(8192)
##        转换为Python对象
        tt1 = json.loads(tt)
##        解析内容
        self.id = tt1['result']['uri']
        self.data = tt1['result']['data']

    def getID(self):
        return self.id

    def getData(self):
        return self.data

##帝王
class Monarch:
    def __init__(self, id):
        self.id = id
        self.monarch = None
        self.reignTitle = None
        self.monarchName = None
        self.label = None
        self.dynasty = None
        self.reignTime = None

    def getID(self):
        return self.id

    def setMonarch(self, monarch):
        self.monarch = monarch

    def getMonarch(self):
        return self.monarch

    def setReignTitle(self, rt):
        self.reignTitle = rt

    def getReignTitle(self):
        return  self.reignTitle

    def setMonarchName(self, name):
        self.monarchName = name

    def getMonarchName(self):
        return self.monarchName
    
    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def setDynasty(self, dyn):
        self.dynasty = dyn

    def getDynasty(self):
        return self.dynasty

    def setReignTime(self, rt):
        self.reignTime = rt

    def getReignTime(self):
        return self.reignTime

##返回朝代名对应的所有皇帝
class TemporalMonarch:
    def __init__(self, tname):
        self.prefix = "http://data.library.sh.cn/jp/temporal/"
        self.url = self.prefix+tname+'.json?key='+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read(8192)
##        转换为Python对象
        tt1 = json.loads(tt)
        self.monarchs = []
        for item in tt1['result']:
            monarch = Monarch(item['uri'])
##        帝王
            monarch.setMonarch(item['monarch'])
##        年号
            monarch.setReignTitle(item['reignTitle'])
##        帝王名
            monarch.setMonarchName(item['monarchName'])
##        ？？？
            monarch.setLabel(item['label'])
##        朝代
            monarch.setDynasty(item['dynasty'])
##        起始终止执政时间
            monarch.setReignTime((float(item['begin']), float(item['end'])))
##        加入帝王数组
            self.monarchs.append(monarch)

    def getMonarchs(self):
        return self.monarchs

##朝代信息
class Dynasty:
    def __init__(self, id):
        self.id = id
        self.label = None
        self.reignTime = None

    def getID(self):
        return self.id

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def setReignTime(self, rt):
        self.reignTime = rt

    def getReignTime(self):
##        TODO: 应对当前API的不完善
        res = ResFromURI(self.id)
        endYear = float(res.getJSON()[UUID_LIBRARY['endYear']])
        return (self.reignTime[0], endYear)


##获取全部的朝代
class TemporalAll:
    def __init__(self):
        self.prefix = "http://data.library.sh.cn/jp/temporal.json?key="
        self.url = self.prefix+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read(8192)
##        转换为Python对象
        tt1 = json.loads(tt)
        self.dynasties = []
        for dt in tt1['result']:
            dynasty = Dynasty(dt['uri'])
            dynasty.setLabel(dt['label'])
##            设置不可确认的朝代终止时间为-1
##            TODO: 应对当前API的不完善
            endTime = -1
            if dt['end'] != '':
                endTime = dt['end']
            dynasty.setReignTime((float(dt['begin']), float(endTime)))
            self.dynasties.append(dynasty)

    def getDynasties(self):
        return self.dynasties

class BookData:
    def __init__(self,**kwargs):
        self.prefix = "http://data.library.sh.cn/jp/work/data?"
        self.url = self.prefix+kwargs.keys()[0]+'='+kwargs[kwargs.keys()[0]]
        for key in kwargs.keys()[1:-1]:
            self.url += key+'='+kwargs[key]
        self.url += '&key='+APIKey
        f = urllib2.urlopen(self.url)
        tt = f.read()
##        转换为Python对象
        tt1 = json.loads(tt)
##        找到其中的人
        self.persons = []
        for item in tt1['@graph']:
            idd = item['@id']
            if UUID_LIBRARY['person'] in idd:
                relwork = item['relatedWork']
                pp = ThePerson(idd, relwork)
                self.persons.append(pp)

    def getPersons(self):
        return self.persons

if __name__ == "__main__":
##    fn = FamilyName("陈")
##    print fn.getID()
##    fn = Person("丁丙")
##    print fn.getFamilyName()
##    fn = Place("杞县")
##    print fn.getLongLat()
##    fn = Temporal("秦")
##    print fn.getData()
##    fn = TemporalMonarch("秦")
##    for mon in fn.getMonarchs():
##        pprint(ResFromURI(mon.getID()).getJSON())
##    fn = TemporalAll()
##    for dyn in fn.getDynasties():
##        print dyn.getLabel()
##    bd = BookData(title="上川")
##    for pp in bd.getPersons():
##        print pp.getID()
    bd = BookData(familyName="张")
    for pp in bd.getPersons():
        print pp.getID()
