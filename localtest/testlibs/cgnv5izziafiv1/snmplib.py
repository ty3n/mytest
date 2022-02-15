# SNMP Manufacturing functions
import os,Snmp,htx
from toolslib_local import *
from MFT512 import *

##### SNMP OIDs
ifPhysAddress2_OID = ".1.3.6.1.2.1.2.2.1.6.2"
docsDevServerBootState_OID = ".1.3.6.1.2.1.69.1.4.1"
modemProdResetAccessStart_OID = ".1.3.6.1.4.1.8595.1.400.2.1.1.8.0"
modemCmTelnetAccessEnable_OID = ".1.3.6.1.4.1.8595.1.400.3.1.9.0"
modemProdCommandLine_OID = ".1.3.6.1.4.1.8595.1.400.4.1.9.0"
modemProdSwBank_OID = "1.3.6.1.4.1.8595.1.400.2.1.2.40.5.1.1.0"
docsIfCmStatusValue_OID = ".1.3.6.1.2.1.10.127.1.2.2.1.1.2"
docsIfSigQSignalNoise_OID = ".1.3.6.1.2.1.10.127.1.1.4.1.5.3"
docsIfDownChannelPower_OID = ".1.3.6.1.2.1.10.127.1.1.1.1.6.3"
docsIfCmStatusTxPower_OID = ".1.3.6.1.2.1.10.127.1.2.2.1.3.2"
sysDescr_OID = "1.3.6.1.2.1.1.1.0"
transmissionatMAC='1.3.6.1.2.1.10.127.1.3.3.1.2'
transmissionatIPAddress='1.3.6.1.2.1.10.127.1.3.3.1.3.'


def SnmpCheckUsSignal(*argv):
    '''
    argv :
        dutid,terms,labels,Panel,Log,Config,flow,[Return])
        terms : ccu , cb , sw , vm ,dut 
    ''' 
    mac = argv[2][0]
    term = argv[1][-1]   
    log = argv[-4]
    port =argv[0]
    usChannel = int(argv[-3](argv[-2],'usChannel'))
    ofdmaChannel = int(argv[-3](argv[-2],'ofdmaChannel'))
    cmts = argv[-3]('Base','CMTSIP')
    ipaddr = SnmpGetWanIp(cmts,mac)
    us_pwr_oid = '1.3.6.1.4.1.4491.2.1.20.1.2.1.1'
    us_freq_oid = '1.3.6.1.2.1.10.127.1.1.2.1.2'
    ofdma_freq_oid = '1.3.6.1.4.1.4491.2.1.28.1.13.1.2'
    ofdma_pwr_oid = '1.3.6.1.4.1.4491.2.1.28.1.13.1.10'
    # lWaitCmdTerm(term,'shell','#',3,3)
    # ipaddr = GetWanIP(term)
    system_uspower = eval(argv[-3]('Base','system_uspower'))
    uspower_offset = eval(argv[-3]('Base','uspower_offset'))
    #us_ofdm_offset = eval(argv[-3]('Base','us_ofdm_offset'))
    #ofdm_uspower = int(argv[-3]('Base','ofdm_uspower'))    
    freq_step = argv[-3]('Base','freq_step')
    freq_uspower_EU = eval('uspower_hub4_%s'%freq_step)
    #freq_uspower_EU = {16:0,55:0,42:0,23:0,29:0,48:0,10:0,36:0} #{freq:us_offset}
    idxFreqDic = {}
    for i in range(5):
        try:
            us_freq_dic = Snmp.SnmpWalk(ipaddr,us_freq_oid)
            print "22222222222222"
            print us_freq_dic
            break
        except:
            print "Retry Snmp Query US SC-QAM Frequency %d"%i
            if i == 4:raise Except('Query US SC-QAM Frequency Fail!!')
            time.sleep(2)
            continue
    for try_ in range(3):
        idxFreqDic = {}
        for freq in us_freq_dic:
            if us_freq_dic[freq] !=0:
                idxFreqDic.update({us_freq_dic[freq]: freq.split('.')[-1]})
        msg_us_lock = "US Channel Lock: %d (%d)"%(len(idxFreqDic),usChannel)
        if len(idxFreqDic) <> usChannel:
            if try_ == 2: 
                log(msg_us_lock,1)
                raise Except("ErrorCode(E00242): US Channel Lock  FAIL")
            else: continue 
        else:
            log(msg_us_lock,2)
            break
    test_fail = 0
    print "33333333333333333"
    print idxFreqDic
    for f in idxFreqDic.keys():     # US power comparison
        #print freq
        freq = int(f)
        if freq>15*1000000 and freq<40*1000000:
            pwr =  Snmp.SnmpGet(ipaddr,us_pwr_oid+'.'+idxFreqDic[freq]).values()[0]/10.0
            #print type(pwr)
            #system_uspower = cmts_uspwr[freq]
            pwr =  pwr + freq_uspower_EU[freq/1000000][port]
            msg_pwr = "US Freq = %.2f MHz, Base Power = %.2f Report = %.2f, diff = %.2f (%.2f ~ %.2f)"%(freq/1000000,system_uspower,pwr,pwr - system_uspower, uspower_offset*-1,uspower_offset)
            #print pwr
            if abs(pwr-system_uspower) > uspower_offset:
                test_fail=1
                log(msg_pwr,1)
            else:
                log(msg_pwr,2)
    if test_fail: raise Except("ErrorCode(E00242): US Power Check  FAIL")
    '''
    ############### OFDMA ###############
    idxOfdmaFreqDic = {}
    for i in range(5):
        try:
            ofdma_freq_dic = Snmp.SnmpWalk(ipaddr,ofdma_freq_oid)
            break
        except:
            print "Retry Snmp Query OFDMA Frequency %d"%i
            if i == 4:raise Except('Query OFDMA Frequency Fail!!')
            time.sleep(2)
    for try_ in range(3):
        for freq in ofdma_freq_dic:
            if ofdma_freq_dic[freq] !=0:
                idxOfdmaFreqDic.update({ofdma_freq_dic[freq]: freq.split('.')[-1]})
        msg_ofdma_lock = "OFDMA Channel Lock: %d (%d)"%(len(idxOfdmaFreqDic),ofdmaChannel)
        if len(idxOfdmaFreqDic) <> ofdmaChannel:
            if try_ == 2:
                log(msg_ofdma_lock,1)
                raise Except("ErrorCode(E00242): OFDMA Channel Lock FAIL")
            else: continue 
        else:
            log(msg_ofdma_lock,2)
            break
    log('\n')
    test_fail = 0
    for freq in idxOfdmaFreqDic:     # US power comparison
        #print freq
        pwr =  Snmp.SnmpGet(ipaddr,ofdma_pwr_oid+'.'+idxOfdmaFreqDic[freq]).values()[0]/4.0
        #print pwr
        #system_uspower = cmts_uspwr[freq]
        pwrOffset =  pwr - ofdm_uspower
        msg_pwr = "Check US OFDM repower  = %.2f, Base Power = %.2f , Offset = %.2f (%.2f ~ %.2f)"%(pwr,ofdm_uspower,pwrOffset,us_ofdm_offset*-1,us_ofdm_offset)
        #print pwr
        if abs(pwrOffset) > us_ofdm_offset:
            test_fail+=1
            log(msg_pwr,1)               
        else:
            log(msg_pwr,2)
    if test_fail: raise Except("ErrorCode(E00242): OFDMA Power Check FAIL")
    '''

def SnmpCheckDsSignal(*argv):
    '''
    argv :
        dutid,terms,labels,Panel,Log,Config,flow,[Return])
        terms : ccu , cb , sw , vm ,dut 
    ''' 
    mac = argv[2][0]
    cmts = argv[-3]('Base','CMTSIP')
    term = argv[1][-1]   
    log = argv[-4]
    pn = argv[-3]('Base','PN')
    dsChannel = int(argv[-3](argv[-2],'dsChannel'))
    ofdmChannel = int(argv[-3](argv[-2],'ofdmChannel'))
    ds_pwr_oid = '1.3.6.1.2.1.10.127.1.1.1.1.6'
    ds_freq_oid = '1.3.6.1.2.1.10.127.1.1.1.1.2'
    ds_snr_oid = '1.3.6.1.2.1.10.127.1.1.4.1.5'
    ofdm_pwr_oid = '1.3.6.1.4.1.4491.2.1.28.1.11.1.3'
    ofdm_freq_oid = '1.3.6.1.4.1.4491.2.1.28.1.9.1.3'
    ofdm_mer_oid = '1.3.6.1.4.1.4491.2.1.27.1.2.5.1.3'
    # ipaddr = GetWanIP(term)
    ipaddr = SnmpGetWanIp(cmts,mac)
    freq_step = eval(argv[-3]('Base','freq_step'))
    CMTS_freq = eval(argv[-3]('Base','CMTS_freq'))
    system_snr = eval(argv[-3]('Base','system_snr'))
    snr_offset = eval(argv[-3]('Base','snr_offset'))
    dspower_offset = eval(argv[-3]('Base','dspower_offset'))
    port =argv[0]+1
    if port > 4 : port -= 4
    for try_ in range(3): 
        sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
        if len(sn)==12:break
    dspower=eval('dspower_%s_%s_%s'%(freq_step,sn,port))
    #dspower = {639: 0, 645: 0, 615: 0, 627: 0, 609:0, 603: 0, 633: 0, 621: 0}
    #dspower = {650: 11, 658: 11, 666: 11, 674: 11, 682: 11, 690: 11, 698: 11, 706: 11}
    dsfreqlist=[]
    for i in range(4):
        dsfreqlist.append((CMTS_freq + freq_step * i)*1000000)
    idxFreqDic = {}
    for i in range(5):
        try:
            ds_freq_dic = Snmp.SnmpWalk(ipaddr,ds_freq_oid)
            print "11111111111"
            print ds_freq_dic
            break
        except:
            print "Retry Snmp Query DS Frequency %d"%i
            if i == 4:raise Except('Query DS Frequency Fail!!')
            time.sleep(2)
    for try_ in range(3):       
        for freq in ds_freq_dic:
            if ds_freq_dic[freq] !=0:
                idxFreqDic.update({ds_freq_dic[freq]: freq.split('.')[-1]})
        msg_lock = "DS Channel Lock: %d (%d)"%(len(idxFreqDic),dsChannel)
        if len(idxFreqDic) <> dsChannel:
            if try_ == 2: 
                print idxFreqDic
                log(msg_lock,1)
                raise Except("ErrorCode(E00242): %s DS Channel Lock  FAIL"%ipaddr)
            else: continue
        else:
            log(msg_lock,2)
            break
    #log('\n')
    test_fail = 0
    #for f in sorted(idxFreqDic):     # DS power comparison
    for f in sorted(dsfreqlist):
        freq = f/1000000.0
        pwr = Snmp.SnmpGet(ipaddr,ds_pwr_oid+'.'+idxFreqDic[f]).values()[0]/10.0      
        msg_pwr = "DS Freq = %.2f MHz, Base Power = %.2f Report = %.2f, diff = %.2f (%.2f ~ %.2f)"%(freq,dspower[freq],pwr,pwr - dspower[freq], dspower_offset*-1,dspower_offset)
        pwr = pwr - dspower[freq]
        if abs(pwr) > dspower_offset:
            test_fail+=1 
            log(msg_pwr,1)
        else:
            log(msg_pwr,2)
    if test_fail : raise Except("ErrorCode(E00242): %s DS Power Check  FAIL"%ipaddr)            
    #log('\n')            
    test_fail = 0
    #for f in sorted(idxFreqDic):     # US power comparison
    for f in sorted(dsfreqlist):
        freq = f/1000000.0
        snr =  Snmp.SnmpGet(ipaddr,ds_snr_oid+'.'+idxFreqDic[f]).values()[0]/10.0 
        msg_snr = "DS Freq = %.2f MHz, SNR = %.2f ( > %.2f)"%(freq, snr,system_snr)
        if snr < system_snr : 
            test_fail+=1 
            log(msg_snr,1)
        else:
            log(msg_snr,2)
    if test_fail: raise Except("ErrorCode(E00242): %s DS SNR Check  FAIL"%ipaddr)
    '''
    ############### OFDM ###################
    idxOfdmFreqDic = {}
    for i in range(5):
        try:
            ofdm_freq_dic = Snmp.SnmpWalk(ipaddr,ofdm_freq_oid)
            break
        except:
            print "Retry Snmp Query OFDM Frequency %d"%i
            if i == 4:raise Except('Query Query OFDM Frequency Fail!!')
            time.sleep(2)
    for try_ in range(3):       
        for freq in ofdm_freq_dic:
            if ofdm_freq_dic[freq] !=0:
                idxOfdmFreqDic.update({ofdm_freq_dic[freq]: freq.split('.')[-1]})
        msg_lock = "OFDM Channel Lock: %d (%d)"%(len(idxOfdmFreqDic),ofdmChannel)
        if len(idxOfdmFreqDic) <> ofdmChannel:
            if try_ == 2: 
                log(msg_lock,1)
                raise Except("ErrorCode(E00242): %s OFDM Channel Lock  FAIL"%ipaddr)
            else: continue
        else:
            log(msg_lock,2)
            break
    test_fail = 0
    # ofdm_dspower = {820:-1,801:-5,807:-1.5,813:-0.8,819:-2,825:-1.5,831:-1,837:0.66,843:-1,849:-12}
    for s in sorted(idxOfdmFreqDic):     # DS power comparison
        idxOfdmChCenFreqDic = {}
        cenFreqDic = Snmp.SnmpWalk(ipaddr,'1.3.6.1.4.1.4491.2.1.28.1.11.1.2.'+idxOfdmFreqDic[s])
        for q in cenFreqDic:
            idxOfdmChCenFreqDic.update({cenFreqDic[q]: q.split('.')[-1]})
        for f in idxOfdmChCenFreqDic:
            if idxOfdmChCenFreqDic[f] == '3' or idxOfdmChCenFreqDic[f] == '7':
                freq = f/1000000.0
                pwr = Snmp.SnmpGet(ipaddr,ofdm_pwr_oid+'.'+idxOfdmFreqDic[s]+'.'+idxOfdmChCenFreqDic[f]).values()[0]/10.0      
                msg_pwr = "DS Freq = %.2f MHz, Base Power = %.2f, Report = %.2f, diff = %.2f (%.2f ~ %.2f)"%(freq, ofdm_dspower[freq],pwr ,pwr - ofdm_dspower[freq], dspower_offset*-1,dspower_offset)
                pwr = pwr - ofdm_dspower[freq]
                if abs(pwr) > dspower_offset:
                    test_fail+=1 
                    log(msg_pwr,1)
                else:
                    log(msg_pwr,2)
            else:continue
    if test_fail: raise Except("ErrorCode(E00242): %s OFDM Power Check  FAIL"%ipaddr)
    test_fail = 0
    for f in sorted(idxOfdmFreqDic):
        freq = f/1000000.0
        snr =  Snmp.SnmpGet(ipaddr,ofdm_mer_oid+'.'+idxOfdmFreqDic[s]).values()[0]/100.0 
        msg_snr = "OFDM Freq = %.2f MHz, SNR = %.2f ( > %.2f)"%(freq, snr,system_snr)
        if snr < system_snr : 
            test_fail+=1 
            log(msg_snr,1)
        else:
            log(msg_snr,2)
    if test_fail: raise Except("ErrorCode(E00242): %s OFDM RxMER Check FAIL"%ipaddr)
    '''       

def CheckSnmpMACSN_Tune(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    #sn =  argv[2][1]
    sn = GetSN(mac)
    term = argv[1][-1]
    log = argv[-4]
    cmts = argv[-3]('Base','CMTSIP')
    #ipaddr = GetWanIP(term)
    ipaddr = SnmpGetWanIp(cmts,mac)
    timeout = int(argv[-3](argv[-2],'timeout'))
    if not WaitingSnmpReady(ipaddr,timeout):
       raise Except("ErrorCode(0007):Waiting Snmp ready Failed!!")
    for try_ in range(3):
        try:
           mac_addr = MacTrans(Snmp.SnmpGet(ipaddr,ifPhysAddress2_OID).values()[0])
           break
        except:
           mac_addr=''
    if len(mac_addr) <> 12:
       raise Except("ErrorCode(414043):Can't get mac address for snmp")
    if mac.upper() <> mac_addr:
       raise Except("ErrorCode(E00164):Snmp Get MAC address compare error %s (%s)"%(mac_addr,mac))
    for try_ in range(3):
        try:
           serialNumber = Xurl("snmp://%s/private/DOCS-CABLE-DEVICE-MIB/docsDevSerialNumber.0/s"%ipaddr).get()
        except:
           serialNumber=''
        if sn.upper() == serialNumber:break
    if sn.upper() <> serialNumber:
        raise Except("ErrorCode(214077):Snmp Get Serial Number compare error %s (%s)"%(serialNumber,sn))
    msg='Snmp get SerialNumber: %s (%s)\nSnmp get Macaddress: %s (%s)'%(serialNumber,sn,mac_addr,mac)
    log(msg,2)


def SnmpGetWanIp(cmtsip,cmMac):
    for i in range(10):
        try:
            cmtsIpDic = Snmp.SnmpWalk(cmtsip,'1.3.6.1.2.1.10.127.1.3.3.1.2')
            break
        except:
            print "Retry Snmp Query IP Index %d"%i
            if i == 9:raise Except('Query Ip Index Fail!!')
            time.sleep(2)
            continue
    ipIdx = ''
    for v in cmtsIpDic.values():
        if v.encode('hex').upper() == cmMac:
            ipIdx = cmtsIpDic.keys()[cmtsIpDic.values().index(v)].split('.')[-1]
    if not ipIdx: raise Except('Invalid Mac Address!!')
    return Snmp.SnmpGet(cmtsip,'1.3.6.1.2.1.10.127.1.3.3.1.3.'+ipIdx).values()[0]

def getWlanip(mac,cmtsip):
    try:
      #values=Snmp.SnmpWalk(cmtsip,transmissionatMAC)
      values=Snmp.SnmpWalk(cmtsip,'1.3.6.1.2.1.10.127.1.3.3.1.2')
      value='0.0.0.0'
      mac_id=''
      dut_status=int(-1)
      for oid in values:
          if mactrans(values[oid])==mac:
             mac_id=oid.split('.')[-1].strip()
             break
      time.sleep(1)
      if mac_id:
         # value=Snmp.SnmpGet(cmtsip,transmissionatIPAddress+mac_id).values()[0]
         value=Snmp.SnmpGet(cmtsip,'1.3.6.1.2.1.10.127.1.3.3.1.3.'+mac_id).values()[0]
         print value
         time.sleep(1) 
         
         if htx_local.IsConnect(value,6):
            for retry in range(15):
               dut_status = Snmp.SnmpGet(value,docsIfCmStatusValue_OID).values()[0]
               if 9 <= dut_status <= 12:
                  return (True,dut_status,value)
               time.sleep(0.5)
    except:
      pass
    return (False,dut_status,value)

def WaitCMregistor(mac,cmtsip,timeout):
    s_time=timeout+time.time()+0.1
    while time.time() < s_time:
          value=getWlanip(mac,cmtsip)
          print value
          #print 'registor :',
          #print value
          if value[0]:
             break 
    return value

def SnmpWaitCMRegistration(*argv):
    '''-1: noWanIp(-1)
       0: queryNone(0)
       1: other(1)
       2: notReady(2)
       3: notSynchronized(3)
       4: phySynchronized(4)
       5: usParametersAcquired(5)
       6: rangingComplete(6)
       7: ipComplete(7)
       8: todEstablished(8)
       9: securityEstablished(9)
       10: paramTransferComplete(10)
       11: registrationComplete(11)
       12: operational(12)
       13: accessDenied(13)
    '''
    online_status={'-1':'noWanIp','0':'queryNone','1':'other','2':'notReady','3':'notSynchronized',\
                   '4':'phySynchronized','5':'usParametersAcquired','6':'rangingComplete','7':'ipComplete',\
                   '8':'todEstablished','9':'securityEstablished','10':'paramTransferComplete',\
                   '11':'registrationComplete','12':'operational','13':'accessDenied'}
    mac = argv[2][0]
    timeout = int(argv[-3](argv[-2],'timeout'))
    cmts = argv[-3]('Base','CMTSIP')
    CMTS_freq = argv[-3]('Base','CMTS_freq')
    Telnet = eval(argv[-3]('Base','TELNET'))
    username = argv[-3]('Base','username')
    password_ = argv[-3]('Base','password_')
    log = argv[-4]
    ETH0IP = argv[-3]('AFI','ETH0IP').split('|')
    ETH0IP_ = ETH0IP[0].strip()
    c_port = argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4
       ETH0IP_ = ETH0IP[1].strip()
    port = c_port + 1
    pid = '30%s1'%(port+1)

    for i in range(2):
      if i==0:timeout=20
      else:timeout=200
      value=WaitCMregistor(mac,cmts,timeout)
      if value[0]: 
      	log('\nCM Operational OK\n',2)
      	break
      else: 
      	if i==1:raise Except("ErrorCode(E00125):Registration Timeout | dud_status:%s | wan_ip:%s"%(online_status[str(value[1])] , value[2]))
      	log('tune freq 527',2)
        argv[1][-1]=lLogin_AFI1(ETH0IP_,pid,username,password_)
        if argv[1][-1]:
          argv[-4]('ARM Telnet login')      
        else:raise Except('Telnet login Failure')
        lWaitCmdTerm_(argv[1][-1],"cli",">",8,3)
        lWaitCmdTerm_(argv[1][-1],"doc","docsis>",5,5)
        TuneDsFreq(argv[1][-1],CMTS_freq,60)

def TuneDsFreq(term,CMTS_freq,timeout):
    stime=time.time()
    etime=time.time()+timeout
    while time.time()<= etime:
         data = lWaitCmdTerm_(term,"cmstatus","docsis>",5,5)
         print data
         if "NOT_SYNCHRONIZED" not in data:
            term<<"quit"
            print '\nTune Ds freq OK\n'
            return 
         else:
            lWaitCmdTerm_(term,"tune %s"%CMTS_freq,"docsis>",8,2)
            time.sleep(20)     
    raise Except("ErrorCode(E00125):Tune Ds freq fail")  


def MacTrans(mac):
    return "%02X%02X%02X%02X%02X%02X"%(ord(mac[0]),ord(mac[1]),ord(mac[2]),ord(mac[3]),ord(mac[4]),ord(mac[5]))

def lPrintSysDescr_Tune(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    #sn =  argv[2][1]
    sn = GetSN(mac)
    term = argv[1][-1]
    log = argv[-4]
    cmts = argv[-3]('Base','CMTSIP')
    ipaddr = GetWanIP(term)
    #ipaddr = SnmpGetWanIp(cmts,mac)
    sysdesc = argv[-3]('Base','sysdesc')
    value = result = ''
    
    for try_ in range(20):
        try:
            value = result = Snmp.SnmpGet(ipaddr,sysDescr_OID).values()[0]
            break
        except:
            if try_ == 19:raise Except('ErrorCode(214036):Snmp get failed : No response')
            time.sleep(2)
            continue 
            
    if value:
       msg=      "DOCSIS Version:      "
       msg=msg + result[:result.find("<<")].strip() + '\n'
       result =  result[result.find("<<")+2:result.find(">>")].split(";")
       msg=msg + "Hardware Version:    "
       msg=msg + result[0].split(":")[1].strip() + '\n'
       msg=msg + "Vendor:              "
       msg=msg + result[1].split(":")[1].strip() + '\n'
       msg=msg + "BootLoader Version:  "
       msg=msg + result[2].split(":")[1].strip() + '\n'
       msg=msg + "Software Version:    "
       msg=msg + result[3].split(":")[1].strip() + '\n'
       msg=msg + "Model Name:          "
       msg=msg + result[4].split(":")[1].strip() 
       log(msg)
    if value <> sysdesc:
    #if value in sysdesc:
       print value
       print sysdesc
       raise Except('ErrorCode(214036):SNMP sysDescr.0 incorrect!')
    log('SNMP sysDescr check pass',2)


def WaitingSnmpReady(ipaddr,timeout): 
    os.system('arp -d')
    i = 0
    print 'Waiting Snmp ready...' 
    while i < timeout: 
          try: 
              #print ipaddr,ifPhysAddress2_OID
             Snmp.SnmpGet(ipaddr,ifPhysAddress2_OID).values()
             flag = 1 
          except Exception,e:
             print e.message
             flag =0 
          if flag: 
             return 1  
          i += 1 
          time.sleep(1) 
    return 0  
   
   

def Correction_Telnet_Shell_Password(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    telnet_PWD='admin'
    shell_PWD='AccessDeny'
        
    ipaddr = GetWanIP(term)

    timeout = int(argv[-3](argv[-2],'timeout'))
    if not WaitingSnmpReady(ipaddr,timeout):
       raise Except("ErrorCode(0007):Waiting Snmp ready Failed!!")

    for try_ in range(10):
        try:
            Snmp.SnmpSet(ipaddr,'1.3.6.1.4.1.8595.20.16.1.1.1.1.4.1',"s","%s"%shell_PWD,community="private")
            Snmp.SnmpSet(ipaddr,'1.3.6.1.4.1.8595.20.16.1.1.1.1.4.2',"s","%s"%telnet_PWD,community="private")
            time.sleep(1)
            Snmp.SnmpSet(ipaddr,'1.3.6.1.4.1.8595.20.16.2.1',"i",1,community="private")            
            break
        except:
            time.sleep(1)
            if try_ == 9:
                raise Except("Snmp Set Telnet_Shell_Password FAIL") 
            continue
           
    msg = 'Snmp Set Telnet_Shell_Password PASS'
    log(msg,2)

def GetSN(mac):
    sn = ""
    #ServerIP,ServerPort,timeout = map(strip,argv[-3]('Base','MESServer').split('|'))
    ServerIP='127.0.0.1'
    ServerPort=1800
    timeout=30
    MesSocket=htx.UDPService(ServerIP,int(ServerPort),int(timeout))
    MesSocket.set('3,' + mac)  
    Result=MesSocket.get()
    print Result
    Result=Result.strip()
    if Result:
       if len(Result)<>12 or (Result[:2] != '25' and Result[:2] != 'V5'and Result[:2] != 'B5'): # Check SN length and header
          raise Except("ErrorCode(0005):Get SN Failed:%s"%Result)
       else:
          sn = Result
          return sn
    raise Except("ErrorCode(0005):Connection MES Server Fail ")

   
def CheckSnmpMACSN(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    #sn =  argv[2][1]
    sn = GetSN(mac)
    term = argv[1][-1]
    log = argv[-4]
    password_ = argv[-3]('Base','shell_password').strip()
    lWaitCmdTerm(term,"shell","Password:",5,3)
    lWaitCmdTerm(term,"%s"%password_,"#",5,3)
    
    ipaddr = GetWanIP(term)
    timeout = int(argv[-3](argv[-2],'timeout'))
    if not WaitingSnmpReady(ipaddr,timeout):
       raise Except("ErrorCode(0007):Waiting Snmp ready Failed!!")
       
    for try_ in range(20):
        try:
           mac_addr = MacTrans(Snmp.SnmpGet(ipaddr,ifPhysAddress2_OID).values()[0])
           break
        except:
           mac_addr=''
           time.sleep(2)
           continue
           
    if len(mac_addr) <> 12:
       raise Except("ErrorCode(414043):Can't get mac address for snmp")
    if mac.upper() <> mac_addr:
       raise Except("ErrorCode(E00164):Snmp Get MAC address compare error %s (%s)"%(mac_addr,mac))
    for try_ in range(3):
        try:
           # serialNumber = Xurl("snmp://%s/private/DOCS-CABLE-DEVICE-MIB/docsDevSerialNumber.0/s"%ipaddr).get()
           serialNumber = Snmp.SnmpGet(ipaddr,".1.3.6.1.2.1.69.1.1.4.0").values()[0]
        except:
           serialNumber=''
        if sn.upper() == serialNumber:break
    if sn.upper() <> serialNumber:
        raise Except("ErrorCode(214077):Snmp Get Serial Number compare error %s (%s)"%(serialNumber,sn))
    msg='Snmp get SerialNumber: %s (%s)\nSnmp get Macaddress: %s (%s)'%(serialNumber,sn,mac_addr,mac)
    log(msg,2)



def CheckSnmpMACSNTelnet_CCR(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    shellpassword = argv[-3]('Base','shellpassword')
    ipaddr = GetWanIPTelnet_CCR(term,shellpassword)
    timeout = int(argv[-3](argv[-2],'timeout'))
    if not WaitingSnmpReady(ipaddr,timeout):
       raise Except("ErrorCode(0007):Waiting Snmp ready Failed!!")
    for try_ in range(3):
        try:
           mac_addr = MacTrans(Snmp.SnmpGet(ipaddr,ifPhysAddress2_OID).values()[0])
           break
        except:
           mac_addr=''
    if len(mac_addr) <> 12:
       raise Except("ErrorCode(414043):Can't get mac address for snmp")
    if mac.upper() <> mac_addr:
       raise Except("ErrorCode(E00164):Snmp Get MAC address compare error %s (%s)"%(mac_addr,mac))
    for try_ in range(3):
        try:
           serialNumber = Xurl("snmp://%s/private/DOCS-CABLE-DEVICE-MIB/docsDevSerialNumber.0/s"%ipaddr).get()
        except:
           serialNumber=''
        if sn.upper() == serialNumber:break
    if sn.upper() <> serialNumber:
        raise Except("ErrorCode(214077):Snmp Get Serial Number compare error %s (%s)"%(serialNumber,sn))
    msg='Snmp get SerialNumber: %s (%s)\nSnmp get Macaddress: %s (%s)'%(serialNumber,sn,mac_addr,mac)
    log(msg,2)


def lPrintSysDescr(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    #sn =  argv[2][1]
    sn = GetSN(mac)
    term = argv[1][-1]
    log = argv[-4]
    #password_ = argv[-3]('Base','shell_password').strip()
    #lWaitCmdTerm(term,"shell","Password:",5,3)
    #lWaitCmdTerm(term,"%s"%password_,"#",5,3)
    ipaddr = GetWanIP(term)
    sysdesc = argv[-3]('Base','sysdesc')
    value = result = ''
    
    for try_ in range(20):
        try:
            value = result = Snmp.SnmpGet(ipaddr,sysDescr_OID).values()[0]
            break
        except:
            if try_ == 19:raise Except('ErrorCode(214036):Snmp get failed : No response')
            time.sleep(2)
            continue 
            
    if value:
       msg=      "DOCSIS Version:      "
       msg=msg + result[:result.find("<<")].strip() + '\n'
       result =  result[result.find("<<")+2:result.find(">>")].split(";")
       msg=msg + "Hardware Version:    "
       msg=msg + result[0].split(":")[1].strip() + '\n'
       msg=msg + "Vendor:              "
       msg=msg + result[1].split(":")[1].strip() + '\n'
       msg=msg + "BootLoader Version:  "
       msg=msg + result[2].split(":")[1].strip() + '\n'
       msg=msg + "Software Version:    "
       msg=msg + result[3].split(":")[1].strip() + '\n'
       msg=msg + "Model Name:          "
       msg=msg + result[4].split(":")[1].strip() 
       log(msg)
    if value <> sysdesc:
    #if value in sysdesc:
       print value
       print sysdesc
       raise Except('ErrorCode(214036):SNMP sysDescr.0 incorrect!')
    log('SNMP sysDescr check pass',2)

    
def SnmpGetDUTipOpenTelnet(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut
    '''
    mac = argv[2][0]
    log = argv[-4]
    c_port = argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4
    cmtsip = argv[-3]('Base','cmtsip')
    timeout = int(argv[-3](argv[-2],'timeout'))
    username = argv[-3]('Base','username').strip()
    password_ = argv[-3]('Base','password_').strip()
    
    lWaitCmdTerm(argv[1][1],'rf %s c'%(c_port+1),'OK',5)
    dutiplist = WaitCMregistor(mac,cmtsip,timeout)
    dutip = dutiplist[-1]
    argv[1][-1] = lLogin_CMTS(dutip,username,password_)
          
def mactrans(mac):
    b=''
    for j in map(ord,mac):
        b=b+'%02X'%j
    return b    
           
def lLogin_CMTS(dstip,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    print 'Telnet login Start'
    for i in range(5):
        term = htx.Telnet(dstip)
        data = term.wait("login:",5)[-1]
        print '[%s]%s'%(time.ctime(),data)
        print username
        print password
        term << username
        time.sleep(2)
        term << password
        data=term.wait('>',5)[-1]
        print '[%s]%s'%(time.ctime(),data)
        if '>' in data  or '#' in data:
            time.sleep(1)
            return term 
            break
        if i == 4:raise Except('Telnet login Failure')           
           
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
            
                         
