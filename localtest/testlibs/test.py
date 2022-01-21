import time 
from .term_3 import *

def lLogin(m):
    m.msg('Telnet login Start') 
    mac, iface = iface_ip_get_mac('192.168.100.10')
    dstmac = (':'.join(m.mac[i:i+2] for i in range(0, len(m.mac), 2)))
    m.msg(mac)
    m.msg(dstmac)
    m.term=TelnetLayer2(mac,'192.168.100.10',dstmac,'192.168.100.1',iface)
    m.msg(m.term.wait('login',10))
    m.msg(lWaitCmdTerm(m.term,'msoadmin',':',5))
    m.msg(lWaitCmdTerm(m.term,'password','Menu>',10))
    m.msg(lWaitCmdTerm(m.term,'doc','sis>',10))
    m.msg(lWaitCmdTerm(m.term,'ven','sis>',10))
    m.msg(lWaitCmdTerm(m.term,'dir','sis>',10))
    #term=Telnet(dstip,pid,3)
    # data = m.term.wait("login:",15)[-1]
    #print '[%s]%s'%(time.ctime(),data)
    #print username
    #print password
    # m.term << 'root'
    # time.sleep(1)
    # m.term << 'iamgroot'
    # time.sleep(1)
    # m.msg(m.term.wait('#',10)[-1])

def prodshow(m):
    lWaitCmdTerm(m.term,'cli','Menu>',5)
    lWaitCmdTerm(m.term,'doc','sis>',5)
    lWaitCmdTerm(m.term,'Prod','tion>',5)
    m.msg(lWaitCmdTerm(m.term,'prodshow','tion>',5))

def Test1(m):
    m.msg(lWaitCmdTerm(m.term,'Prod','tion>',10))
    m.msg(lWaitCmdTerm(m.term,'Cal','tion>',10))
    m.msg(lWaitCmdTerm(m.term,'Up','tion>',10))
    m.msg(lWaitCmdTerm(m.term,'print 1','tion>',10))

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

