#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 20:50:40 2016

@author: wangqiushi
"""
# 导入库
import os
import sys
import shutil
import pickle
import bibtexparser


# 全局变量

path = os.path.abspath(os.path.dirname(sys.argv[0])) #当前路径
dbAddr = '/db.pkl' #数据库文件地址
dataAddr = '/data' #文献保存地址
#dbAddr = '/dbBeta.pkl' #调试
#dataAddr = '/dataBeta' #调试

# init(), 初始化函数, 负责创建带头的空数据库文件
def init():
    head = {'globalID':0}
    database = [head]
    dbp = open(path + dbAddr, 'wb')
    pickle.dump(database, dbp, 2)
    dbp.close()
    
# newPN = new(), 新建一个空数据项
def new():
    newPN = {'ID':'',\
             'author':'',\
             'journal':'',\
             'title':'',\
             'year':'',\
             'volume':'',\
             'number':'',\
             'pages':'',\
             'doi':'',\
             'ISSN':'',\
             'month':'',\
             'keyword':'',\
             'abstract':'',\
             'comment':'',\
             'link':'',\
             'tag':''} 
    return(newPN)
    

# outlist = str2list(string), 将以';'分隔的字符串转换为字符串列表的函数
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

 # outstr = list2str(inputlist), 将字符串列表转换为以';'分隔的字符串的函数
def list2str(inputlist):
    outstr = ''
    for i in range(len(inputlist)):
        outstr = outstr + inputlist[i] + ';'
    return(outstr)

# info = datainfo(dataFolder), 返回data文件夹的目录信息
def datainfo(dataFolder):
    info = {'IDstr':'',\
            'IDnum':'',\
            'IDmin':'',\
            'IDmax':''}
    IDlist = os.listdir(dataFolder)

    intIDlist = []
    for i in range(len(IDlist)):
        intIDlist.append(int(IDlist[i]))
    intIDlist.sort()
    for i in range(len(intIDlist)):
        IDlist[i] = str(intIDlist[i])
    info['IDstr'] = list2str(IDlist)    
    info['IDnum'] = str(len(intIDlist))
    info['IDmin'] = str(min(intIDlist))
    info['IDmax'] = str(max(intIDlist))
    return(info)
    

# insert(bibAddr), 命令insert bibAddr (pdfAddr), 用于插入新数据项 
def insert(bibAddr, pdfAddr):
    with open(path + '/' + bibAddr) as bibFile:
        bibStr = bibFile.read()
    bibLoad = bibtexparser.loads(bibStr)
    bibData = bibLoad.entries[0]
    
    dbpr = open(path + dbAddr, 'rb')
    database = pickle.load(dbpr)
    dbpr.close()
    head = database[0]

    ID = head['globalID'] + 1
    strID = (8-len(str(ID)))*'0' + str(ID)
    
    newPN = new()
    newPN['ID'] = strID
    
    if bibData.has_key('author'):
        newPN['author'] = bibData['author']
    if bibData.has_key('journal'):
        newPN['journal'] = bibData['journal']
    if bibData.has_key('title'):
        newPN['title'] = bibData['title']
    if bibData.has_key('year'):
        newPN['year'] = bibData['year']
    if bibData.has_key('volume'):
        newPN['volume'] = bibData['volume']
    if bibData.has_key('number'):
        newPN['number'] = bibData['number']
    if bibData.has_key('pages'):
        newPN['pages'] = bibData['pages']
    if bibData.has_key('doi'):
        newPN['doi'] = bibData['doi']
    if bibData.has_key('issn'):
        newPN['ISSN'] = bibData['issn']
    if bibData.has_key('month'):
        newPN['month'] = bibData['month']
    if bibData.has_key('keyword'):
        newPN['keyword'] = bibData['keyword']
    if bibData.has_key('abstract'):
        newPN['abstract'] = bibData['abstract']
    if bibData.has_key('comment'):
        newPN['comment'] = bibData['comment']
    if bibData.has_key('tag'):
        newPN['tag'] = bibData['tag']
    
    saveAddr = path + dataAddr + '/' +strID
    os.mkdir(saveAddr)
    shutil.move(path + '/' + bibAddr, saveAddr)
    os.rename(saveAddr + '/' + bibAddr, saveAddr + '/' + strID + '.bib')
    
    if pdfAddr != 'none':
        shutil.move(path + '/' + pdfAddr, saveAddr)
        localpdfAddr = dataAddr + '/' + strID + '/' + pdfAddr
        newPN['link'] = localpdfAddr
        
    database.append(newPN)
    head['globalID'] = ID
    database[0] = head
    
    dbpw = open(path + dbAddr, 'wb')
    pickle.dump(database, dbpw, 2)
    dbpw.close()
    print
    print('Insert ID: ' + strID + ' successfully!')
    print('\n')
    return(strID)
    
# modify(ID), 命令modify ID, 用于修改数据项内容 
def modify(ID):
    strID = (8-len(str(ID)))*'0' + str(ID)
    
    dbpr = open(path + dbAddr, 'rb')
    database = pickle.load(dbpr)
    dbpr.close()
    head = database[0]
    globalID = head['globalID']

    
    if (ID <= globalID) and (database[ID]['ID'] != '-1'):

        saveAddr = path + dataAddr + '/' +strID
        with open(saveAddr + '/' + strID + '.bib') as bibFile:
            bibStr = bibFile.read()
        bibLoad = bibtexparser.loads(bibStr)
        bibData = bibLoad.entries[0]
        
        PN = database[ID]

        if bibData.has_key('author'):
            PN['author'] = bibData['author']
        if bibData.has_key('journal'):
            PN['journal'] = bibData['journal']
        if bibData.has_key('title'):
            PN['title'] = bibData['title']
        if bibData.has_key('year'):
            PN['year'] = bibData['year']
        if bibData.has_key('volume'):
            PN['volume'] = bibData['volume']
        if bibData.has_key('number'):
            PN['number'] = bibData['number']
        if bibData.has_key('pages'):
            PN['pages'] = bibData['pages']
        if bibData.has_key('doi'):
            PN['doi'] = bibData['doi']
        if bibData.has_key('issn'):
            PN['ISSN'] = bibData['issn']
        if bibData.has_key('month'):
            PN['month'] = bibData['month']
        if bibData.has_key('keyword'):
            PN['keyword'] = bibData['keyword']
        if bibData.has_key('abstract'):
            PN['abstract'] = bibData['abstract']
        if bibData.has_key('comment'):
            PN['comment'] = bibData['comment']
        if bibData.has_key('tag'):
            PN['tag'] = bibData['tag']
    
        database[ID] = PN
        dbpw = open(path + dbAddr, 'wb')
        pickle.dump(database, dbpw, 2)
        dbpw.close()
        print
        print('Modify ID: ' + strID + ' successfully!')
        print('\n')
        return(1)
    else:
        print
        print('ID: ' + strID + ' does not exist.')
        print('\n')
        return(-1)
            

    
# remove(ID), 命令remove ID, 用于删除数据项内容, ID置为-1, 数据库顺序不变
def remove(ID):   
    strID = (8-len(str(ID)))*'0' + str(ID)
    
    dbpr = open(path + dbAddr, 'rb')
    database = pickle.load(dbpr)
    dbpr.close()
    head = database[0]
    globalID = head['globalID']
    
    if (ID <= globalID) and (database[ID]['ID'] != '-1'):
        PN = database[ID]
        PN['ID'] = '-1'
        PN.pop('author')
        PN.pop('journal')
        PN.pop('title')
        PN.pop('year')
        PN.pop('volume')
        PN.pop('number')
        PN.pop('pages')
        PN.pop('doi')
        PN.pop('ISSN')
        PN.pop('month')
        PN.pop('keyword')
        PN.pop('abstract')
        PN.pop('comment')
        PN.pop('tag')
    
        database[ID] = PN
        dbpw = open(path + dbAddr, 'wb')
        pickle.dump(database, dbpw, 2)
        dbpw.close()
    

        saveAddr = path + dataAddr + '/' +strID
        shutil.rmtree(saveAddr)
        print
        print('Remove ID: ' + strID + ' successfully!')
        print('\n')
    else:
        print
        print('ID: ' + strID + ' does not exist.')
        print('\n')
    

# show(item, ID), 命令show, 用于显示数据项
def show(item, ID):
    itemlist = str2list(item)
    IDlist = str2list(ID)
    intIDlist = []
    for i in range(len(IDlist)):
        intIDlist.append(int(IDlist[i]))
        
    dbpr = open(path + dbAddr, 'rb')
    database = pickle.load(dbpr)
    dbpr.close()
    head = database[0]   

    globalID = head['globalID']


    for i in intIDlist:
        print
        if (i <= globalID) and (database[i]['ID'] != '-1'):
            print('ID: ' + database[i]['ID'])
            if ('author' in itemlist) and (database[i]['author'] != ''):
                print('Author: ' + database[i]['author'])
            if ('title' in itemlist) and (database[i]['title'] != ''):
                print('Title: ' + database[i]['title'])
            if ('journal' in itemlist) and (database[i]['journal'] != ''):
                print('Journal: ' + database[i]['journal'])
            if ('year' in itemlist) and (database[i]['year'] != ''):
                print('Year: ' + database[i]['year'])
            if ('month' in itemlist) and (database[i]['month'] != ''):
                print('Month: ' + database[i]['month'])
            if ('volume' in itemlist) and (database[i]['volume'] != ''):
                print('Volume: ' + database[i]['volume'])
            if ('number' in itemlist) and (database[i]['number'] != ''):
                print('Number: ' + database[i]['number'])
            if ('pages' in itemlist) and (database[i]['pages'] != ''):
                print('Pages: ' + database[i]['pages'])
            if ('doi' in itemlist) and (database[i]['doi'] != ''):
                print('Doi: ' + database[i]['doi'])
            if ('ISSN' in itemlist) and (database[i]['ISSN'] != ''):
                print('ISSN: ' + database[i]['ISSN'])
            if ('keyword' in itemlist) and (database[i]['keyword'] != ''):
                print('Keyword: ' + database[i]['keyword'])
            if ('abstract' in itemlist) and (database[i]['abstract'] != ''):
                print('Abstract: ' + database[i]['abstract'])
            if ('comment' in itemlist) and (database[i]['comment'] != ''):
                print('Comment: ' + database[i]['comment'])
            if ('link' in itemlist) and (database[i]['link'] != ''):
                print('Link: ' + database[i]['link'])
            if ('tag' in itemlist) and (database[i]['tag'] != ''):
                print('Tag: ' + database[i]['tag'])

        else: 
            stri = (8-len(str(i)))*'0' + str(i)
            print('ID: ' + stri + ' does not exist.')

    print('\n')
    
# search(item, target), 命令search item target, 
# 用于在指定item中的全部ID中搜索target字符串， 不区分大小写
def search(item, target):
    dbpr = open(path + dbAddr, 'rb')
    database = pickle.load(dbpr)
    dbpr.close()
    head = database[0]   
    globalID = head['globalID']

    if os.name == 'posix':
        utarget = unicode(target, 'utf-8') #转换为unicode, 方便处理汉字
    elif os.name == 'nt':
        utarget = target.decode('gbk')

    findID = []
    for i in range(1, globalID + 1):
        if database[i]['ID'] != '-1':
            if utarget.lower() in database[i][item].lower():
                findID.append(database[i]['ID'])
    
    findnum = len(findID)
    print
    print('Search ' + '\'' + target + '\'' + ' in ' + '\'' + item + '\'.')
    print
    if findnum != 0:
        print('Find ' + str(findnum) + ' matches.')
        print(findID)
        show(item, list2str(findID))
    else:
        print('Find ' + str(findnum) + ' matches.')
        print('\n')

# tag(), 命令tag，用于显示所有tag集合
def tag():
    dbpr = open(path + dbAddr, 'rb')
    database = pickle.load(dbpr)
    dbpr.close()
    head = database[0]   
    globalID = head['globalID']

    taglist = []
    for i in range(1, globalID + 1):
        if database[i]['ID'] != '-1':
            taglist.extend(str2list(database[i]['tag']))

    tagset = list(set(taglist))
    print
    print('Tag set is:')
    print('[' + list2str(tagset) + ']')
    print('\n')
            
    

# cmd = command(), 负责处理输入命令   
def command(args):
    cmdlist = ['insert', 'modify', 'remove', 'show', 'search', 'tag']
    allItem = 'author;title;journal;year;month;volume;number;' + \
              'pages;doi;ISSN;keyword;abstract;comment;link;tag'
    dataFolder = path + dataAddr
    info = datainfo(dataFolder)

    if len(args) == 1:
        print
        print('Please select a command.')
        print(cmdlist)
        print
        print('insert bibAddr (pdfAddr)')
        print('modify ID')
        print('remove ID')
        print('show (items = all) (IDs = all)')
        print('search item target')
        print('tag')
        print('\n')
    else:
        if args[1] == 'insert':
            if len(args) == 2:
                print
                print('Not enough argument.')
                print('\n')
            elif len(args) == 3:
                strID = insert(args[2], 'none')
                show(allItem, strID)
            elif len(args) >= 4:
                strID = insert(args[2], args[3])
                show(allItem, strID)

        elif args[1] == 'modify':
            if len(args) == 2:
                print
                print('Not enough argument.')
                print('\n')
            elif len(args) >= 3:
                ID = int(args[2])
                exitcode = modify(ID)
                if exitcode == 1:
                    show(allItem, str(ID))

        elif args[1] == 'remove':
            if len(args) == 2:
                print
                print('Not enough argument.')
                print('\n')
            elif len(args) >= 3:
                ID = int(args[2])
                remove(ID)
    
        elif args[1] == 'show':
            
            if len(args) == 2:
                item = 'all'
                ID = 'all'
            elif len(args) == 3:
                item = args[2]
                ID = 'all'
            elif len(args) >= 4:
                item = args[2]
                ID = args[3]
            
            if item == 'all':
                item = allItem
            if ID == 'all':
                ID = info['IDstr']
            show(item, ID)
        
        elif args[1] == 'search':
            if len(args) <= 3:
                print
                print('Not enough argument.')
                print('\n')
            elif len(args) >=4:
                item = args[2]
                target = args[3]
                if item in str2list(allItem):
                    search(item, target)
                else:
                    print
                    print('No such item \'' + item + \
                          '\',' + ' please select an item.')
                    print(str2list(allItem))
                    print('\n')

        elif args[1] == 'tag':
            tag()
            
        else:
            print
            print('No such command \'' + args[1] + \
                  '\',' + ' please select a command.')
            print(cmdlist)
            print('\n')
    

    
if __name__ == '__main__':
    args = sys.argv #输入参数列表
    #init()
    command(args)

    

    





