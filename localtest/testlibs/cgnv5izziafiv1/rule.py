import os,sys,time,random,odbc,glob,pyodbc
import buildkey,thread  
import struct
build_lock=thread.allocate_lock() 
from toolslib_local import *


#config set
TestProgIP = os.popen('ipconfig').read()
if '172.28.221' in TestProgIP:
    TestProgIP = '172.28.221.253'
    CAshareIP = '172.28.221.250'

elif '172.28.227' in TestProgIP:
    TestProgIP = '172.28.227.253'
    CAshareIP = '172.28.227.250'
    
elif '172.28.224' in TestProgIP:
    TestProgIP = '172.28.224.253'
    CAshareIP = '172.28.224.250'

else:
    TestProgIP = '172.28.122.23'
    CAshareIP = '172.28.122.23'


def GetCaKey(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    path = "C:/HtSignTools/CA/DualHitron.CA/out"    
    #mac = '84948C4BA1F0'   
    ca_type = ['cer','prv','pvt']
    dsn ="host='%s' dbname='test' user='test' password='test'"%CAshareIP
    mac = argv[2][0]

    path = argv[-3]('TFTPSERVER','tftprootfolder')
    for i in range(len(ca_type)):
        data = os.popen("GetCaKey \"%s\" \"%s\" %s %s"%(dsn,path,mac,ca_type[i])).read() 
        print data
        if "PASS" in data:
            msg="Get CA Key Success %s"%mac

        else: 
            raise Except ("ErrorCode(0002):Get CA key error %s %s"%(mac,ca_type))
            
    argv[-4](msg,2)


def GenerateLGIWIFIKey_back():
    key_str = ['ABCDEFGHJKLMNPQRSTUVWXYZ','23456789','abcdefghijkmnpqrstuvwxyz']# skip 'o','0','1','l','I' 
    while 1:            
        capital_num = int(random.choice('12')) 
        int_num = int(random.choice('12'))
        lower_num = 12 - (capital_num + int_num)
        count = [0,0,0] # [capital,int,lower]    
        wifikey = ""
        for i in range(12):
            key = random.choice(key_str[int(random.choice('012'))])
            #print key
            if 65 <= ord(key) <= 90: # Check capital string 
                count[0]+=1
                if count[0] > capital_num: key = random.choice(key_str[int(random.choice('12'))])               
            if 48 <= ord(key) <= 57: # Check Integer string
                count[1]+=1
                if count[1] > int_num: key = random.choice(key_str[int(random.choice('2'))])            
            wifikey = wifikey + key 
        if not 1 <= count[0] <= 2: continue
        if not 1 <= count[1] <= 2: continue        
        if capital_num + int_num == 2:
            if (48 <= ord(wifikey[0]) <=57 or 65 <= ord(wifikey[0]) <=90) and (48 <= ord(wifikey[1]) <=57 or 65 <= ord(wifikey[1]) <=90):continue              
            if (48 <= ord(wifikey[10]) <=57 or 65 <= ord(wifikey[10]) <=90) and (48 <= ord(wifikey[11]) <=57 or 65 <= ord(wifikey[11]) <=90):continue
        return wifikey

def ChkWpaKeyRule(wifikey):
    key = [None]*20
    W_flag = 0
    for i in range(len(wifikey)):
        key[i] = wifikey[i]
        if key[i] == 'W': W_flag+=1
        if W_flag > 1: return 0
        if i >0:
            if key[i] == 'W':
                if key[i-1]=='W' or key[i-1]=='V': return 0
            elif key[i] == 'V':
                if key[i-1]=='W' or key[i-1]=='V': return 0 
            elif key[i] == 'w':
                if key[i-1]=='w' or key[i-1]=='v': return 0
            elif key[i] == 'v':
                if key[i-1]=='w' or key[i-1]=='v': return 0
    return 1  


def GenerateGeneralWIFIKey():
    keystr = 'ACEFGHJKLMNPQRSTUXYZ2345679abcdefghjkmnpqrstuxyz'
    a =  random.SystemRandom(keystr)
    while 1: 
        wifikey = ""
        for i in range(12):
            wifikey = wifikey + a.choice(keystr)
            #print wifikey
        if not ChkWpaKeyRule(wifikey):
            continue 
        return wifikey 

def GenerateHUB4WIFIKey():
    keystr = 'ACEFGHJKLMNPQRSTUVWXYZ'
    keyint = '2345679'
    keystr_list = list(keystr)
    keyint_list = list(keyint)
    random.shuffle(keystr_list)
    random.shuffle(keyint_list)
    wifikey=keystr_list[:18]+keyint_list
    while True:
        random.shuffle(wifikey)
        if ChkHUB4WpaKeyRule(wifikey[:8],keyint_list):
           continue
        wifikey = ''.join(wifikey[:8])
        break
    return wifikey 

def ChkHUB4WpaKeyRule(*args):
    intflag=0
    excludes_str=('0','O','D','8','B','I','1')
    for key in args[0]:
        for _str in excludes_str:
            if key == _str: return 1
        if key in args[1]: intflag+=1
    if intflag: return 0
    else: return 1

def GenerateLGIWIFIKey():
    key_str = ['ABCDEFGHJKLMNPQRSTUVWXYZ','23456789','abcdefghjkmnpqrstuvwxyz']
    a =  random.SystemRandom()
    while 1:            
        capital_num = int(a.choice('12')) 
        int_num = int(a.choice('12'))
        lower_num = 12 - (capital_num + int_num)
        count = [0,0,0] # [capital,int,lower]    
        wifikey = ""
        
        for i in range(12):
            key = a.choice(key_str[int(a.choice('012'))])
            #print key
            if 65 <= ord(key) <= 90: # Check capital string 
                count[0]+=1
                if count[0] > capital_num: key = a.choice(key_str[int(a.choice('12'))])               
            if 48 <= ord(key) <= 57: # Check Integer string
                count[1]+=1
                if count[1] > int_num: key = a.choice(key_str[int(a.choice('2'))])            
            wifikey = wifikey + key 
        if not 1 <= count[0] <= 2: continue
        if not 1 <= count[1] <= 2: continue 
        if not ChkWpaKeyRule(wifikey): continue      
        if capital_num + int_num == 2:
            if (48 <= ord(wifikey[0]) <=57 or 65 <= ord(wifikey[0]) <=90) and (48 <= ord(wifikey[1]) <=57 or 65 <= ord(wifikey[1]) <=90):continue              
            if (48 <= ord(wifikey[10]) <=57 or 65 <= ord(wifikey[10]) <=90) and (48 <= ord(wifikey[11]) <=57 or 65 <= ord(wifikey[11]) <=90):continue
        return wifikey

def GenerateWebKey():
    #keystr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'   
    keystr = '0123456789'
    wifikey = ""
    a =  random.SystemRandom(keystr)
    if len(keystr)<>10: raise Except("keystr error")
    for i in range(7):
        wifikey = wifikey + a.choice(keystr)
    b = ComputeChecksum(wifikey)
    key = '%s%d'%(wifikey,b)    
    c = ValidateChecksum(key) 
    if c: return key
    else: raise Except("FAIL WEB KEY: %s "%key)

def ValidateChecksum(PIN):
    PIN = int(PIN)   
    accum = 0 
    accum += 3 * ((PIN / 10000000) % 10)  
    accum += 1 * ((PIN / 1000000) % 10)  
    accum += 3 * ((PIN / 100000) % 10)  
    accum += 1 * ((PIN / 10000) % 10)  
    accum += 3 * ((PIN / 1000) % 10)  
    accum += 1 * ((PIN / 100) % 10)  
    accum += 3 * ((PIN / 10) % 10)  
    accum += 1 * ((PIN / 1) % 10)  
    return (0 == (accum % 10)) 

def ComputeChecksum(PIN):
    accum = 0
    PIN = int(PIN)     
    PIN *= 10; 
    accum += 3 * ((PIN / 10000000) % 10)  
    accum += 1 * ((PIN / 1000000) % 10)  
    accum += 3 * ((PIN / 100000) % 10)  
    accum += 1 * ((PIN / 10000) % 10)  
    accum += 3 * ((PIN / 1000) % 10)  
    accum += 1 * ((PIN / 100) % 10)  
    accum += 3 * ((PIN / 10) % 10)     
    digit = int((accum % 10))
    return (10 - digit) % 10 



def CheckCertificate(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    a = ""
    for i in range(0,len(mac),2):
        if i < 10: 
            a = a + mac[i:i+2] + ":"
        elif i == 10: a = a + mac[i:i+2]
        else: break
    print a
    for i in range(3):
        data = lWaitCmdTerm(argv[1][-1],"cmcert","on>",8,3)
        print data
        argv[-4](data,2)
        if a in data and mac in data:
            msg="Check Certificate %s: PASS (PASS)"%mac
            break
        else: 
            if i==2:raise Except ("ErrorCode(414051):Check Certificate %s ,%s"%(mac,data))
    argv[-4](msg,2)

def CheckCertificate_RES(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    a = ""
    for i in range(0,len(mac),2):
        if i < 10: 
            a = a + mac[i:i+2] + ":"
        elif i == 10: a = a + mac[i:i+2]
        else: break
    for i in range(3):
        data = lWaitCmdTerm(argv[1][-1],"cmcert","on>",5,3)
        argv[-4](data,2)
        if a in data and "[%s]"%mac in data: 
            msg="Check Certificate %s: PASS (PASS)"%mac
            break
        else: 
            if i==2:raise Except ("ErrorCode(414051):Check Certificate %s ,%s"%(mac,data))
            
    argv[-4](msg,2)
    
    t = time.gmtime()
    current_year = '%s'%str(t[0])
    year_diff=20
    if int(t[1])==1:year_diff=19
    for i in range(3):
        data = lWaitCmdTerm(argv[1][-1],"cmcert","on>",5,3)
        start_year = data.split("Validity Start")[1].split("Validity End")[0].split()[-2]
        ending_year = data.split("Validity End")[1].split("Subject Name")[0].split()[-2]        
        if current_year==start_year and int(ending_year)-int(start_year)==year_diff:
            msg="Check CA start date and have expired date of 20 year PASS (PASS)"
            break
        else:
            if i==2:raise Except("Check CA start date and have expired date of 20 year Fail!")   
  
    argv[-4](msg,2)
                
def CheckProdction(term,sy,sp,log):
    for try_ in range(4):
        data = lWaitCmdTerm(term,"prodshow","ion>",8,2)
        if sy in data:
          gsp = data.split(sy)[-1].split(">")[0].split("<")[-1]
          msg= "%s: %s (%s)"%(sy,gsp,sp)
          if sp == gsp:
             log(msg,2)
             break
          else:
            if try_==3:
               raise Except ("ErrorCode(E00147):%s"%msg) 
        else:
          if try_== 3:
             raise Except (sy+": get error") 

def CheckMacSN(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    usbdevice = eval(argv[-3]("Base","USB_Device"))
    mac = argv[2][0]
    #sn =  argv[2][1]
    sn = GetSN(mac)
    term = argv[1][-1]
    log = argv[-4]
    rf_mac = "%012X"%(int(mac,16))
    lan_mac = "%012X"%(int(mac,16)+2)
    usb_host_mac = "%012X"%(int(mac,16)+1)
    rf_mac = rf_mac[0:2]+"-"+rf_mac[2:4]+"-"+rf_mac[4:6]+"-"+rf_mac[6:8]+"-"+rf_mac[8:10]+"-"+rf_mac[10:12]
    lan_mac = lan_mac[0:2]+"-"+lan_mac[2:4]+"-"+lan_mac[4:6]+"-"+lan_mac[6:8]+"-"+lan_mac[8:10]+"-"+lan_mac[10:12]
    usb_host_mac = usb_host_mac[0:2]+"-"+usb_host_mac[2:4]+"-"+usb_host_mac[4:6]+"-"+usb_host_mac[6:8]+"-"+usb_host_mac[8:10]+"-"+usb_host_mac[10:12]

    CheckProdction(term, "Cable Modem Serial Number",sn,log)
    CheckProdction(term, "Cable Modem MAC",rf_mac,log)   
    CheckProdction(term, "Lan MAC",lan_mac,log) 
    if usbdevice :
       CheckProdction(term, "USB Host MAC",usb_host_mac,log)  
    
def GetWpaKeyandInsert(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    log = argv[-4]
    
    #lWaitCmdTerm(argv[1][-1],"quit","#",5)
    #lWaitCmdTerm(argv[1][-1],"cli","mainMenu>",5,5)
    data=lWaitCmdTerm(argv[1][-1],"Manu","Manufacture>",8,3)
    if "Command not found" in data:
          lWaitCmdTerm(argv[1][-1],"quit","#",5)
          lWaitCmdTerm(argv[1][-1],"cli","mainMenu>",5,5)
          lWaitCmdTerm(argv[1][-1],"Manu","Manufacture>",5,3)
    else :
         lWaitCmdTerm(argv[1][-1],"Manu","Manufacture>",5,3)
          #break
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","Manufacture>",5,2)
        wifi_key_back = data.split("now")[-1].split("Manufacture")[0].strip()
        #wifi_key_back = data.split("wpa key is:")[-1].split("MAIN")[0].strip()
        if len(wifi_key_back)==12:break 
        if try_==2:raise Except("wpakey %s digit fail"%wifi_key_back)
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","Manufacture>",5,2)
        wifi_key = data.split("now")[-1].split("Manufacture")[0].strip()
        #wifi_key = data.split("wpa key is:")[-1].split("MAIN")[0].strip()
        if wifi_key==wifi_key_back:break 
        if try_==2:raise Except("wpakey %s digit fail"%wifi_key)
    argv[-4]('WPAKEY : %s '%wifi_key,2)
    ### Set Web Kay ###
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"userPasswordGet","Manufacture>",5,2)
        web_key_back = data.split("Get")[-1].split("Manufacture")[0].strip()
        #wifi_key_back = data.split("wpa key is:")[-1].split("MAIN")[0].strip()
        if len(web_key_back)==8:break 
        if try_==2:raise Except("webkey %s digit fail"%web_key_back)
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"userPasswordGet","Manufacture>",5,2)
        web_key = data.split("Get")[-1].split("Manufacture")[0].strip()
        #wifi_key = data.split("wpa key is:")[-1].split("MAIN")[0].strip()
        if web_key==web_key_back:break 
        if try_==2:raise Except("wpakey %s digit fail"%web_key)
    argv[-4]('WebKEY : %s '%web_key,2)
    
    ''' 
    if insert :
       key_dic = {'SSID_PASSWORD':'','NETWORK_KEY':'','WPS_PIN':'','FON_KEY':''}
       key_dic['NETWORK_KEY'] = wifi_key
       key_dic['WPS_PIN'] = wifi_key
       key_dic['SSID_PASSWORD'] = web_key 
       Insert_WiFiKEY(mac,key_dic,log)
    '''
    if insert :
       key_dict = {'password':'','wps_pin':'','network_key':''}
       key_dict['password'] = web_key         
       key_dict['wps_pin'] = wifi_key          ## 2.4G password
       key_dict['network_key'] = wifi_key      ## 5G password
       insert_ssid_mes(mac,key_dict) 
       argv[-4]('Insert WIFI 2G/5G Key AND WEB KEY PASS',2)   
    

def GetWiFiKEY_CGN3(sn):
    db = odbc.odbc("TESTlog/TEST/test")
    SQL = db.cursor()
    SQL.execute("SELECT NetworkKey FROM SSIDkey WHERE SN = '%s' ORDER BY [Time] DESC"%sn)  #wifiKey path is different
    data = SQL.fetchone()[0]
    return data 

def GetWebKEY_CGN3(sn):
    db = odbc.odbc("TESTlog/TEST/test")
    SQL = db.cursor()
    SQL.execute("SELECT SSIDKey FROM SSIDkey WHERE SN = '%s' ORDER BY [Time] DESC"%sn)  #webKey path is different
    data = SQL.fetchone()[0]
    return data 



def CheckGetWpaKeyandInsert(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    sn =  argv[2][1]
    log = argv[-4]

    for i in range(40):
       lWaitCmdTerm(argv[1][-1],"quit","#",5,2)
       lWaitCmdTerm(argv[1][-1],"cli","mainMenu>",8,3)
       data = lWaitCmdTerm(argv[1][-1],"Manu",">",5,3)
       if "Command not found" in data:
           lWaitCmdTerm(argv[1][-1],"quit","#",5,2)
           lWaitCmdTerm(argv[1][-1],"cli","Menu>",8,3)
           lWaitCmdTerm(argv[1][-1],"Manu",">",5,3)
       if i ==39:raise Except("Go to Manufacture path fail")
       if "Manufacture" in data:
          lWaitCmdTerm(argv[1][-1],"Manu","ture>",5,3)
          break
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","Manufacture>",5,2)
        wifi_key = data.split("now")[-1].split("Manufacture")[0].strip()
        #wifi_key_back = data.split("wpa key is:")[-1].split("MAIN")[0].strip()
        if wifi_key == GetWiFiKEY_CGN3(sn):break 
        if try_==2:raise Except("check wpakey %s digit fail"%wifi_key)
    log('Check wpakey %s digit OK!'%wifi_key)  
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"userPasswordGet","Manufacture>",5,2)
        web_key = data.split("Get")[-1].split("Manufacture")[0].strip()
        #print web_key
        if web_key == GetWebKEY_CGN3(sn):break 
        if try_==2:raise Except("check webkey %s digit fail"%web_key)
    log('Check webkey %s digit OK!'%web_key)   


def GetWpaKeyandInsert_CWV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    log = argv[-4]
   
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","Manufacture>",5)
        wifikey_ = data.split("wpaKeygetnow")[-1].split("Manufacture")[0].strip()
        if len(wifikey_)==8:break 
        if try_==2:raise Except("wpakey %s digit fail"%wifikey_)
        
    argv[-4]('WPAKEY : %s '%wifikey_,2)
  
    #wifi_key = sn +'2G0000'
    if insert :
       key_dict = {'password':'','wps_pin':'','network_key':''}     
       #key_dict['password'] = wifi_key        ##ONLY 2.4G password 
       key_dict['wps_pin'] = wifikey_          ## 2.4G password
       key_dict['network_key'] = wifikey_      ## 5G password        
       insert_ssid_mes(mac,key_dict) 
       argv[-4]('insert password PASS',2)

def CheckGetWpaKeyandInsert_CWV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    #sn =  argv[2][1]
    sn = GetSN(mac)
    log = argv[-4]
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","Manufacture>",5)
        wifi_key_back = data.split("wpaKeygetnow")[-1].split("Manufacture")[0].strip()
        key_d=GetWiFiKEY(sn)
        if wifi_key_back==key_d[0] and wifi_key_back==key_d[1]:break 
        if try_==2:raise Except("check wpakey %s digit fail"%wifi_key_back)
    log('Check wpakey %s digit OK!'%wifi_key_back) 

def GetWiFiKEY(sn):
    key_list=['',''] #0:2.4G,1:5G
    key_table=["NetworkKey","WPSPinKey"]
    for i in range(len(key_table)):
        db = odbc.odbc("TESTlog/TEST/test")
        SQL = db.cursor()
        SQL.execute("SELECT %s FROM SSIDkey WHERE SN = '%s' ORDER BY [Time] DESC"%(key_table[i],sn))
        data = SQL.fetchone()[0]
        if data:
            key_list[i]=data    
        else:
            raise Except("get wpakey from DB fail")           
    return key_list 


#############20121129 add function#############
def InstallKey_CCR(*argv):
    '''
    argv :
        dutid,terms,labels,Panel,Log,Config,flow,[Return])
        terms : ccu , cb , sw , vm ,dut 
    Model:SMCD3G-CCR
    '''
    mac = argv[2][0]
    mac_ = "%s:%s:%s:%s:%s:%s"%(mac[:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:])
    log = argv[-4]
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    term = argv[1][-1]
    '''   
    build_lock.acquire()
    data = os.popen("C:\\HtSignTools\\HtCmKey.exe DualHitron %s"%mac).read()
    build_lock.release()
    if not os.path.isfile("%s/%s.DualHitron"%(openssl_path,mac)):
        raise Except ("failed:Build BPI key error")
    '''
    build_lock.acquire()
    for i in range(3):
        data = os.popen("C:\\HtSignTools\\HtCmKey.exe DualHitron %s"%mac).read()
        if not os.path.isfile("%s/%s.DualHitron"%(openssl_path,mac)):
           if i==2:raise Except ("ErrorCode(0002):Build BPI key error")
        else:
           f = open("%s/%s.DualHitron"%(openssl_path,mac),'rb')
           data = f.read()
           f.close()
           if data.count(mac)<> 2 or data.count(mac_) <> 2:
              os.popen("del %s/%s.DualHitron"%(openssl_path,mac))
              if i==2:raise Except ("ErrorCode(0002):Build BPI key error")
           else:break      
    build_lock.release()   

    #ca_file = open("%s/%s.DualHitron"%(openssl_path,mac),"rb").read()
    print ('Install %s.DualHitron'%(mac))
    for i in range(4):
        data = lWaitCmdTerm(term,"bpiset %s %s.DualHitron"%(tftp_ip,mac),"keys saved",10)
        if 'Tftp exited OK' in data:
            log('Install %s.DualHitron OK!'%(mac),2)
            break
        else:
           if i==3: raise Except ("ErrorCode(E00167):Install BPI key failed")    
    
    
#############20121130 cve30360 mx###########
def InstallKey_CVE30360MX(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    
    #install cmcert key
    a = "%012X"%(int(mac,16))
    doc_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]
    for i in ["cer","prv"]:
        if not os.path.isfile("%s/%s.%s"%(openssl_path,doc_ca,i)):
            raise Except ("ErrorCode(0002):No such file %s.%s"%(doc_ca,i)) 
    lWaitCmdTerm(term,"cmcert %s %s.cer %s.prv eth0.1"%(tftp_ip,doc_ca,doc_ca),"keys saved",10)
    argv[4]('Install %s.cer %s.prv OK'%(doc_ca,doc_ca),2)

    #Install Pakcet Cable Certificate
    a = "%012X"%(int(mac,16)+1)
    pkt_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]  
    for i in ["cer","prv"]:
        if not os.path.isfile("%s/%s.%s"%(openssl_path,pkt_ca,i)):
            raise Except ("ErrorCode(0002):No such file %s.%s"%(pkt_ca,i))   
    data=lWaitCmdTerm(term,"mtaCert 0 %s.cer %s.prv %s eth0.1"%(pkt_ca,pkt_ca,tftp_ip),"ture>",5)
    if data.count('Tftp exited OK')<>2:
       raise Except ("ErrorCode(E00167):mtaCert 0 %s.cer %s.prv failed"%(pkt_ca,pkt_ca)) 
    argv[4]('Install %s.cer %s.prv OK'%(pkt_ca,pkt_ca),2)
   
    for i in ('PacketCable_Centralized_CA.509.cer','CableLabs_Service_Provider_Root_CA.cer'):
        if not os.path.isfile("%s/%s"%(openssl_path,i)):
                raise Except ("ErrorCode(0002):No such file %s"%i) 
    lWaitCmdTerm(term,"mtaMfgCert 0 PacketCable_Centralized_CA.509.cer %s eth0.1"%tftp_ip,"Succeeded setting",5)
    #lWaitCmdTerm(term,"mtaMfgCert 0 PacketCable_Centralized_MTA_CA.der %s"%tftp_ip,"Succeeded setting",5)
    lWaitCmdTerm(term,"mtaSpRootCert 0 CableLabs_Service_Provider_Root_CA.cer %s eth0.1"%tftp_ip,"Succeeded setting",5)
    lWaitCmdTerm(term,"exit","docsis>",5) 
    lWaitCmdTerm(term,"exit",">",5)
    lWaitCmdTerm(term,"pacm","pacm>",5)
    lWaitCmdTerm(term,"security","security>",5)
    lWaitCmdTerm(term,"certificates","certificates>",5)
    mac1=":".join(pkt_ca.split("-"))
    dst=[mac1, "O=CableLabs, Inc., OU=PacketCable, OU=PC CA00001, CN=CableLabs, Inc. PacketCable CA",
         "CN=CableLabs Service Provider Root CA" ]
    flag=0    
    for i in range(1,4):
        data=lWaitCmdTerm(argv[1][-1],"displayCertContent 0 %s"%i,"tes>",5,3)
        print data
        if not dst[i-1] in data:
           argv[4]('%s'%data)
           raise Except ("%s displayCertContent 0 %s check fail"%(mac,i))
        else:
           argv[4]("displayCertContent 0 %s pass"%i,2)   
    
#############add CGN_RES by TDL 20121201#############    
def CheckWpaKeyandInsert_RES(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    sn =  argv[2][1]    
    log = argv[-4]
    """
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","MAIN>",5)
        wifi_key = data.split("wpa key is:")[-1].split("MAIN")[0].strip()
        if len(wifi_key)==12:break 
        if try_==2:raise Except("wpakey %s digit fail"%wifi_key)
    """
    for try_ in range(3):    
        data = sn[4:]
        wifikey = hex(int(data,16)^int('DEADFDAE',16))
        wifikey = wifikey[2:-1].upper()
        print 'count wifikey: %s'%wifikey
        if len(wifikey) == 8:break 
        if try_==2:raise Except("ErrorCode(E00248):wpakey %s count fail"%wifi_key)
           
    lWaitCmdTerm(argv[1][-1],"top",">",3)
    data = lWaitCmdTerm(argv[1][-1],"script show",">",3)
    wifi_key = data.split("wireless_wpa_preshare_key 1 ")[-1].split("wireless_pre_authentication 1 false")[0].strip()
    print 'wifi_key: %s'%wifi_key
    print len(wifi_key)
    if len(wifi_key)<>8 or wifi_key <> wifikey: raise Except("ErrorCode(E00248):wpakey %s fail(%s)"%(wifi_key,wifikey))

    argv[-4]('WPAKEY : %s '%wifi_key,2)
    if insert :
       key_dic = {'SSID_PASSWORD':'','NETWORK_KEY':'','WPS_PIN':'','FON_KEY':''}
       key_dic['SSID_PASSWORD'] = wifi_key
       Insert_WiFiKEY(mac,key_dic,log) 
    
def InstallCustomerKey_RES(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    
    mac = "%012X"%(int(mac,16))
    doc_ca = mac[0:2]+"-"+mac[2:4]+"-"+mac[4:6]+"-"+mac[6:8]+"-"+mac[8:10]+"-"+mac[10:12]
    for i in ["cer","prv"]:
        if not os.path.isfile("%s/%s.%s"%(openssl_path,doc_ca,i)):
            raise Except ("ErrorCode(E00170):No such file %s.%s"%(doc_ca,i)) 
    print lWaitCmdTerm(argv[1][-1],"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved",10)
    argv[4]('Install %s.cer %s.prv OK'%(doc_ca,doc_ca),2)
        
#############add CDE30364 by TDL 20130108#############  
def GetWpaKeyandInsert_R2(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    log = argv[-4]
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","ure>",5)
        wifi_key_back = data.split("wpa key is:")[-1].split("Manufacture")[0].strip()
        if len(wifi_key_back)==12:break 
        if try_==2:raise Except("wpakey %s digit fail"%wifi_key_back)
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","ure>",5)
        wifi_key = data.split("wpa key is:")[-1].split("Manufacture")[0].strip()
        if wifi_key==wifi_key_back:break 
        if try_==2:raise Except("wpakey %s digit fail"%wifi_key)
    argv[-4]('WPAKEY : %s '%wifi_key,2)
    if insert :
       key_dic = {'SSID_PASSWORD':'','NETWORK_KEY':'','WPS_PIN':'','FON_KEY':''}
       key_dic['SSID_PASSWORD'] = wifi_key
       Insert_WiFiKEY(mac,key_dic,log)
      
#######################SMCD3GNV_13_04_17################################
def _installkey(term,cmd,waitstr):
    for try_ in range(3):
        term << cmd
        data=term.wait(waitstr,5)[-1]
        if waitstr in data:return data
        if 'tftp: rcvmsgopt: Resource temporarily unavailable' in data:
           term << chr(0x03)
           lWaitCmdTerm(term,"cli",">",5) 
           lWaitCmdTerm(term,"cable","cable>",5)
           lWaitCmdTerm(term,"doc","docsis>",5)
           lWaitCmdTerm(term,"Manu","Manufacture>",5)
    return ''
    
def InstallKey_SMCD3GNV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    log = argv[-4]
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    #Install CM certificate   
    # Private Key
    term.get()
    #lWaitCmdTerm(term,dut_card,"cable","cable>",3,3) 
    #lWaitCmdTerm(term,dut_card,"doc","docsis>",3,3)
    lWaitCmdTerm(term,"Manu","Manufacture>",5)
    a = "%012X"%(int(mac,16))
    doc_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]
    for i in ["cer","prv"]:
        if not os.path.isfile("%s\%s.%s"%(openssl_path,doc_ca,i)):
            raise Except ("No such file %s.%s"%(doc_ca,i)) 
    
    #lWaitCmdTerm(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved",5)
    if not _installkey(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved"): 
       raise Except('Install %s.cer %s.prv NG'%(doc_ca,doc_ca))
    log('Install %s.cer %s.prv OK'%(doc_ca,doc_ca))
    a = "%012X"%(int(mac,16)+1)
    pkt_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]
    
    for i in ["cer","prv"]:
        if not os.path.isfile("%s\%s.%s"%(openssl_path,pkt_ca,i)):
            raise Except ("No such file %s.%s"%(pkt_ca,i))   
      
    for j in range(3):
        data = _installkey(term,"mtaCert 0 %s.cer %s.prv %s"%(pkt_ca,pkt_ca,tftp_ip),"mtakey.bin")
        print data
        if data.count('Tftp exited OK')<>2: 
           if j==2:
              raise Except ("mtaCert 0 %s.cer %s.prv %s"%(pkt_ca,pkt_ca,tftp_ip)) 
        else:break  
            
    if not _installkey(term,"mtamfgCert 0 PacketCable_Centralized_CA.509.cer %s"%tftp_ip,"Succeeded setting"):
       raise Except('install PacketCable_Centralized_CA.509.cer NG')
    if not _installkey(term,"mtaspRootCert 0 CableLabs_Service_Provider_Root_CA.cer %s"%tftp_ip,"Succeeded setting"):
       raise Except('install CableLabs_Service_Provider_Root_CA.cer NG')
    log('Install %s.cer %s.prv OK'%(pkt_ca,pkt_ca))

    lWaitCmdTerm(term,"exit","docsis>",5) 
    lWaitCmdTerm(term,"exit","cable>",5)
    lWaitCmdTerm(term,"pacm","pacm>",3)
    lWaitCmdTerm(term,"security","security>",5)
    lWaitCmdTerm(term,"certificates","certificates>",5)
    for i in range(3):
        data = lWaitCmdTerm(term,"displayCertContent 0 1","rsaEncryption",10)
        log(data)
        mac1=":".join(pkt_ca.split("-"))
        if not mac1 in data:
            if i==2:
               raise Except ("%s displayCertContent 0 1 check fail"%mac)
        else:
            log('displayCertContent 0 1 pass')
            break
    for i in range(3):
        data = lWaitCmdTerm(term,"displayCertContent 0 2","rsaEncryption",10)
        log(data)
        if not "O=CableLabs, Inc., OU=PacketCable, OU=PC CA00001, CN=CableLabs, Inc. PacketCable CA" in data:
            if i==2:raise Except ("%s displayCertContent 0 2 check fail"%mac)
        else:
            log('displayCertContent 0 2 pass')
            break 
    for i in range(3):
        data = lWaitCmdTerm(term,"displayCertContent 0 3","rsaEncryption",10)
        log(data)
        if not "CN=CableLabs Service Provider Root CA" in data:
          if i ==2:raise Except ("%s displayCertContent 0 3 check fail"%mac)   
        else:
            log('displayCertContent 0 3 pass')
            break
def GetSN(mac):
    sn = ""
    #ServerIP,ServerPort,timeout = map(strip,argv[-3]('Base','MESServer').split('|'))
    ServerIP='127.0.0.1'
    ServerPort=1800
    timeout=30
    MesSocket=htx_local.UDPService(ServerIP,int(ServerPort),int(timeout))
    MesSocket.set('3,' + mac)  
    Result=MesSocket.get()
    print Result
    Result=Result.strip()
    if Result:
       if len(Result)<>12 or (Result[:2] != '25' and Result[:2] != 'V5'and Result[:2] != 'B5'):
          raise Except("ErrorCode(0005):Get SN Failed:%s"%Result)
       else:
          sn = Result
          return sn
    raise Except("ErrorCode(0005):Connection MES Server Fail ")
      
def InstallParameter(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    #mac,sn = argv[2][:2]
    mac = argv[2][0]
    sn = GetSN(mac)
    hw = argv[-3]('Base','HSW').split('|')[0].strip()
    hw_major = hw[0]
    hw_minor = hw[-1]
    wifi_key_install = eval(argv[-3]('Base','WIFI_Device'))
    prodset = eval(argv[-3]('Base','prodset'))
    boardConfig = 1
    labellisit = argv[2]
    term = argv[1][-1]
    #lWaitCmdTerm(argv[1][-1],"macAddr %s"%mac,"ure>",5,2)
    data=lWaitCmdTerm(argv[1][-1],"macAddr %s"%mac,"ure>",5,2)
    print data
    if 'Error format!' in data:
       raise Except('ErrorCode(0000):Install MAC Adress NG,%s'%data)
    argv[4]('Install MAC Adress OK')
    
    for i in range(3):
        data=lWaitCmdTerm(argv[1][-1],"setSN %s"%sn,"ure>",5,2)
        print data
        if 'have been saved' in data:break
        else:
            if i==2:raise Except('ErrorCode(0000):Install Serial Number NG,%s'%data)
    argv[4]('Install Serial Number OK')
    
    lWaitCmdTerm(argv[1][-1],"sethwver %s %s"%(hw_major,hw_minor),"saved",8,3)
    data = lWaitCmdTerm(argv[1][-1],"show","Cable",8,3)
    argv[4](data)
    if "%s.%s"%(hw_major,ord(hw_minor)) in data  or  "%s.%s"%(hw_major,hw_minor) in data: 
       argv[4]('Install HW Version %s OK'%hw)
    else:
       raise Except ("ErrorCode(0000):HW ver %s,%s"%(hw,data))

    #if wifi_key_install:
    if 1:
       for i in range(30):
          lWaitCmdTerm(argv[1][-1],"top","Menu>",10,3)
          data = lWaitCmdTerm(argv[1][-1],"Manu",">",5,2)
          if 'Manufacture>' in data:
              break
       wifi_key = GenerateHUB4WIFIKey()
       data=lWaitCmdTerm(argv[1][-1],"wpaKeyset %s"%wifi_key,"ure>",5)
       #argv[4]('%s'%data)
       argv[4]('Install Wpakey %s OK'%wifi_key)
       
    '''  
    lWaitCmdTerm(argv[1][-1],"top","Menu>",10,3)   
    lWaitCmdTerm(argv[1][-1],"doc","docsis>",8)
    lWaitCmdTerm(argv[1][-1],"Prod","tion>",8,2)
    data=lWaitCmdTerm(argv[1][-1],"prodsh","Production>",5)
    if '<216> [in quarter DB]' not in data:
       argv[1][-1] << "prodset"
       while 1:
           argv[1][-1].get()
           time.sleep(0.1)
           data = lWaitCmdTerm(argv[1][-1],"",">",5,2)
           if "[q]-Quit" in data:
              lWaitCmdTerm(argv[1][-1],"w","been saved",5,2)
              argv[4]("Prodset Extended Upstream Power=216")
              break
           if "Extended US Power : Currently set to" in data:
              print "Extended Upstream Power: MAX3518"
              lWaitCmdTerm(argv[1][-1],"216",">",5)
    data=lWaitCmdTerm(argv[1][-1],"prodsh","Production>",5)          
    if '<216> [in quarter DB]' not in data:raise Except ("Set Extended Upstream Power=216 fail")
    '''

def InstallKey(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    mac_ = "%s:%s:%s:%s:%s:%s"%(mac[:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:])
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    build_lock.acquire()
    for i in range(3):
        data = os.popen("C:\\HtSignTools\\HtCmKey.exe DualHitron %s"%mac).read()
        if not os.path.isfile("%s/%s.DualHitron"%(openssl_path,mac)):
           if i==2:raise Except ("ErrorCode(0002):Build BPI key error")
        else:
           f = open("%s/%s.DualHitron"%(openssl_path,mac),'rb')
           data = f.read()
           f.close()
           if data.count(mac)<> 2 or data.count(mac_) <> 2:
              os.popen("del %s/%s.DualHitron"%(openssl_path,mac))
              if i==2:raise Except ("ErrorCode(0002):Build BPI key error")
           else:break      
    build_lock.release()
    #ca_file = open("%s/%s.DualHitron"%(openssl_path,mac),"rb").read()  
    #install BPI key  
    lWaitCmdTerm(argv[1][-1],"bpiset %s %s.DualHitron"%(tftp_ip,mac),"keys saved",8,3)
    argv[4]('Install BPI Key Success',2)


def InstallKey_CGN3(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    log = argv[-4]
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    #Install CM certificate   
    #Private Key
    term.get()
    #lWaitCmdTerm(term,"Manu","Manufacture>",5)
    a = "%012X"%(int(mac,16))
    doc_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]
    for i in ["cer","prv"]:
        if not os.path.isfile("%s\%s.%s"%(openssl_path,doc_ca,i)):
            raise Except ("No such file %s.%s"%(doc_ca,i))     
    lWaitCmdTerm(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved",15)
    #if not _installkey(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved"): 
     #  raise Except('Install %s.cer %s.prv NG'%(doc_ca,doc_ca))
    log('Install %s.cer %s.prv OK'%(doc_ca,doc_ca))

def InsertPublicKey(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    log = argv[-4]
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    mta_cer_path_loacl = argv[-3]('TFTPSERVER','mta_cer_path_loacl')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    
    mac="%012X"%(int(mac,16)+1)
    log_name = '%s\\%s.der'%(openssl_path,mac)
    if not os.path.isfile(log_name):
        raise Except ("failed:No such file %s.der"%mac)     
    file = glob.glob('%s\\%s*.der'%(openssl_path,mac)) 
    count = 0 
    if file:
       for i in file:
          a= i.split("\\")[-1].strip()
          if a==mac+'.der':
             break
          count+=1
          if count ==2:raise Except('Not match publickey!')
    print i    
    argv[4]('%s'%i,2) 
    file_ = open(i,'rb').read()  
    #print file_
    #ODBCinsert(mac,file_)  
    key = ODBCinsert(mac,file_)
    if file_<>key:
       raise Except("Check Local Pulickey and DB Fail")
    argv[4]('Check Local Public Key and DB pass')
    src = []
    for c in key:
        d = struct.unpack("c",c)[0]
        if "\\x" in d:
          src.append(d.split[-1:-3])
        else:
          src.append("%02x"%ord(d))
    for try_ in range(6):
        data=lWaitCmdTerm(term,"displayCertContent 1 1","tes>",5,3)
        #data = data.split("sha1WithRSAEncryption")[1].split("certific")[0].split()
        data = data.split("sha1WithRSAEncryption")[-1].split("certificates>")[0].split()
        #print data
        dst = []
        for d in data:
            for d in d.split(":"):
                if d :dst.append(d)
        if dst<>src[0x213:]:
           if try_==5:
              argv[4]('DB PublicKey :%s'%src[0x213:])
              argv[4]('DUT PublicKey :%s'%data)
              raise Except("Check DUT Pulickey and DB Fail")
        else:
            argv[4]('DB PublicKey :%s'%src[0x213:])
            argv[4]('DUT PublicKey :%s'%data)
            argv[4]('Check DUT Pulickey and DB Pass',2)
            break

def ODBCinsert(mac,logfile):
    mac="%012X"%(int(mac,16)-1)
    logfile = bz2.compress(logfile)
    
    #logserver='172.28.206.253'
    #if '172.28.206' not in os.popen('ipconfig').read():logserver='172.28.209.253' 
     
    logserver='172.28.221.250'
    if '172.28.224' in os.popen('ipconfig').read():logserver='172.28.224.250'
    if '172.28.227' in os.popen('ipconfig').read():logserver='172.28.227.250'      
             
    db = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(logserver,'TEST','TEST','test')) 
    db.autocommit=True
    cursor = db.cursor()
    sql = "insert into PublicKey (MAC,testtime,publickey) values('%s',getdate(),?)"%mac 
    cursor.execute(sql,(buffer(logfile),))
    time.sleep(1)
    cursor.execute("select publickey from PublicKey where MAC = '%s' order by testtime DESC"%mac)
    data = cursor.fetchone()
    if data:
       print 'Publickey insert to DB success'
       return bz2.decompress(data[0])
    else:
       return 0
      

def InstallKey_CGNV4EU(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
         #CA / EMTA Key in local
    '''
    mac = argv[2][0]
    mac_ = "%s:%s:%s:%s:%s:%s"%(mac[:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:])
    term = argv[1][-1]
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    mta_cer_path = argv[-3]('TFTPSERVER','mta_cer_path')
    mta_cer_path_loacl = argv[-3]('TFTPSERVER','mta_cer_path_loacl')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    
    #install cmcert key
    build_lock.acquire()
    for i in range(3):
        data = os.popen("C:\\HtSignTools\\HtCmKey.exe DualHitron %s"%mac).read()
        if not os.path.isfile("%s/%s.DualHitron"%(openssl_path,mac)):
           if i==2:raise Except ("ErrorCode(0002):Build BPI key error")
        else:
           f = open("%s/%s.DualHitron"%(openssl_path,mac),'rb')
           data = f.read()
           f.close()
           if data.count(mac)<> 2 or data.count(mac_) <> 2:
              os.popen("del %s/%s.DualHitron"%(openssl_path,mac))
              if i==2:raise Except ("ErrorCode(0002):Build BPI key error")
           else:break      
    build_lock.release()
    #ca_file = open("%s/%s.DualHitron"%(openssl_path,mac),"rb").read()  
    #install BPI key  
    data=lWaitCmdTerm(term,"bpiset %s %s.DualHitron"%(tftp_ip,mac),"keys saved",8,3)
    argv[4]('%s'%data)
    argv[4]('Install BPI Key Success',2)
    
    ##install SSL certification 
    data=lWaitCmdTerm(term,"sslDload %s 0005CA-1520520001N0-%s.pfx key.txt"%(tftp_ip,mac),"MAC verified OK",8,2)
    argv[4]('%s'%data)
    time.sleep(0.3)
    lWaitCmdTerm(term,"sslCheck %s"%(mac),"MAC verified OK",8,2)
    argv[4]('Install NOS-SSL Success',2)

    #print "Install Pakcet Cable Certificate"
    mac = "%012X"%(int(mac,16)+1)
    build_lock.acquire()
    #msg1 = buildkey.Create(mta_cer_path_loacl,mac)
    msg = buildkey.Create(openssl_path,mac)
    build_lock.release()
    if msg:raise Except('ErrorCode(0001):%s'%msg)

    os.popen("%s\\cleanall.bat"%mta_cer_path).read() 
    
    #data = os.popen("%s\\buildkey\\b %s"%(mta_cer_path,mac)).read()
    if not os.path.isfile("%s/Euro-PacketCable_Service_Provider_Root_CA.509.cer"%openssl_path):
        raise Except ("failed:No such file Euro-PacketCable_Service_Provider_Root_CA.509.cer") 
    if not os.path.isfile("%s/Hitron_EuroPacketCable_CA.509.cer"%openssl_path):
        raise Except ("failed:No such file Hitron_EuroPacketCable_CA.509.cer")
    if not os.path.isfile("%s/%s.der"%(openssl_path,mac)):
        data = os.popen("copy %s\\%s.der C:\\HtSignTools\\CA\\DualHitron.CA\\out"%(mta_cer_path_loacl,mac)).read()
    if not os.path.isfile("%s/%s_private.der"%(openssl_path,mac)):
        data = os.popen("copy %s\\%s_private.der C:\\HtSignTools\\CA\\DualHitron.CA\\out"%(mta_cer_path_loacl,mac)).read()
    if not os.path.isfile("%s/%s_public.der"%(openssl_path,mac)):
        data = os.popen("copy %s\\%s_public.der C:\\HtSignTools\\CA\\DualHitron.CA\\out"%(mta_cer_path_loacl,mac)).read()


    argv[4]("Install %s.der"%mac,2)
    argv[4]("Install %s_private.der"%mac,2)

    lWaitCmdTerm(argv[1][-1],"exit","is>",5)  
    lWaitCmdTerm(argv[1][-1],"exit","Menu>",5)
    lWaitCmdTerm(argv[1][-1],"pacm","cm>",5,2)
    lWaitCmdTerm(argv[1][-1],"sec","ty>",5,2)
    lWaitCmdTerm(argv[1][-1],"certificates","es>",5,2)

    data=lWaitCmdTerm(argv[1][-1],"getAllCerts 1 %s.der %s_private.der Hitron_EuroPacketCable_CA.509.cer  Euro-PacketCable_Service_Provider_Root_CA.509.cer %s l2sd0.2"%(mac,mac,tftp_ip),"certificates>",10,2)     
    argv[4]('%s'%data)
    
    mac1 = mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
    dst=[mac1, "OU=Euro-PacketCable, CN=Euro-PacketCable Root Device Certificate Authority","CN=tComLabs Service Provider Root CA" ]

    flag=0    
    for i in range(1,4):
        data=lWaitCmdTerm(argv[1][-1],"displayCertContent 1 %s"%i,"tes>",5,3)
        argv[4]('%s'%data,2)
        if not dst[i-1] in data:
           #argv[4]('%s'%data)
           raise Except ("%s displayCertContent 1 %s check fail"%(mac,i))
        else:
           argv[4]("displayCertContent 1 %s pass"%i,2)   

def InstallKey_CGNV4EU_DB(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    mac_ = "%s:%s:%s:%s:%s:%s"%(mac[:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:])    
    menu = argv[-3]('Base','Menu').strip()
    model = argv[-3]('Base','ModelName')
    ca_type = ['DualHitron']
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    
    #build_lock.acquire()
    for i in range(3): 
        data = os.popen("GetCaKey.exe \"%s\" %s"%(openssl_path,mac)).read() 
        print data
        if "Success" in data:
            msg="Get CA Key Success %s"%mac
            argv[4](msg,2)
            break
        if i==2: 
            raise Except ("ErrorCode(0002):Get CA key error %s %s"%(mac,ca_type))

    #build_lock.release()
    
    #ca_file = open("%s/%s.DualHitron"%(openssl_path,mac),"rb").read()  
    #install BPI key  
    print lWaitCmdTerm(argv[1][-1],"bpiset %s %s.DualHitron"%(tftp_ip,mac),"keys saved",30,2)
    argv[4]('Install BPI Key Success',2)

    #print "Install Pakcet Cable Certificate"
    mac = "%012X"%(int(mac,16)+1)
    mta_ca_type = ['der']
    
    #build_lock.acquire()
    #msg = buildkey.Create(openssl_path,mac)
    for i in range(3): 
        data = os.popen("GetCaKey.exe \"%s\" %s"%(openssl_path,mac)).read() 
        print data
        if "Success" in data:
            msg="Get MTA CA Key Success %s"%mac
            argv[4](msg,2)
            break
        if i==2: 
            raise Except ("ErrorCode(0002):Get MTA CA key error %s %s"%(mac,mta_ca_type))
    #build_lock.release()
    #if msg:raise Except('ErrorCode(0001):%s'%msg)

    lWaitCmdTerm(argv[1][-1],"top","nu>",10,2)
    lWaitCmdTerm(argv[1][-1],"pacm","cm>",10)
    lWaitCmdTerm(argv[1][-1],"sec","ty>",10)
    lWaitCmdTerm(argv[1][-1],"certificates","es>",10)
    lWaitCmdTerm(argv[1][-1],"getAllCerts 1 %s.der %s_private.der Hitron_EuroPacketCable_CA.509.cer Euro-PacketCable_Service_Provider_Root_CA.509.cer %s l2sd0.2"%(mac,mac,tftp_ip),"certificates>",30,2)     
    argv[4]("Install %s.der"%mac,2)
    argv[4]("Install %s_private.der"%mac,2)
     
    mac1 = mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
    dst=[mac1, "OU=Euro-PacketCable, CN=Euro-PacketCable Root Device Certificate Authority","CN=tComLabs Service Provider Root CA" ]
    flag=0    
    for i in range(1,4):
        data=lWaitCmdTerm(argv[1][-1],"displayCertContent 1 %s"%i,"tes>",15,3)
        print data    
        if not dst[i-1] in data:
           raise Except ("%s displayCertContent 1 %s check fail"%(mac,i))
        else:
           if i == 1: argv[4](data,2) 
           argv[4]("displayCertContent 1 %s pass"%i,2)      


def InstallKey_CGN3(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    log = argv[-4]
    #path = "C:/HtSignTools/CA/DualHitron.CA/out"    
    #mac = '84948C4BA1F0'   
    ca_type = ['cer','prv','pvt']
    dsn ="host='%s' dbname='test' user='test' password='test'"%CAshareIP
    path = argv[-3]('TFTPSERVER','tftprootfolder')
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    #Install CM certificate   
    # Private Key
    term.get()
    #lWaitCmdTerm(term,"Manu","Manufacture>",5)
    a = "%012X"%(int(mac,16))
    doc_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]
    for i in ["cer","prv"]:
        if not os.path.isfile("%s\%s.%s"%(openssl_path,doc_ca,i)):
            #raise Except ("No such file %s.%s"%(doc_ca,i)) 
            for i in range(len(ca_type)):
                data = os.popen("GetCaKey \"%s\" \"%s\" %s %s"%(dsn,path,mac,ca_type[i])).read() 
                print data
                if "PASS" in data:
                    msg="Get CA Key Success %s"%mac
                else: 
                    raise Except ("ErrorCode(0002):Get CA key error %s %s"%(mac,ca_type))
          
    
    #lWaitCmdTerm(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved",5)
    lWaitCmdTerm(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved",15)
    #if not _installkey(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved"): 
     #  raise Except('Install %s.cer %s.prv NG'%(doc_ca,doc_ca))
    log('Install %s.cer %s.prv OK'%(doc_ca,doc_ca))

    
