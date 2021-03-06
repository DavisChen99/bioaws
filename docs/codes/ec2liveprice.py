import io
import sys
import os
import re
import platform
from optparse import OptionParser
from bs4 import BeautifulSoup

from optparse import OptionParser
usage = "usage: %prog [options] InstanceType"
parser = OptionParser(usage)
parser.add_option('-m','--mode',type='str',default = 'off', help = 'off/on/update (off by default)')
parser.add_option('-t','--type',type='str',default = 'ri', help = 'od/do/ri/dri/cri/cdri (ri by default)')
parser.add_option('-s','--os',type='str',default = 'li', help = 'li/win/su/rh/wsqs/wsqw/wsqe (li by default)')
parser.add_option('-r','--region',type='str',default = 'zhy', help = 'bjs/zhy (zhy by default)')
parser.add_option("-p", action = "store_false",dest = "abb", default = True, help = "print abbrevs to stdout") 

option,args = parser.parse_args(sys.argv)

smode = option.mode
instype = option.type
osystem = option.os
region = option.region

index = args[1:]

## get current dir and set lib dir
currentdir = os.path.dirname(__file__)  # 当前文件所在的目录
pathdir = '%s/lib/' % currentdir

# judge the system type then set wgetdir
wgetdir = ''
if 'Windows' in platform.platform():
    mysystem = 'Windows'
    wgetdir = '%s/bin/wget.exe' %  currentdir
else:
    mysystem = 'Non-Windows'
    wgetdir = 'wget'

if not os.path.exists(pathdir):
    os.mkdir(pathdir)
    smode = 'update'
    print ('> no local lib, set mode to update, please try again after lib updated...')

# paths combine
pathdir.strip()
html_linux = pathdir + 'ec2_linux.html'
html_rhel = pathdir + 'ec2_rhel.html'
html_suse = pathdir + 'ec2_suse.html'
html_win = pathdir + 'ec2_win.html'
html_win_sqlstd = pathdir + 'ec2_win_sqlstd.html'
html_win_sqlweb = pathdir + 'ec2_win_sqlweb.html'
html_win_sqlent = pathdir + 'ec2_win_sqlent.html'

parse_linux = pathdir + 'ec2_linux'
parse_rhel = pathdir + 'ec2_rhel'
parse_suse = pathdir + 'ec2_suse'
parse_win = pathdir + 'ec2_win'
parse_win_sqlstd = pathdir + 'ec2_win_sqlstd'
parse_win_sqlweb = pathdir + 'ec2_win_sqlweb'
parse_win_sqlent = pathdir + 'ec2_win_sqlent'

# partial urls
pri_linux = 'ec2/pricing/ec2-linux-pricing/'
pri_rhel = 'ec2/pricing/ec2-rhel-pricing/'
pri_suse = 'ec2/pricing/ec2-suse-pricing/'
pri_win = 'ec2/pricing/ec2-windows-pricing/'
pri_win_sqlstd = 'ec2/pricing/ec2-windows-with-sql-standard-pricing/'
pri_win_sqlweb = 'ec2/pricing/ec2-windows-with-sql-web-pricing/'
pri_win_sqlent = 'ec2/pricing/ec2-windows-with-sql-server-enterprise-pricing/'

# dictionary for abreviations
translate = {'bjs': '北京区域', 
             'zhy': '宁夏区域', 
             'od': '按需实例',
             'do': '专用按需实例',
             'ri': '预留实例',
             'dri': '专用预留实例',
             'cri': '可转换实例',
             'cdri': '可转换专用预留实例',
             'li': 'EC2 Linux',
             'win': 'EC2 Windows',
             'su': 'EC2 SUSE',
             'rh': 'EC2 RHEL',
             'wsqs': '采用 SQL Standard 的 EC2 Windows',
             'wsqw': '采用 SQL Web 的 EC2 Windows',
             'wsqe': '采用 SQL Server Enterprise 的 EC2 Windows'
             }

if not option.abb:
    print ('\nAbbreviations:')
    for key in translate:
        print ('%s <---> %s' % (key,translate[key]))

# function for judge the url we open or download
def geturl(osystem):
    if osystem == 'li':
        myurl = 'https://www.amazonaws.cn/en/' + pri_linux
        myfile = html_linux
        myparse = parse_linux
    elif osystem == 'rh':
        myurl = 'https://www.amazonaws.cn/en/' + pri_rhel
        myfile = html_rhel
        myparse = parse_rhel
    elif osystem == 'su':
        myurl = 'https://www.amazonaws.cn/en/' + pri_suse
        myfile = html_suse
        myparse = parse_suse
    elif osystem == 'win':
        myurl = 'https://www.amazonaws.cn/en/' + pri_win
        myfile = html_win
        myparse = parse_win
    elif osystem == 'wsqs':
        myurl = 'https://www.amazonaws.cn/en/' + pri_win_sqlstd
        myfile = html_win_sqlstd
        myparse = parse_win_sqlstd
    elif osystem == 'wsqw':
        myurl = 'https://www.amazonaws.cn/en/' + pri_win_sqlweb
        myfile = html_win_sqlweb
        myparse = parse_win_sqlweb
    elif osystem == 'wsqe':
        myurl = 'https://www.amazonaws.cn/en/' + pri_win_sqlent
        myfile = html_win_sqlent
        myparse = parse_win_sqlent
    else:
        raise ValueError('wrong os option, please check usage by <python thisscript.py -h>')
        sys.exit(0)
    return myurl,myfile,myparse

# function to set table list according to diff option:
odhead = '实例类型 | vCPU | ECU | 内存 | 存储 | OD价格（人民币）/每小时'
rihead = '实例类型 | 期限 | 产品类型 | 预付价格（人民币） | 使用价格（人民币） | 月度成本（人民币） | 有效RI率 | 与OD相比的成本节省 | OD价格（人民币）/每小时'
myhead = ''

def getablenum(region,instype,os):
    if region == 'bjs':
        if os == 'wsqe': # 37
            if instype == 'od':
                tnum = 19
                myhead = odhead
            elif instype == 'do':
                tnum = 20
                myhead = odhead
            elif instype == 'ri':
                tnum = 21
                myhead = rihead
            elif instype == 'dri':
                tnum = 25
                myhead = rihead
            elif instype == 'cri':
                tnum = 29
                myhead = rihead
            elif instype == 'cdri':
                tnum = 33
                myhead = rihead
            else:
                raise ValueError('wrong instype option, please check usage by <python thisscript.py -h>')
                sys.exit(0)
        else: # 44
            if instype == 'od':
                tnum = 22
                myhead = odhead
            elif instype == 'do':
                tnum = 23
                myhead = odhead
            elif instype == 'ri':
                tnum = 24
                myhead = rihead
            elif instype == 'dri':
                tnum = 29
                myhead = rihead
            elif instype == 'cri':
                tnum = 34
                myhead = rihead
            elif instype == 'cdri':
                tnum = 39
                myhead = rihead
            else:
                raise ValueError('wrong instype option, please check usage by <python thisscript.py -h>')
                sys.exit(0)
    elif region == 'zhy':
        if os == 'wsqe':
            if instype == 'od':
                tnum = 0
                myhead = odhead
            elif instype == 'do':
                tnum = 2
                myhead = odhead
            elif instype == 'ri':
                tnum = 3
                myhead = rihead
            elif instype == 'dri':
                tnum = 7
                myhead = rihead
            elif instype == 'cri':
                tnum = 11
                myhead = rihead
            elif instype == 'cdri':
                tnum = 15
                myhead = rihead
            else:
                raise ValueError('wrong instype option, please check usage by <python thisscript.py -h>')
                sys.exit(0)
        else:
            if instype == 'od':
                tnum = 0
                myhead = odhead
            elif instype == 'do':
                tnum = 1
                myhead = odhead
            elif instype == 'ri':
                tnum = 2
                myhead = rihead
            elif instype == 'dri':
                tnum = 7
                myhead = rihead
            elif instype == 'cri':
                tnum = 12
                myhead = rihead
            elif instype == 'cdri':
                tnum = 17
                myhead = rihead
            else:
                raise ValueError('wrong instype option, please check usage by <python thisscript.py -h>')
                sys.exit(0)
    else:
        raise ValueError('wrong region option, please check usage by <python thisscript.py -h>')
        sys.exit(0)
    return tnum, myhead
# set public vars
myurl= []
addr = ''
htmlfile = ''
parsefile = ''
deepfile = ''
downloader= ''

# search mode :online, offline, update only
systemlist = ['li','win','su','rh','wsqs','wsqw','wsqe']
allnum = [0,1,2,7,12,17,22,23,24,29,34,39]
sqlentnum = [0,2,3,7,11,15,19,20,21,25,29,33]
mygetnum = ''

myurl = geturl(osystem)
addr = myurl[0]
htmlfile = myurl[1]
parsefile = myurl[2]

myget = getablenum(region,instype,osystem)
mygetnum = myget[0]
myhead = myget[1]

if smode == 'off' and option.abb:
    print ('[offline mode]')
elif smode == 'on':
    print ('[online mode]')
    downloader = '%s %s -O %s' % (wgetdir,addr,htmlfile)
    os.system(downloader)
    soup = BeautifulSoup(open(htmlfile,encoding='utf-8'),features='html.parser')
    tables = soup.findAll('table')
    deepfile = '%s_%s.txt' % (parsefile,mygetnum)
    if 'win_sqlent' in parsefile:
        # if mygetnum == '0':
        #     deepfile = '%s_%s.txt' % (parsefile,mygetnum)
        # else:
        mylist = ''
        if instype in ['od','do']:
            tab = tables[mygetnum]
            for tr in tab.tbody.findAll('tr'):
                for td in tr.findAll('td'):
                    text = td.getText()
                    if 'SSD' in text:
                        mylist += text.ljust(20)
                    elif 'Upfront' in text:
                        mylist += text.ljust(18)
                    elif 'yr' in text:
                        mylist += text.ljust(6)
                    else:
                        mylist += text.ljust(15)
                    #mylist += text + ' | '
                mylist += '\n'
            fp = open(deepfile,"w",encoding='utf-8')
            fp.write(mylist)
            fp.close()
        else:
            for i in range(0,4):
                mynewnum = mygetnum + i
                tab = tables[mynewnum]
                for tr in tab.tbody.findAll('tr'):
                    for td in tr.findAll('td'):
                        text = td.getText()
                        if 'SSD' in text:
                            mylist += text.ljust(20)
                        elif 'Upfront' in text:
                            mylist += text.ljust(18)
                        elif 'yr' in text:
                            mylist += text.ljust(6)
                        else:
                            mylist += text.ljust(15)
                        #mylist += text + ' | '
                    mylist += '\n'
            fp = open(deepfile,"w",encoding='utf-8')
            fp.write(mylist)
            fp.close()
    else:
        mylist = ''
        if instype in ['od','do']:
            tab = tables[mygetnum]
            for tr in tab.tbody.findAll('tr'):
                for td in tr.findAll('td'):
                    text = td.getText()
                    if 'SSD' in text:
                        mylist += text.ljust(20)
                    elif 'Upfront' in text:
                        mylist += text.ljust(18)
                    elif 'yr' in text:
                        mylist += text.ljust(6)
                    else:
                        mylist += text.ljust(15)
                    #mylist += text + ' | '
                mylist += '\n'
            fp = open(deepfile,"w",encoding='utf-8')
            fp.write(mylist)
            fp.close()
        else:
            for i in range(0,5):
                mynewnum = mygetnum + i
                tab = tables[mynewnum]
                for tr in tab.tbody.findAll('tr'):
                    for td in tr.findAll('td'):
                        text = td.getText()
                        if 'SSD' in text:
                            mylist += text.ljust(20)
                        elif 'Upfront' in text:
                            mylist += text.ljust(18)
                        elif 'yr' in text:
                            mylist += text.ljust(6)
                        else:
                            mylist += text.ljust(15)
                        #mylist += text + ' | '
                    mylist += '\n'
            fp = open(deepfile,"w",encoding='utf-8')
            fp.write(mylist)
            fp.close()
    print ('> updated :)')
elif smode == 'update':
    print ('[update mode]')
    for myos in systemlist:
        myurl = geturl(myos)
        addr = myurl[0]
        htmlfile = myurl[1]
        parsefile = myurl[2]
        downloader = '%s %s -O %s' % (wgetdir,addr,htmlfile)
        os.system(downloader)
        # use BeautifulSoup to parse html
        soup = BeautifulSoup(open(htmlfile,encoding='utf-8'),features='html.parser')
        tables = soup.findAll('table')
        if 'win_sqlent' in parsefile:
            for count in sqlentnum: 
                deepfile = '%s_%s.txt' % (parsefile,count)
                mylist = ''
                if count in [0,2,19,20]:
                    tab = tables[count]
                    for tr in tab.tbody.findAll('tr'):
                        for td in tr.findAll('td'):
                            text = td.getText()
                            if 'SSD' in text:
                                mylist += text.ljust(20)
                            elif 'Upfront' in text:
                                mylist += text.ljust(18)
                            elif 'yr' in text:
                                mylist += text.ljust(6)
                            else:
                                mylist += text.ljust(15)
                            #mylist += text + ' | '
                        mylist += '\n'
                    fp = open(deepfile,"w",encoding='utf-8')
                    fp.write(mylist)
                    fp.close()
                else:
                    for i in range(0,4):
                        newcount = count + i
                        tab = tables[newcount]
                        for tr in tab.tbody.findAll('tr'):
                            for td in tr.findAll('td'):
                                text = td.getText()
                                if 'SSD' in text:
                                    mylist += text.ljust(20)
                                elif 'Upfront' in text:
                                    mylist += text.ljust(18)
                                elif 'yr' in text:
                                    mylist += text.ljust(6)
                                else:
                                    mylist += text.ljust(15)
                                #mylist += text + ' | '
                            mylist += '\n'
                    fp = open(deepfile,"w",encoding='utf-8')
                    fp.write(mylist)
                    fp.close()
        else:
            for count in allnum: 
                deepfile = '%s_%s.txt' % (parsefile,count)
                mylist = ''
                if count in [0,1,22,23]:
                    tab = tables[count]
                    for tr in tab.tbody.findAll('tr'):
                        for td in tr.findAll('td'):
                            text = td.getText()
                            if 'SSD' in text:
                                mylist += text.ljust(20)
                            elif 'Upfront' in text:
                                mylist += text.ljust(18)
                            elif 'yr' in text:
                                mylist += text.ljust(6)
                            else:
                                mylist += text.ljust(15)
                            #mylist += text + ' | '
                        mylist += '\n'
                    fp = open(deepfile,"w",encoding='utf-8')
                    fp.write(mylist)
                    fp.close()
                else:
                    for i in range(0,5):
                        newcount = count + i
                        tab = tables[newcount]
                        for tr in tab.tbody.findAll('tr'):
                            for td in tr.findAll('td'):
                                text = td.getText()
                                if 'SSD' in text:
                                    mylist += text.ljust(20)
                                elif 'Upfront' in text:
                                    mylist += text.ljust(18)
                                elif 'yr' in text:
                                    mylist += text.ljust(6)
                                else:
                                    mylist += text.ljust(15)
                                #mylist += text + ' | '
                            mylist += '\n'
                    fp = open(deepfile,"w",encoding='utf-8')
                    fp.write(mylist)
                    fp.close()
    print ('\n> update job finished :)\n> start your query!')
    sys.exit(0)





# set vars
name = ''
lawer = 0

if index:
    print ('\n[%s - %s - %s]\n' % (translate[region], translate[osystem], translate[instype]))
    print (myhead)
    deepfile = '%s_%s.txt' % (parsefile,mygetnum)
    with open(deepfile,'r',encoding='UTF-8') as a:
        for each_line in a:
            line = each_line.strip('\n')
            for name in index:
                if re.search(name, line, re.IGNORECASE):
                    print (line)
                    lawer = 1
    if not lawer:
        print ('no such instance...\n')
else:
    if option.abb:
        print ('please tell me instance type...\n')


#   0 --- 按需 (OD) 实例  ZHY
#   1 --- 专用按需 (OD) 实例 ZHY
#   2 --- 预留实例 (RI) ZHY
#   3 --- 专用预留实例 (RI) ZHY
#   4 --- 可转换预留实例 (RI) ZHY
#   5 --- 可转换专用预留实例 (RI) ZHY
#   6 --- 按需 (OD) 实例 BJS
#   7 --- 专用按需 (OD) 实例 BJS
#   8 --- 预留实例 (RI) BJS
#   9 --- 专用预留实例 (RI) BJS
#  10 --- 可转换预留实例 (RI) BJS
#  11 --- 可转换专用预留实例 (RI) BJS
