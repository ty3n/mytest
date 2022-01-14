import time 
from .term_3 import *

def lLogin(m):
    m.msg('Telnet login Start') 
    m.msg(m.ip)
    m.term = Telnet('192.168.100.1',m.ip)
    #term=Telnet(dstip,pid,3)
    data = m.term.wait("login:",15)[-1]
    #print '[%s]%s'%(time.ctime(),data)
    #print username
    #print password
    m.term << 'root'
    time.sleep(1)
    m.term << 'iamgroot'
    time.sleep(1)
    m.msg(m.term.wait('#',10)[-1])

def prodshow(m):
    lWaitCmdTerm(m.term,'cli','Menu>',5)
    lWaitCmdTerm(m.term,'doc','sis>',5)
    lWaitCmdTerm(m.term,'Prod','tion>',5)
    m.msg(lWaitCmdTerm(m.term,'prodshow','tion>',5))

def Test1(m):
    time.sleep(2)
    m.msg('Test1')

def Test2(m):
    time.sleep(1)
    m.msg('Test2')

def Test3(m):
    time.sleep(2)
    m.msg('Test3')

def Test4(m):
    time.sleep(3)
    m.msg('Test4')

def Test5(m):
    time.sleep(3)
    m.msg('Test5')

def Test6(m):
    time.sleep(3)
    m.msg('Test6')

def Test7(m):
    time.sleep(3)
    m.msg('Test7')

def Test8(m):
    time.sleep(3)
    m.msg('Test8')

