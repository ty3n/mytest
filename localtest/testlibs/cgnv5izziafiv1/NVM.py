import os,sys,time,random,odbc,glob,pyodbc,htx
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

elif '172.28.225' in TestProgIP:
    TestProgIP = '172.28.225.253'
    CAshareIP = '172.28.225.250'

    
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
        if not ChkWpaKeyRule(wifikey[:8]):
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

def GenerateLGIWIFIKey_20190525():
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


def GenerateLGIWIFIKey():
    keystr = 'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789'
    #keystr = '0123456789'
    a =  random.SystemRandom(keystr)
    while 1: 
        wifikey = ""
        for i in range(12):
            wifikey = wifikey + a.choice(keystr)
            #print wifikey
        if not ChkWpaKeyRule(wifikey):
            continue 
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

    #print a
    for i in range(3):
        data = lWaitCmdTerm(argv[1][-1],"cmcert","on>",8,3)
        print data
        #if 'Public Key Length = 1024 bits' in data and a in data: 
        if a in data:
            msg="Check CA_3.0 Certificate %s: PASS (PASS)"%mac
            argv[-4](data,2)
            break
        else: 
            if i==2:raise Except ("ErrorCode(414051):Check Certificate %s ,%s"%(mac,data))
    argv[-4](msg,2)

    for i in range(3):
        data = lWaitCmdTerm(argv[1][-1],"cmcert","on>",8,3)
        if "ORG Name : CableLabs, Inc." or "ORG Name : CableLabs" in data:
            msg="Check CableLabs CA Key PASS"
            break
        else: 
            if i==2:raise Except ("ErrorCode(414051):Check CableLabs CA Key PASS")
    argv[-4](msg,2)

    for i in range(3):
        data = lWaitCmdTerm(argv[1][-1],"cmcert","on>",8,3)
        if "CableLabs, Inc. Cable Modem Root Certificate Authority" or "CableLabs Cable Modem Certificate Authority" in data:
            msg="Check COMMON NAME PASS"
            break
        else: 
            if i==2:raise Except ("ErrorCode(414051):Check COMMON NAME Failed")
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
        data = lWaitCmdTerm(argv[1][-1],"cmcert","Certification>",5,3)
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
        data = lWaitCmdTerm(argv[1][-1],"cmcert","Certification>",5,3)
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
        data = lWaitCmdTerm(term,"prodshow","Production>",8,2)
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
    #sn =  argv[2][1]
    mac = mac.upper()
    sn = GetSN(mac)              
    log = argv[-4]
    '''
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
    '''
    for try_ in range(3):
        #wifi_key="Cl4r0@%s"%mac[-6:]
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","Manufacture>",5,2)
        wifi_key = data.split("now")[-1].split("Manufacture")[0].strip()        
        if wifi_key == GetWiFiKEY_CGN3(sn):break 
        if try_==2:raise Except("check wpakey %s digit fail"%wifi_key)
    log('Check wpakey %s digit OK!'%wifi_key)  


def insert_ssid_mes(mac,key_dict):
    """
       key_dict={'ssid':'' , 
                 'password':'' , 
                 'ssid2':'' ,
                 'wps_pin':'' , 
                 'network_key':'' ,
                 'pin_24g':'' , 
                 'pin_5g':'' ,
                 'fonkey':'' ,
                }
    """
    key_dict = ";".join(str(key_dict).split(","))
    MesSocket=htx.UDPService("127.0.0.1",1800,30)
    #MesSocket=htx_local.UDPService("127.0.0.1",1800,30)
    MesSocket.set('9,%s,%s'%(mac,key_dict))  
    Result=MesSocket.get()
    if Result <> '':
       if 'OK' in Result:
          return 1
       else:
          raise Except("ErrorCode(0006):upload ssid and wpakey to mes Failed")    
    raise Except("ErrorCode(0005):Connection MES Server Fail ") 

def GetWpaKeyandInsert_CWV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    log = argv[-4]
   
    mac=mac.upper()
    #wifikey_= "Cl4r0@%s"%mac[-6:]   
    #argv[-4]('WPAKEY : %s '%wifikey_,2)
    #wifi_key = sn +'2G0000'
    for try_ in range(3):
        data = lWaitCmdTerm(argv[1][-1],"wpaKeygetnow","Manufacture>",5)
        get_wifikey = data.split("wpaKeygetnow")[-1].split("Manufacture")[0].strip()
        #if wifikey_==get_wifikey:break 
        if len(get_wifikey)==12:break 
        if try_==2:raise Except("wpakey %s digit fail"%wifikey_)
    if insert :
       key_dict = {'password':'','wps_pin':'','network_key':''}     
       #key_dict['password'] = get_wifikey        ##ONLY 2.4G password 
       key_dict['wps_pin'] = get_wifikey          ## 2.4G password
       key_dict['network_key'] = get_wifikey      ## 5G password        
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
    lWaitCmdTerm(argv[1][-1],"top","nu>",5,2)
    lWaitCmdTerm(argv[1][-1],"shell","Password:",5,3)
    lWaitCmdTerm(argv[1][-1],"password","#",5,3)
    lWaitCmdTerm(argv[1][-1],"cd /var/tmp/","#",5,3)
    lWaitCmdTerm(argv[1][-1],"rm /var/tmp/in.txt","#",5,3)
    lWaitCmdTerm(argv[1][-1],"rm /var/tmp/out.txt","#",5,3)
    for i in range(3):
        lWaitCmdTerm(argv[1][-1],"rm /var/tmp/in.txt","#",5,3)
        lWaitCmdTerm(argv[1][-1],"echo %s>/var/tmp/in.txt"%wifi_key_back,"#",5,3)
        data=lWaitCmdTerm(argv[1][-1],"ls /var/tmp/","#",5,3)
        if "in.txt" in data:break
        else:
            if i==2:Except("ErrorCode:Build in.txt fail")
            time.sleep(1)
    
    for i in range(3):
        lWaitCmdTerm(argv[1][-1],"rm /var/tmp/out.txt","#",5,3)
        lWaitCmdTerm(argv[1][-1],"openssl enc -e -AES-256-ECB -K EBEBD739001462C01C8BD4A76F1B7028 -in /var/tmp/in.txt -out /var/tmp/out.txt -p","#",10,2)
        data=lWaitCmdTerm(argv[1][-1],"ls /var/tmp/","#",5,3)
        if "out.txt" in data:break
        else:
            if i==2:Except("ErrorCode:Build out.txt fail")
            time.sleep(1)
    
    for i in range(3):
        data=""
        data=lWaitCmdTerm(argv[1][-1],"hexdump /var/tmp/out.txt","#",5,3)
        try:
            hex_key=''.join(data.split('0000000')[-1].split("0000010")[0].strip().split())
            if len(hex_key)==32:break
            else:
                if i==2:Except("ErrorCode:get encrypted password fail")
                time.sleep(1)
        except:
            if i==2:Except("ErrorCode:get out.txt data fail") 
            time.sleep(1)
    argv[-4]('Encryption Password:%s'%hex_key,2)        
    if 1 :
       #key_dict = {'password':'','wps_pin':'','network_key':''}  
       key_dict = {'wps_pin':'','network_key':'','pin_24g':'','pin_5g':''}   
       key_dict['pin_24g'] = hex_key        ##hex key
       key_dict['pin_5g'] = hex_key
       key_dict['wps_pin'] = wifi_key_back          ## 2.4G password
       key_dict['network_key'] = wifi_key_back      ## 5G password        
       insert_ssid_mes(mac,key_dict) 
       argv[-4]('insert encrypted password PASS',2)
       
    lWaitCmdTerm(argv[1][-1],"cd /","#",5,3)
    lWaitCmdTerm(argv[1][-1],"exit",">",10,1)
    
            
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
    if os.path.exists("%s/%s.DualHitron"%(openssl_path,mac)):
         os.remove("%s/%s.DualHitron"%(openssl_path,mac))
         
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
            log('%s'%data,2)
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
    
    ca_type = ['cer','prv']
    d30_size=[];d31_size=[]
    dsn ="host='%s' dbname='TMSDB' user='test' password='test'"%CAshareIP
    path = argv[-3]('TFTPSERVER','tftprootfolder')
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    term = argv[1][-1]
    mac = "%012X"%(int(mac,16))
    doc_ca = mac[0:2]+"-"+mac[2:4]+"-"+mac[4:6]+"-"+mac[6:8]+"-"+mac[8:10]+"-"+mac[10:12]

    #Install CM D3.0 CA Key certificate   
    term.get()
    argv[4]("Cable lab. Certificate 3.0 loading Start...")
    a = "%012X"%(int(mac,16))
    doc_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]
    #Del default CA
    if os.path.exists("%s/%s.cer"%(path,doc_ca)):
         os.remove("%s/%s.cer"%(path,doc_ca))
    else:print "The CA Key is Delete"
    if os.path.exists("%s/%s.prv"%(path,doc_ca)):
         os.remove("%s/%s.prv"%(path,doc_ca))
    else:print "The CA Key is Delete"
    if os.path.exists("%s/%s.pvt"%(path,doc_ca)):
         os.remove("%s/%s.pvt"%(path,doc_ca))
    else:print "The CA Key is Delete"
    
    for i in range(len(ca_type)):
        data = os.popen("GetCaKey \"%s\" \"%s\" %s %s 0"%(dsn,path,mac,ca_type[i])).read() #0=D3.0 CA Key,1 = D3.1 CA Key
        print data
        if "PASS" in data:
            msg="Get D3.0 CA Key Success %s"%mac
        else: 
            raise Except ("ErrorCode(0002):Get D3.0 CA key error %s %s"%(mac,ca_type))
        file_size=os.path.getsize("%s/%s.%s"%(path,doc_ca,ca_type[i]))
        if file_size>1000: raise Except ("failed:Check file size %s.%s"%(doc_ca,ca_type[i])) ##check size
        else: d30_size.append(file_size)
    argv[4]("CA_3.0(%s.cer,size:%d | %s.prv,size:%d) Check OK"%(doc_ca,d30_size[0],doc_ca,d30_size[1]),2)  
    
    lWaitCmdTerm(term,"cmcert %s %s.cer %s.prv"%(tftp_ip,doc_ca,doc_ca),"keys saved",10,2)
    argv[4]('Install %s.cer %s.prv OK'%(doc_ca,doc_ca),2)

    #Install EMTA Key
    for k in ('PacketCable_Centralized_MTA_CA.der','CableLabs_Service_Provider_Root_CA.cer'):
        if not os.path.isfile("%s/%s"%(openssl_path,k)):
                raise Except ("ErrorCode(0002):No such file %s"%k) 

    a = "%012X"%(int(mac,16)+1)
    pkt_ca = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]  
    
    if os.path.exists("%s/%s.cer"%(path,pkt_ca)):
         os.remove("%s/%s.cer"%(path,pkt_ca))
         print "The Key is delete"
    else:print "The CA Key is Delete"
    if os.path.exists("%s/%s.prv"%(path,pkt_ca)):
         os.remove("%s/%s.prv"%(path,pkt_ca))
         print "The Key is delete"
    else:print "The CA Key is Delete"
    if os.path.exists("%s/%s.pvt"%(path,pkt_ca)):
         os.remove("%s/%s.pvt"%(path,pkt_ca))
         print "The Key is delete"
    else:print "The CA Key is Delete"

    for i in ["cer","prv"]:
        if not os.path.isfile("%s/%s.%s"%(openssl_path,pkt_ca,i)):
            #raise Except ("ErrorCode(E00170):No such file %s.%s"%(doc_ca,i)) 
            for j in range(len(ca_type)):
                data = os.popen("GetCaKey \"%s\" \"%s\" %s %s 0"%(dsn,path,a,ca_type[j])).read() 
                print data
                if "PASS" in data:
                    msg="Get EMTA Key Success %s"%mac
                else: 
                    raise Except ("ErrorCode(0002):Get EMTA key error %s %s"%(a,ca_type))
    
    EmtaContent = {'OU_new': ['PacketCable_Centralized_MTA_CA_G2.cer',
                              'OU=PC CA00001 - G2'],
                   'OU_old': ['PacketCable_Centralized_MTA_CA.der',
                              'O=CableLabs, OU=PacketCable, CN=PacketCable Root Device Certificate Authority']
                  }
                  
    if not os.path.isfile("%s/%s.cer"%(openssl_path,pkt_ca)):
            raise Except ("ErrorCode(0002):No such file %s.cer"%pkt_ca) 
    time.sleep(1)
    emta_key = open("%s\%s.cer"%(openssl_path,pkt_ca),"rb").read()
    if "PC CA00001 - G2" in emta_key:
        for k in ['PacketCable_Centralized_MTA_CA_G2.cer']:
            if not os.path.isfile("%s/%s"%(openssl_path,k)):
                raise Except ("ErrorCode(0002):No such file %s"%k) 
        veren='OU_new'                
    elif "PC CA00001" in emta_key:
        veren='OU_old' 
    
    # Install EMTA Key
    #0=NA/1=EU #1=LAN/2=WAN
    lWaitCmdTerm(term,"top","nu>",5,2)
    lWaitCmdTerm(term,"pacm","cm>",5,2)    
    lWaitCmdTerm(term,"sec","security>",5,2)
    lWaitCmdTerm(term,"certificates","tes>",5,2) 
    #getAllCerts 0 BC-4D-FB-30-C3-7A.der BC-4D-FB-30-C3-7A.prv PacketCable_Centralized_MTA_CA.der CableLabs_Service_Provider_Root_CA.cer 192.168.100.32 lan0
    ##data=lWaitCmdTerm(term,"getAllCerts 0 %s.cer %s.prv PacketCable_Centralized_MTA_CA_G2.cer CableLabs_Service_Provider_Root_CA.cer %s"%(pkt_ca,pkt_ca,tftp_ip),"tes>",30,2)     
    data=lWaitCmdTerm(term,"getAllCerts 0 %s.cer %s.prv %s CableLabs_Service_Provider_Root_CA.cer %s l2sd0.2"%(pkt_ca,pkt_ca,EmtaContent[veren][0],tftp_ip),"tes>",30,2)     
    #argv[4]('%s'%(data),2)
    argv[4]('Install %s.cer %s.prv OK'%(pkt_ca,pkt_ca),2)
    time.sleep(1)
    
    MTA_CA_G2="OU=PC CA00001 - G2"
    mac1=":".join(pkt_ca.split("-"))
    dst=[mac1, EmtaContent[veren][1],"CN=CableLabs Service Provider Root CA" ]
                
    for k in range(3):
        data=lWaitCmdTerm(argv[1][-1],"displayCertContent 0 1","tes>",10,3)
        print data
        if dst[0] in data: 
            cer_key=data.split("Inc., OU=PacketCable, ")[-1].split(", CN=CableLabs")[0].strip()
            break
        else:
            if k==2:
                argv[4]('%s'%data)
                raise Except ("%s displayCertContent 0 1 check fail"%(mac))
                
    argv[4]('%s'%data[:750])
    argv[4]("displayCertContent 0 1 pass",2)  

    data=""  
    for k in range(3):
        data=lWaitCmdTerm(argv[1][-1],"displayCertContent 0 2","tes>",10,3)
        print data
        if "OU=PacketCable" in data:
            ma_key=data.split("Inc., OU=PacketCable, ")[-1].split(", CN=CableLabs")[0].strip()
            break
        else:
            if k==2:
                argv[4]('%s'%data)
                raise Except ("%s displayCertContent 0 2 check fail"%(mac))
                
    argv[4]('%s'%data[:750])
    argv[4]("displayCertContent 0 2 pass",2)  
 
    if cer_key<>ma_key:raise Except("display Cert Content fail!(%s<>%s)"%(cer_key,ma_key))
    argv[4]('%s==%s'%(cer_key,ma_key))
    
    for k in range(3):
        data=lWaitCmdTerm(argv[1][-1],"displayCertContent 0 3","tes>",10,3)
        print data
        if dst[2] in data:break
        else:
            if k==2:
                argv[4]('%s'%data)
                raise Except ("%s displayCertContent 0 3 check fail"%(mac))
    argv[4]('%s'%data[:750])
    argv[4]("displayCertContent 0 3 pass",2) 
    
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
    mac=mac.upper()
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
          lWaitCmdTerm(argv[1][-1],"quit","#",5,3)
          lWaitCmdTerm(argv[1][-1],"cli","Menu>",10,3)
          data = lWaitCmdTerm(argv[1][-1],"Manu",">",5,2)          
          if 'Manufacture>' in data:
              break
       #wifi_key= "Cl4r0@%s"%mac[-6:] 
       wifi_key = GenerateLGIWIFIKey()
       if len(wifi_key) <> 12:
          raise Except('ErrorCode(0000):Check WiFi key Fali,%s'%wifi_key)
       argv[1][-1].get()
       data=lWaitCmdTerm(argv[1][-1],"wpaKeyset %s"%wifi_key,"ure>",5)
       argv[4]('%s'%data)
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

def InstallWpakey(*argv):
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
    lWaitCmdTerm(argv[1][-1],"Manu","Manufacture>",5,2) 
    #wifi_key= "Cl4r0@%s"%mac[-6:] 
    wifi_key = GenerateLGIWIFIKey()
    if len(wifi_key) <> 12:
      raise Except('ErrorCode(0000):Check WiFi key Fali,%s'%wifi_key)
    argv[1][-1].get()
    data=lWaitCmdTerm(argv[1][-1],"wpaKeyset %s"%wifi_key,"ure>",5)
    argv[4]('%s'%data)
    argv[4]('Install Wpakey %s OK'%wifi_key)
       

def InstallAtom(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    if os.path.isfile('c:\\station.ini'):
        execfile('c:\\station.ini') 

    ComPort_list={1:"com1",
                  2:"com2",
                  3:"com3",
                  4:"com4",
                  5:"com5",
                  6:"com6",
                  7:"com7",
                  8:"com8"               
                  }

    #mac,sn = argv[2][:2]
    mac = argv[2][0]
    sn = GetSN(mac)
    c_port = argv[0]

    term=htx.SerialTTY(ComPort_list[(c_port+1)],115200)
    a = ""
    for i in range(0,len(mac),2):
        if i < 10: 
            a = a + mac[i:i+2] + ":"
        elif i == 10: a = a + mac[i:i+2]
        else: break
    print a
    term<<"\n"
    time.sleep(0.5)
    term<<"root"
    time.sleep(0.5)
    lWaitCmdTerm(term,"root","~#",5,2)
    #data=lWaitCmdTerm(term,"htx_wls_mac_cmd %s"%a,"MAC RESET --> Done",35)
    data=lWaitCmdTerm(term,"htx_wls_mac_cmd %s"%a,"#",35)
    #print data
    argv[4]('%s'%data)
    lWaitCmdTerm(term,"htx_wls_mac_cmd setAntType pro","#",5,2)
    lWaitCmdTerm(term,"htx_wls_dm_cmd setSN %s"%sn,"#",5,2)
    #lWaitCmdTerm(term,"htx_wls_mac_cmd setAntType CGNV5_PRO_3x3+4x4","#",10,1)
    #time.sleep(0.5)
    #lWaitCmdTerm(term,"htx_wls_mac_cmd setAntType CGNV5_PRO_3x3+4x4","#",10,1)
    #lWaitCmdTerm(term,"htx_wls_mac_cmd setAntType CGNV5_STN_3x3+3x3","#",10,1)
    #lWaitCmdTerm(term,"htx_wls_mac_cmd setAntType CGNV5_MAX_2x2+3x3","#",10,1)
    data=lWaitCmdTerm(term,"htx_wls_mac_cmd getAntType","#",5,2)
    argv[4]('%s'%data)
    #lWaitCmdTerm(term,"htx_wls_dm_cmd freset","#",25,1)
    argv[4]('Install Atom mac %s OK'%a)

def CheckWifiInterface(i,term,cmd,wait_cmd,time_out,log): 
    test_time = time.time()
    while (time.time()- test_time) < time_out: 
          #data = lWaitCmdTerm(term,"iwconfig ath4",'#',3)
          term.get()
          term << cmd
          data = term.wait('#',2)[-1]
          print data
          if i=='5G':
            if wait_cmd in data or 'CLARO' in data:
              #print data
              log("%s"%data)
              return 1
          else:
            if wait_cmd in data or 'CLARO' in data:
              #print data
              log("%s"%data)
              return 1
          print 'Retry iwconfig check wifi interface'            
          time.sleep(10)
    log("%s"%data)
    return 0


def WifiSsid(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    if os.path.isfile('c:\\station.ini'):
        execfile('c:\\station.ini') 

    ComPort_list={1:"com1",
                  2:"com2",
                  3:"com3",
                  4:"com4",
                  5:"com5",
                  6:"com6",
                  7:"com7",
                  8:"com8"               
                  }

    #mac,sn = argv[2][:2]
    mac = argv[2][0]
    sn = GetSN(mac)
    c_port = argv[0]
    log=argv[4]
    term=htx.SerialTTY(ComPort_list[(c_port+1)],115200)
    a = ""
    for i in range(0,len(mac),2):
        if i < 10: 
            a = a + mac[i:i+2] + ":"
        elif i == 10: a = a + mac[i:i+2]
        else: break
    print a

    ssid_5g='HITRON5G-%s'%mac[-4:] 
    ssid_2g='HITRON-%s'%mac[-4:] 
    wifi_interface={'2G':['iwconfig wlan0','802.11bgn  ESSID:"HITRON',80],
                  '5G':['iwconfig wlan2','802.11anac  ESSID:"HITRON5G',50]
                 }
    keystr=range(1,12)
    random.shuffle(keystr)
    channel=keystr[0] 
    s_time=time.time()
    term<<"\n"
    time.sleep(0.5)
    term<<"root"
    time.sleep(0.5)
    lWaitCmdTerm(term,"root","#",5,2)
    
    for band in ['2G', '5G']:
      if not CheckWifiInterface(band,term,wifi_interface[band][0],wifi_interface[band][1],wifi_interface[band][2],log):
        #print CheckWifiInterface(band,term,wifi_interface[band][0],wifi_interface[band][1],wifi_interface[band][2],log)
        raise Except("failed: %s boot up fail\n"%band)  
      
    for i in range(3):
      lWaitCmdTerm(term,"fapi_wlan_cli setSsid -i 0 -s %s"%ssid_2g,'FAPI Command Success',30) #0: wlan0
      lWaitCmdTerm(term,"fapi_wlan_cli setSsid -i 2 -s %s"%ssid_5g,'FAPI Command Success',30) #2: wlan2
      lWaitCmdTerm(term,"fapi_wlan_cli setBeaconType -i 0 -p None",'FAPI Command Success',30)    # Encryption:off
      lWaitCmdTerm(term,"fapi_wlan_cli setBeaconType -i 2 -p None",'FAPI Command Success',30)
      lWaitCmdTerm(term,"fapi_wlan_cli setChannel -i 0 -c %s"%channel,'#',25)
      argv[4]("2g_channel=%s"%channel,2)
      lWaitCmdTerm(term,"fapi_wlan_cli setChannel -i 2 -c 44",'FAPI Command Success',30)
      #lWaitCmdTerm(term,'fapi_wlan_cli setChannelMode -i 0 -p "11NGHT40PLUS"','FAPI Command Success',30)
      #lWaitCmdTerm(term,'fapi_wlan_cli setChannelMode -i 2 -p "11ACVHT40"','FAPI Command Success',30)
      #time.sleep(1)
      lWaitCmdTerm(term,"fapi_wlan_cli apply",'root@intel_ce_linux:~#',35) ## commit wifi config   ########## original
      #lWaitCmdTerm(term,"fapi_wlan_cli apply",'FAPI Command Success',35) ## commit wifi config   ##### toan 11/25
      time.sleep(15) 
      data0=lWaitCmdTerm(term,"iwconfig wlan0",'#',10,3) 
      print data0
      data2=lWaitCmdTerm(term,"iwconfig wlan2",'#',10,3) 
      print data2
      if (ssid_5g in data2) and (ssid_2g in data0):break
      if i==2:
        argv[4]("%s"%data0)
        argv[4]("%s"%data2)
        raise Except("failed: Wifi Setting Fail!") 
    argv[4]("%s"%data0)
    argv[4]("%s"%data2)
    argv[4]('total_time_cost=%dsec'%(time.time()-s_time))
    argv[4]("Wifi Setting PASS")
    term.close()
       
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


def InstallPublicKey(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    log = argv[-4]
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    path = argv[-3]('TFTPSERVER','tftprootfolder') 
    #dsn ="host='%s' dbname='test' user='test' password='test'"%CAshareIP
    dsn ="host='%s' dbname='TMSDB' user='test' password='test'"%CAshareIP
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    ca_type = ['cer','prv','pvt']    
    mta_cer_path=os.getcwd()+"\\PacketCableHitronCA"
    print mta_cer_path
    #Install EMTA Key
    mac = "%012X"%(int(mac,16)+1)
    
    if os.path.exists("%s/%s.der"%(openssl_path,mac)):
         os.remove("%s/%s.der"%(openssl_path,mac))
         print "The Key is delete"
    else:print "The CA Key is Delete"
    
    if os.path.exists("%s/%s_private.der"%(openssl_path,mac)):
         os.remove("%s/%s_private.der"%(openssl_path,mac))
         print "The Key is delete"
    else:print "The CA Key is Delete"

    build_lock.acquire()
    data=os.popen("%s\\buildkey.bat %s"%(mta_cer_path,mac)).read()
    time.sleep(0.5)
    print data
    #build_lock.release()
    
    data = os.popen("copy /y %s\\out\\%s.der %s"%(mta_cer_path,mac,openssl_path)).read()
    data = os.popen("copy /y %s\\out\\%s_private.der %s"%(mta_cer_path,mac,openssl_path)).read()
    #data = os.popen("copy /y %s\\out\\%s_public.der %s"%(mta_cer_path,mac,openssl_path)).read()
    build_lock.release()
    
    if not os.path.isfile("%s//%s.der"%(openssl_path,mac)):
        raise Except ("failed:No such file %s.der"%mac)
    if not os.path.isfile("%s//%s_private.der"%(openssl_path,mac)): 
        raise Except ("failed:No such file %s_private.der"%mac) 
        

    #0=NA/1=EU #1=LAN/2=WAN
    lWaitCmdTerm(term,"pacm","cm>",5,2)    
    lWaitCmdTerm(term,"sec","security>",5,2)
    lWaitCmdTerm(term,"certificates","tes>",5,2) 
    
    for i in ('Hitron_PacketCable_CA.509.cer','CableLabs_Service_Provider_Root.cer'):
        if not os.path.isfile("%s/%s"%(openssl_path,i)):
                raise Except ("ErrorCode(0002):No such file %s"%i) 

    data=lWaitCmdTerm(term,"getAllCerts 0 %s.der %s_private.der Hitron_PacketCable_CA.509.cer CableLabs_Service_Provider_Root.cer %s l2sd0.2"%(mac,mac,tftp_ip),"certificates>",10,2) #0=NA/1=EU   
    argv[4]('%s'%data,2)
    argv[4]('Install %s.cer %s.prv OK'%(mac,mac),2)
  
    mac1 = mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
    dst=[mac1, "C=TW, O=Hitron Technologies, OU=PacketCable, CN=Hitron Technologies PacketCable CA","CN=CableLabs Service Provider Root CA" ]
    flag=0    
    for i in range(1,4):
        data=lWaitCmdTerm(term,"displayCertContent 0 %s"%i,"tes>",5,3) #0=NA/1=EU
        #print data
        argv[4]('%s'%data[:750])
        if i==1:
           t = time.gmtime()
           current_year = int('%s'%str(t[0]))
           for b in data[:750].splitlines():
              if "Not Before" in b:start_year = int((b.split())[-2])
              if "Not After" in b:ending_year = int((b.split())[-2])
           if current_year-start_year<=1 and ending_year - start_year>=19:
                msg="Check EMta CA start date and have expired date of 20 year PASS (PASS)"
           else:
                raise Except("Check EMta CA start date and have expired date of 20 year Fail!") 
           argv[-4](msg,2)             
        if not dst[i-1] in data:
           #log('%s'%data)
           raise Except ("%s displayCertContent 0 %s check fail"%(mac,i))
        else:
           log("displayCertContent 0 %s pass"%i,2)   


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
    if os.path.exists("%s/%s.DualHitron"%(openssl_path,mac)):
    	 os.remove("%s/%s.DualHitron"%(openssl_path,mac))

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
    #argv[4]('%s'%data)
    
    mac1 = mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
    dst=[mac1, "OU=Euro-PacketCable, CN=Euro-PacketCable Root Device Certificate Authority","CN=tComLabs Service Provider Root CA" ]

    flag=0    
    for i in range(1,4):
        data=lWaitCmdTerm(argv[1][-1],"displayCertContent 1 %s"%i,"tes>",5,3)
        argv[4]('%s'%data[:750],2)
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

    
