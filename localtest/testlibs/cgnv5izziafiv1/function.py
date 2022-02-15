import os,Snmp,sys,time,random,odbc,glob,pyodbc
import buildkey,thread  
import struct
build_lock=thread.allocate_lock() 
#from testlibs.toolslib import *
from toolslib_local import *
from MFT512 import *
execfile("station.ini")


def SWEthConnect(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut_ap_arm, dut_ap_atom,dut_bh_arm, dut_bh_atom
    ''' 
    ip = argv[-3](argv[-2],'target_ip').strip()
    time_out = int(argv[-3](argv[-2],'time_out').strip())
    lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5,2)
    #lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2)
    for i in range(time_out):
        argv[1][2] << 'ping 1 %s 64 1'%ip
        time.sleep(1)
        data=argv[1][2].wait('%',3)[-1]
        try:
            loss = int(data.split('500 1000')[-1].split('%')[0].strip())
            if int(loss) == 0:
                argv[-4]('%s Connected....'%ip) 
                return 1
        except:
            pass
        #time.sleep(1) 

def SWEthDisConnect(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    ''' 
    argv[3](powerbutton)
    ip = argv[-3](argv[-2],'target_ip').strip()
    time_out = int(argv[-3](argv[-2],'time_out').strip())
    msg_list = map(strip,argv[-3](argv[-2],'msg').split('|'))
    lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5,2)
    #lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2)
    for i in range(time_out):
        argv[1][2] << 'ping 1 %s 64 1'%ip
        time.sleep(1)
        data=argv[1][2].wait('%',3)[-1]
        try:
            loss = int(data.split('500 1000')[-1].split('%')[0].strip())
            if int(loss) > 0:
                argv[-4]('%s DisConnected....'%ip)
                if msg_list[0]: argv[-4](msg_list[1],2) 
                return 1
        except:
            pass

def TelnetLogin(*argv):
    ETH0IP = argv[-3]('AFI','ETH0IP').split('|')
    ETH0IP_ = ETH0IP[0].strip()
    c_port = argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4
       ETH0IP_ = ETH0IP[1].strip()
    port = c_port + 1
    pid = '30%s1'%(port+1)
    timeout = int(argv[-3](argv[-2],'timeout'))
    username = argv[-3]('Base','username').strip()
    password_ = argv[-3]('Base','password_').strip()
    argv[1][-1] = lLogin(ETH0IP_,pid,username,password_)
     
   
def CheckUsSignal(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    ''' 
    term = argv[1][-1]   
    log = argv[-4]    
    system_uspower = eval(argv[-3]('Base','system_uspower'))
    uspower_offset = eval(argv[-3]('Base','uspower_offset'))
    ##### US Signal Check ######  
    for i in range(3):
        us_ok = 0
        try:
            data = lWaitCmdTerm(term,'usstatus',"Debug>",5)
            #print data
            for j in data.splitlines():
                 if 'Frquency   :' in j:
                     us_freq = j.split(":")[-1].split()
                     print us_freq
                     us_ok+=1
                 if 'rep power  :' in j:
                     us_pwr = j.split(":")[-1].split()
                     print us_pwr
                     us_ok+=1
                 if us_ok > 1: break       
        except:
            if i == 2: raise Except("ErrorCode(E00242): Parsing US Signal FAIL") 
            continue      
        #### Check US Lock #####       
        us_lock = 0
        test_fail = 0
        msg_list = []
        for j in range(len(us_freq)):
            if float(us_freq[j]) > 0: 
                us_lock+=1
                msg = "US Freq = %.2f MHz, Power = %.2f, diff = %.2f(%.2f ~ %.2f)"%(float(us_freq[j]), float(us_pwr[j]),float(us_pwr[j]) - system_uspower, uspower_offset*-1,uspower_offset)
                if abs(float(float(us_pwr[j])-system_uspower)) > uspower_offset: 
                    test_fail+=1
                else:
                    msg_list.append(msg) 
        if us_lock < 4: test_fail+=1
        else: log("US Lock PASS",2)   
        if test_fail > 0:
            if i == 2: raise Except("ErrorCode(E00242): Check US Signal FAIL")
            else:  continue
        else:
            for j in msg_list:
                log(j,2) 
            break 
    log('Check US Signal PASS',2)   
            
                 
def SnmpCheckUsSignal(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    ''' 
    term = argv[1][-1]   
    log = argv[-4]
    us_index = argv[-3](argv[-2],'us_index').split(',') 
    us_pwr_oid = argv[-3](argv[-2],'us_pwr_oid')
    us_freq_oid = argv[-3](argv[-2],'us_freq_oid')
    ipaddr = GetWanIP(term)
    system_uspower = eval(argv[-3]('Base','system_uspower'))
    uspower_offset = eval(argv[-3]('Base','uspower_offset'))
    for try_ in range(3):
        us_freq_dic = Snmp.SnmpWalk(ipaddr,us_freq_oid)
        msg_lock = "US Channel Lock: %d (%d)"%(len(us_freq_dic),len(us_index))
        if len(us_freq_dic) <> len(us_index):
            if try_ == 2: 
                log(msg_lock,1)
                raise Except("ErrorCode(E00242): US Channel Lock  FAIL")
            else: continue 
        else:
            log(msg_lock,2)
            break
    log('\n')
    test_fail = 0
    us_pwr_dic = Snmp.SnmpWalk(ipaddr,us_pwr_oid)                 
    for i in us_index:     # US power comparison
        freq = us_freq_dic["%s.%s"%(us_freq_oid,i)]
        pwr =  us_pwr_dic["%s.%s"%(us_pwr_oid,i)]/10.0
        system_uspower = cmts_uspwr[freq]
        msg_pwr = "US Freq = %.2f MHz, Measure = %.2f Report = %.2f, diff = %.2f (%.2f ~ %.2f)"%(freq//1000000.0, system_uspower,pwr,pwr - system_uspower, uspower_offset*-1,uspower_offset)
        if abs(pwr - system_uspower) > uspower_offset:
            test_fail+=1
            log(msg_pwr,1)               
        else:
            log(msg_pwr,2)
    if test_fail: raise Except("ErrorCode(E00242): US Power Check  FAIL")
        
def SnmpCheckDsSignal(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    ''' 
    term = argv[1][-1]   
    log = argv[-4]
    ds_index = argv[-3](argv[-2],'ds_index').split(',')
    ds_pwr_oid = argv[-3](argv[-2],'ds_pwr_oid')
    ds_freq_oid = argv[-3](argv[-2],'ds_freq_oid')
    ds_snr_oid = argv[-3](argv[-2],'ds_snr_oid')
    ipaddr = GetWanIP(term)
    freq_step = argv[-3]('Base','freq_step')
    system_snr = eval(argv[-3]('Base','system_snr'))
    snr_offset = eval(argv[-3]('Base','snr_offset'))
    system_dspower = eval(argv[-3]('Base','system_dspower'))
    dspower_offset = eval(argv[-3]('Base','dspower_offset'))
    
    ds_chanel =eval(argv[-3]('Base','ds_chanel'))
    for try_ in range(3):
        ds_freq_dic = Snmp.SnmpWalk(ipaddr,ds_freq_oid)
        msg_lock = "DS Channel Lock: %d (%d)"%(len(ds_freq_dic),len(ds_index))
        if len(ds_freq_dic) <> len(ds_index):
            if try_ == 2: 
                log(msg_lock,1)
                raise Except("ErrorCode(E00242): %s DS Channel Lock  FAIL"%ipaddr)
            else: continue
        else:
            log(msg_lock,2)
            break
    log('\n')
    test_fail = 0
    ds_pwr_dic = Snmp.SnmpWalk(ipaddr,ds_pwr_oid)                 
    for i in ds_index:     # US power comparison
        freq = ds_freq_dic["%s.%s"%(ds_freq_oid,i)]
        pwr =  ds_pwr_dic["%s.%s"%(ds_pwr_oid,i)]/10.0
        system_dspower = cmts_dspwr[freq]
        msg_pwr = "DS Freq = %.2f MHz, Measure = %.2f Report = %.2f, diff = %.2f (%.2f ~ %.2f)"%(freq/1000000.0,system_dspower, pwr,pwr - system_dspower, dspower_offset*-1,dspower_offset)
        if abs(pwr - system_dspower) > dspower_offset:
            test_fail+=1 
            log(msg_pwr,1)
        else:
            log(msg_pwr,2)
    if test_fail: raise Except("ErrorCode(E00242): %s DS Power Check  FAIL"%ipaddr)            
    log('\n')            
    test_fail = 0
    ds_snr_dic = Snmp.SnmpWalk(ipaddr,ds_snr_oid)                 
    for i in ds_index:     # US power comparison
        freq = ds_freq_dic["%s.%s"%(ds_freq_oid,i)]
        snr =  ds_snr_dic["%s.%s"%(ds_snr_oid,i)]/10.0
        msg_snr = "DS Freq = %.2f MHz, SNR = %.2f ( > %.2f)"%(freq/1000000.0, snr,system_snr)
        if snr < system_snr:
            test_fail+=1 
            log(msg_snr,1)
        else:
            log(msg_snr,2)
    if test_fail: raise Except("ErrorCode(E00242): %s DS SNR Check  FAIL"%ipaddr)              
         
