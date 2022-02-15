import os,time,sys,thread,odbc
from WLAN import *
CML_Lock=thread.allocate_lock()
from toolslib_local import *
import htx_local

if os.path.isfile('c:\\station.ini'):
   execfile('c:\\station.ini') 
resetbutton = 'flash1'
wpsbutton = 'flash2'
powerbutton = 'flash3'
checkled = 'flash4'  

def PACM_CONFIG_EURO(*argv):
    '''
     Description: setup configuration of band to band1 in production db.
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    log = argv[-4]
    set = eval(argv[-3](argv[-2],'set')); #print band
    set=int(set)
    '''
    lWaitCmdTerm(term,"PACM_CONFIG_EURO_set %d"%set,"OK",8,3)
    time.sleep(0.1)
    lWaitCmdTerm(term,"PACM_CONFIG_EURO_set %d"%set,"OK",8,3)
    time.sleep(0.1)
    data=lWaitCmdTerm(term,"save","OK",5,3)
    time.sleep(0.1)
    log(data)
    log( "Set PACM_CONFIG_EURO is %d PASS"%set,2)
    '''    
    data=lWaitCmdTerm(term,"show","production>",5,3)
    if 'PACM_CONFIG_EURO              %d'%set not in data:
        raise Except("Check PACM_CONFIG_EURO is %d Fail!"%set)    
    log(data)

def CheckMta(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    mac = argv[2][0]
    term = argv[1][-1]
    log = argv[-4]
    pacm_pord_dic = eval(argv[-3]('Base','pacm_pord_dic'))
    lWaitCmdTerm(term,"prod","production>",5,2)       
    for try_ in range(3):
        flag = 0
        data=lWaitCmdTerm(term,"show","production>",5,2)
        #print data
        for i in pacm_pord_dic.keys():
            value=data.split(i)[-1].strip().split()[0]
            if pacm_pord_dic.get(i)<>value:
               flag = 1 
               if try_==2:raise Except("ErrorCode(0008):Test Fail:%s"%i) 
        #print value
        if not flag:break
    log(data)
    log('Check Pacm Product information PASS',2)


def WifiSetting(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
    password_ = argv[-3]('Base','shell_password').strip()
    #ssid_5g='CLARO2-%s'%mac[-6:] 
    #ssid_2g='CLARO1-%s'%mac[-6:] 
    ssid_5g='HITRON5G-%s'%mac[-4:] 
    ssid_2g='HITRON-%s'%mac[-4:]     
    wifi_interface={'2G':['iwconfig wlan0','802.11bgn  ESSID:"%s"'%ssid_2g,150],
                    '5G':['iwconfig wlan2','802.11anac  ESSID:"%s"'%ssid_5g,50]
                   }
    lWaitCmdTerm(term,"shell","Password:",5,3)
    lWaitCmdTerm(term,"%s"%password_,"#",5,3)
    for band in ['2G', '5G']:
      #wifi_info,data=CheckWifiInterface(band,term,wifi_interface[band][0],wifi_interface[band][1],wifi_interface[band][2])
      #print data
      if not CheckWifiInterface(band,term,wifi_interface[band][0],wifi_interface[band][1],wifi_interface[band][2],log):
        raise Except("failed: %s boot up fail\n"%band) 
    lWaitCmdTerm(term,"exit",">",10)
    '''
    lWaitCmdTerm(term,"script","in>",8,2)
    #lWaitCmdTerm(term,"um_auth_account_name user1 hitron","in>",8,2)
    #lWaitCmdTerm(term,"um_auth_account_password user1 password","in>",8,2)
    #2g
    lWaitCmdTerm(term,"wls_ssid_auth_mode 1 1 open","in>",8,2)
    lWaitCmdTerm(term,"wls_ssid_encrypt_type 1 1 NONE","in>",8,2) 
    lWaitCmdTerm(term,"wls_ssid_name 1 1 %s"%ssid_2g,"in>",8,2)  
    #5g
    lWaitCmdTerm(term,"wls_ssid_auth_mode 2 1 open","in>",8,2)   
    lWaitCmdTerm(term,"wls_ssid_encrypt_type 2 1 NONE","in>",8,2)
    lWaitCmdTerm(term,"wls_ssid_name 2 1 %s"%ssid_5g,"in>",8,2)  #5g ssid 
    lWaitCmdTerm(term,"wls_radio_channel 2 44","in>",8,2)
    #lWaitCmdTerm(term,"commit","in>",35)
    term<<"commit"
    data=term.wait("Main>",40)
    print data  
    log("Clear the password & Setting ssid PASS",2)
    '''
def CheckWifiInterface(i,term,cmd,wait_cmd,time_out,log): 
    test_time = time.time()
    while (time.time()- test_time) < time_out: 
          #data = lWaitCmdTerm(term,"iwconfig ath4",'#',3)
          term.get()
          term << cmd
          data = term.wait('#',2)[-1]
          print data
          if i=='5G':
            if wait_cmd in data:
              #print data
              log("%s"%data)
              return 1
          else:
            if wait_cmd in data:
              #print data
              log("%s"%data)
              return 1
          print 'Retry iwconfig check wifi interface'            
          time.sleep(10)
    log("%s"%data)
    return 0


def USBTest_CODA(*argv):
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

    #term = argv[1][-1]
    c_port = argv[0]
    term=htx.SerialTTY(ComPort_list[(c_port+1)],115200)
    lWaitCmdTerm(term,"root","#",5)
    openssl_path = argv[-3]('TFTPSERVER','tftprootfolder')
    usb_disk = argv[-3]('Base','USB_Disk')
    mta_cer_path = os.getcwd()
    log = argv[-4]
    argv[3](powerbutton)
    vlan = map(integer,argv[-3]('AFI','VLAN1IP').split('.'))
    sid = int(argv[1][2].host.split(',')[-1].split(')')[0])
    tftp_ip = '%s.%s.%s.%s'%(vlan[0],vlan[1],vlan[2],vlan[3]+(sid-1)*4)
    usb_key = eval(argv[-3](argv[-2],'type'))
    
    usb_type={2.0:['usbtest.dat','6544'],
              3.0:['usbtest.dat','Bus 002 Device 003']
              }
            
    for k in xrange(3):
        #try:     
        for i in range(120):
            data=""
            data=lWaitCmdTerm(term,"lsusb -t","#",5)
            print data
            if data.count("ID")==4:break
            else:
                print i
                if i==119:
                  argv[-4]("%s"%data)
                  raise Except ("ErrorCode(E00146):Check USB type fail")
                time.sleep(1)
        
        argv[-4]("%s"%data,2)
    
        for i in range(5):
            term.get()
            mount_data = lWaitCmdTerm(term,"mount","#",5)
            print mount_data
            print "/dev/sda1 on %s"%usb_disk
            #print mount_data.index("/dev/sda1 on %s"%usb_disk)
            if "/dev/sda1 on" in mount_data:
                addr1 = mount_data.split("/dev/sda1 on")[1].strip().split()[0].strip()
                argv[-4]("%s"%mount_data) 
                break
            else:
                if i==4:
                  argv[-4]("%s"%mount_data) 
                  raise Except ("ErrorCode(E00146):Please Check the USB%s device."%usb_key)
                time.sleep(8)
        data1 = lWaitCmdTerm(term,"ls %s"%addr1,"#",5,3)
        print data1
        if 'usbtest.dat' in data1 or 'test.txt' in data1:
          msg='Check USB Content PASS'
          argv[-4]("%s"%msg,2)
        else:
          argv[-4]("%s"%data1)
          raise Except("ErrorCode(E00146):Check USB Content FAIL.")
        log("USB%s TEST PASS"%usb_key,2)
        return
        #except:
        #  raise Except ("ErrorCode(E00146):USB%s Test failed"%usb_key)

def WaitingAndCheckBoot_AFI0(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    Telnet IP = 192.168.84.100/200
    DUT1/2/3/4 = 3021/3031/3041/3051 
    '''
    menu = argv[-3]('Base','Menu').strip()
    customer = argv[-3]('Base','Customer').strip()
    customer2 = argv[-3]('Base','Customer2').strip()
    afi = eval(argv[-3](argv[-2],'afi_station'))
    term = argv[1][-1]
    #lWaitCmdTerm(argv[1][1],'rf %s n'%(c_port+1),'OK',5)
    for try_ in range(3):
        lWaitCmdTerm(term,'cli','mainMenu>',8,2)  
        lWaitCmdTerm(term,'docsis','docsis>',5,2)      
        for i in range(3):
            section = lWaitCmdTerm(term,'dir','docsis>',5,2)
            if section.count(customer) == 2 and ("Filename in sector 2->%s"%customer2 in section):
            #if ("Filename in sector 1->%s"%customer1 in section) and ("Filename in sector 2->%s"%customer2 in section):
               argv[4](section)
               break               
            else:
               if i==2:raise Except('ErrorCode(214032):check section falied : %s'%section)
                              
        for i in range(3):
            if 'Selected sector is 1' not in section and 'Selected sector is 2' not in section and 'Last downloaded Filename->'not in section:
               section = lWaitCmdTerm(term,'dir','is>',5,3)
               if i == 2:
                  raise Except('ErrorCode(0000):UART character lost  %s'%section)
            else:break
        if afi==0:sec=2
        else:sec=1   
        if 'Selected sector is %s'%sec in section:           
           argv[4]('Selected sector %s check pass'%sec,2)            
        else:
           lWaitCmdTerm(argv[1][-1],'bootfrom %s'%sec,'is>',5,3)
           raise Except('Please restart DUT again') 
           '''
           lWaitCmdTerm(argv[1][-1],'reboot','to abort autoboot',30)
           time.sleep(30)
           lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5)
           continue            
           '''             
        return 
    raise Except('ErrorCode(0001):Program execution exception')
    
def RemoveDsCalTable(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]    
    term = argv[1][-1]
    table='MxL267'
    password_ = argv[-3]('Base','shell_password').strip()
    
    lWaitCmdTerm(term,"shell","Password:",5,3)
    lWaitCmdTerm(term,"%s"%password_,"#",5,3)
    
    for i in range(3):
        data=lWaitCmdTerm(term,"ls nvram/1/DownstreamCal/","#",5)
        print data
        if table in data:
            lWaitCmdTerm(term,"rm nvram/1/DownstreamCal/%s"%table,"#",5)
            if i==2:raise Except ("Fail:Remove file %s"%table)
            continue
        else:
            argv[4]("Remove file %s PASS"%table,2)
            break
            
    lWaitCmdTerm(term,"exit","mainMenu>",8)                
    
def WaitingAndCheckBoot(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    Telnet IP = 192.168.84.100/200
    DUT1/2/3/4 = 3021/3031/3041/3051 
    '''
    menu = argv[-3]('Base','Menu').strip()
    customer1 = argv[-3]('Base','Customer1').strip()
    customer2 = argv[-3]('Base','Customer2').strip()
    ETH0IP = argv[-3]('AFI','ETH0IP').split('|')
    ETH0IP_ = ETH0IP[0].strip()
    c_port = argv[0]
    #if argv[0] > 3 : c_port = argv[0] - 4 ##console test
    print argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4
       ETH0IP_ = ETH0IP[1].strip()
    port = c_port + 1
    pid = '30%s1'%(port+1)
    timeout = int(argv[-3](argv[-2],'timeout'))
    username = argv[-3]('Base','username').strip()
    password_ = argv[-3]('Base','password_').strip()
    argv[1][-1] = lLogin(ETH0IP_,pid,username,password_)
    term = argv[1][-1]

    lWaitCmdTerm(argv[1][1],'rf %s n'%(c_port+1),'OK',5)
    for try_ in range(3):
        argv[1][-1] << 'cli'
        data=argv[1][-1].wait(menu,15)[-1]
        if not data :raise Except('Telnet Connect fail')
        print data
        term << ""
        data=term.wait('\n',5)[-1]
        if not data :raise Except('Telnet Connect fail')
        if 'MXP>' in data: term << 'exit\n'
        else : term << 'top\n'
        time.sleep(1)           

        lWaitCmdTerm(term,'docsis','is>',5,3)
        #for i in range(3):
        #    section = lWaitCmdTerm(term,'dir','sis>',5,3)
        #    if section.count(customer) <> 3 :
        #       if i==2:raise Except('ErrorCode(214032):check section falied : %s'%section)
        #    else:
        #       argv[4](section)
        #       break
        for i in range(3):
            section = lWaitCmdTerm(term,'dir','sis>',5,3)
            if section.count(customer2) <> 2 and  customer1 not in section:
               if i==2:raise Except('ErrorCode(214032):check section falied : %s'%section)
            else:
               argv[4](section)
               break
        for i in range(3):
            if 'Selected sector is 1' not in section and 'Selected sector is 2' not in section and 'Last downloaded Filename->'not in section:
               section = lWaitCmdTerm(term,'dir','is>',5)
               if i == 2:
                  raise Except('ErrorCode(0000):UART character lost  %s'%section)
            else:break
            
        if 'Selected sector is 1' in section:
           lWaitCmdTerm(term,'bootfrom 2','is>',5,2)
           lWaitCmdTerm(argv[1][-1],'reboot','to abort autoboot',30)
           time.sleep(30)
           lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5)
           continue
        else:
            argv[4]('Selected sector check pass',2)
        return 
    raise Except('ErrorCode(0001):Program execution exception')
    

def TurnToGAmode(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    lWaitCmdTerm(argv[1][-1],"quit","#",8)
    for i in range(5):
        lWaitCmdTerm(argv[1][-1],"setenv MFG no","#",5,3)
        #data = lWaitCmdTerm(argv[1][-1],"printenv","#",5,3)
        argv[1][-1].get()
        argv[1][-1]<<"printenv"
        time.sleep(2)
        data=argv[1][-1].get()
        print data
        print "1111111111111111111111111111111"
        #print str(data[4000:]).split("MFG=")[-1].split('\r\n')[0]
        if "MFG=no" in str(data):break
        else:
          if i==4:raise Except('ErrorCode(0001):Turn to GA mode fail')
          time.sleep(1)
    argv[4]('Turn to GA mode Pass',2)
    lWaitCmdTerm(argv[1][-1],"cli","mainMenu>",10,2)
    lWaitCmdTerm(argv[1][-1],"doc","docsis>",10)
    for i in range(3):
        data=lWaitCmdTerm(argv[1][-1],"bootfrom 1","docsis>",10)
        if "Sector changed to 1" in str(data):break
        else:
            time.sleep(1)
            if i==2:raise Except("Change bootfrom 1 fail")
    argv[4]('%s'%data)


def Checkbootfrom1(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    menu = argv[-3]('Base','Menu').strip()
    customer = argv[-3]('Base','Customer').strip()
    c_port = argv[0]
    if argv[0] > 3 : c_port = argv[0] - 4           
    section = lWaitCmdTerm(argv[1][-1],'dir','docsis>',5,2)   
    if 'Selected sector is 2' in section:
       lWaitCmdTerm(argv[1][-1],'bootfrom 1','is>',5,2)
       lWaitCmdTerm(argv[1][-1],'reboot','Press @ to abort',20)
       time.sleep(1)
       lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5,2)
       time.sleep(40)
       lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5,2)
       for k in range(10):
           data=argv[1][-1].wait('\n',5)[-1]
           if not data :
              if k == 9:
                 raise Except('Console Connect fail')
              time.sleep(1)
           else:break
       argv[1][-1] << 'quit\n'
       argv[1][-1].get()               
       lWaitCmdTerm(argv[1][-1],'cli',menu,8,10)
       lWaitCmdTerm(argv[1][-1],'docsis','is>',5,3)
       section = lWaitCmdTerm(argv[1][-1],'dir','docsis>',5,3) 
       if 'Selected sector is 1' in section and section.count(customer) == 3:
          argv[4]('%s\nSelected sector 1 check pass'%section,2)             
       else:raise Except('%s\nSelected sector 1 check fail'%section) 
    else:
       argv[4]('%s\nSelected sector 1 check pass'%section,2)
        

def Enable_telnet(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms :
    term = argv[1][-1] ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    lWaitCmdTerm(term,"telnetd","Choice >",5,2)
    lWaitCmdTerm(term,"1","Choice >",10)
    lWaitCmdTerm(term,"1","Choice >",10)
    data=lWaitCmdTerm(term,"1","Set OK!",10)
    #print data
    #argv[4]('change Telnet Daemon %s OK'%data)
    '''
    lWaitCmdTerm(term,"","docsis>",5)
    lWaitCmdTerm(term,"httpd","Choice >",5,2)
    lWaitCmdTerm(term,"1","Choice >",10)
    lWaitCmdTerm(term,"1","Choice >",10)
    data=lWaitCmdTerm(term,"1","Set OK!",10)
    #print data
    argv[4]('change HTTP Daemon %s OK'%data)
    lWaitCmdTerm(term,"","docsis>",5)
    lWaitCmdTerm(term,"dhcpd","Choice >",5,2)
    data=lWaitCmdTerm(term,"1","Set OK!",10)
    #print data
    argv[4]('change DHCP Daemon %s OK'%data)
    '''
    argv[-4]("Enable Telnet pass",2)   


def Checkra0(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    for try_ in range(30):
        data = lWaitCmdTerm(argv[1][-1],"ifconfig ath0","#",5,3)
        #print data
        if 'ath0      Link' in data:
            argv[4]('ifconfig ath0 check pass',2)
            break
        elif try_==29:
            raise Except("ErrorCode(E00138):ifconfig ath0 check fail") 
        time.sleep(1)

def Switch4Port(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''  
    speed = argv[-3](argv[-2],'Speed').strip()
    count,size,interval,ping_loss = map(integer,map(strip,argv[-3]('Base','PingParameter').split('|')))
    ip = argv[-3]('Base','LANIP').strip()
    lWaitCmdTerm(argv[1][2],'cable 0 l','cable',5,2)
    if speed=='1000F':
       lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2)
    else:
       lWaitCmdTerm(argv[1][2],'speed 0 %s'%speed,'speed',5,2)
    
    for try__ in range(6):
        speeds=lWaitCmdTerm(argv[1][2],'status 0','status',5,2)
        print speeds
        if speeds.count(speed)==4:break
        if try__==5:
           raise Except('ErrorCode(E00183):Ether Switch Speed %s(%s)'%(speed,speeds.split('\n')[-1]))
        time.sleep(3)  
    speeds=speeds.split()[-1].split(',')    
    for port in range(4):
        argv[1][2] << 'ping %s %s %s %s %s'%(port+1,ip,size,count,interval)   
        time.sleep(1)
        
    losts=['error']*4
    id_ = int(argv[1][2].host[-2])
    for try_ in range(15):
        flag=1
        #time.sleep(1)
        loss=argv[1][2].wait('%',6)[-1]
        print loss
        for port in range(4):
            if 'vlan%s%s'%(id_,port+1) in loss:
               value=int(loss.split('vlan%s%s'%(id_,port+1))[-1].split('%')[0].split()[-1]) 
               print value
               if value > ping_loss:
                  flag=0
                  argv[1][2] << 'ping %s %s %s %s %s'%(port+1,ip,size,count,interval)    
                  time.sleep(1)
               else:
                  losts[port]= value 
               if try_==14:
                  losts[port]= value    
        if 'error' not in losts:break    
    for port in range(4):
        message = 'Switch  Port %s %s Long Ping lost : %s ( <= %s ) speed: %s ( %s )'%(port,speed,losts[port],ping_loss,speeds[port],speed) 
        if losts[port] > ping_loss:
           raise Except('ErrorCode(E00155):%s'%message)
        argv[-4]('%s'%message)
    argv[-4]('4Port (%s) Switch Ping Pass'%speed,2)    

def Switch4Port_1000F(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''  
    speed = argv[-3](argv[-2],'Speed').strip()
    count,size,interval,ping_loss = map(integer,map(strip,argv[-3]('Base','PingParameter').split('|')))
    ip = argv[-3]('Base','LANIP').strip()
    lWaitCmdTerm(argv[1][2],'cable 0 l','cable',5,2)
    if speed=='1000F':
       lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2)
    else:
       lWaitCmdTerm(argv[1][2],'speed 0 %s'%speed,'speed',5,2)
    
    for try__ in range(6):
        speeds=lWaitCmdTerm(argv[1][2],'status 0','status',5,2)
        print speeds
        if speeds.count(speed)==4:break
        if try__==5:
           raise Except('ErrorCode(E00183):Ether Switch Speed %s(%s)'%(speed,speeds.split('\n')[-1]))
        time.sleep(3)  
    speeds=speeds.split()[-1].split(',')    
        
    id_ = int(argv[1][2].host[-2])   
    for port in range(4):
        lWaitCmdTerm(argv[1][2],'cable 0 o','cable',5,2)
        lWaitCmdTerm(argv[1][2],'cable %s l'%(port+1),'cable',5,2)    
        for try_ in range(5):
            data = lWaitCmdTerm(argv[1][2],'status %s'%(port+1),'status',5,2)  
            if '1000F' in data:break
            time.sleep(1)                    
        value = 'error'
        for try_ in range(3):
            argv[1][2] << 'ping %s %s %s %s %s'%(port+1,ip,size,count,interval)  
            loss=argv[1][2].wait('%',20)[-1]
            try:
               value=int(loss.split('vlan%s%s'%(id_,port+1))[-1].split('%')[0].split()[-1]) 
               if value <= ping_loss:break
            except:pass
        message = 'Switch  Port %s %s Long Ping lost : %s ( <= %s ) speed: %s ( %s )'%(port,speed,value,ping_loss,speeds[port],speed) 
        if value == 'error' or value > ping_loss:
           raise Except('ErrorCode(E00155):%s'%message)
        argv[-4]('%s'%message)
    lWaitCmdTerm(argv[1][2],'cable 1 s','cable',5,2)
    time.sleep(2)
    argv[-4]('4Port (%s) Switch Ping Pass'%speed,2)  


def Switch4Port_100F(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''  
    speed = argv[-3](argv[-2],'Speed').strip()
    count,size,interval,ping_loss = map(integer,map(strip,argv[-3]('Base','PingParameter').split('|')))
    ip = argv[-3]('Base','LANIP').strip()
    lWaitCmdTerm(argv[1][2],'cable 0 l','cable',5,2)
    if speed=='1000F':
       lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2)
    else:
       lWaitCmdTerm(argv[1][2],'speed 0 %s'%speed,'speed',5,2)
    
    for try__ in range(6):
        speeds=lWaitCmdTerm(argv[1][2],'status 0','status',5,2)
        print speeds
        if speeds.count(speed)==4:break
        if try__==5:
           raise Except('ErrorCode(E00183):Ether Switch Speed %s(%s)'%(speed,speeds.split('\n')[-1]))
        time.sleep(3)  
    speeds=speeds.split()[-1].split(',')    
        
    id_ = int(argv[1][2].host[-2])   
    for port in range(4):
        lWaitCmdTerm(argv[1][2],'cable 0 o','cable',5,2)
        lWaitCmdTerm(argv[1][2],'cable %s l'%(port+1),'cable',5,2)    
        for try_ in range(5):
            data = lWaitCmdTerm(argv[1][2],'status %s'%(port+1),'status',5,2)  
            if '100F' in data:break
            time.sleep(1)                    
        value = 'error'
        for try_ in range(3):
            argv[1][2] << 'ping %s %s %s %s %s'%(port+1,ip,size,count,interval)  
            loss=argv[1][2].wait('%',20)[-1]
            try:
               value=int(loss.split('vlan%s%s'%(id_,port+1))[-1].split('%')[0].split()[-1]) 
               if value <= ping_loss:break
            except:pass
        message = 'Switch  Port %s %s Long Ping lost : %s ( <= %s ) speed: %s ( %s )'%(port,speed,value,ping_loss,speeds[port],speed) 
        if value == 'error' or value > ping_loss:
           raise Except('ErrorCode(E00155):%s'%message)
        argv[-4]('%s'%message)
    lWaitCmdTerm(argv[1][2],'cable 1 s','cable',5,2)
    time.sleep(2)
    argv[-4]('4Port (%s) Switch Ping Pass'%speed,2)  

def Switch1Port(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''  
    speed = argv[-3](argv[-2],'Speed').strip()
    count,size,interval,ping_loss = map(integer,map(strip,argv[-3]('Base','PingParameter').split('|')))
    ip = argv[-3]('Base','LANIP').strip()
    lWaitCmdTerm(argv[1][2],'cable 0 l','cable',5,2)
    if speed=='1000F':
       lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2)
    else:
       lWaitCmdTerm(argv[1][2],'speed 0 %s'%speed,'speed',5,2)
    
    for try__ in range(6):
        speeds=lWaitCmdTerm(argv[1][2],'status 0','status',5,2)
        print speeds
        if speeds.count(speed)==1:break
        if try__==5:
           raise Except('ErrorCode(E00183):Ether Switch Speed %s(%s)'%(speed,speeds.split('\n')[-1]))
        time.sleep(3)  
    speeds=speeds.split()[-1].split(',')    
    for port in range(1):
        argv[1][2] << 'ping %s %s %s %s %s'%(port+1,ip,size,count,interval)   
        time.sleep(1)
        
    losts=['error']
    id_ = int(argv[1][2].host[-2])
    for try_ in range(15):
        flag=1
        #time.sleep(1)
        loss=argv[1][2].wait('%',6)[-1]
        print loss
        for port in range(1):
            if 'vlan%s%s'%(id_,port+1) in loss:
               value=int(loss.split('vlan%s%s'%(id_,port+1))[-1].split('%')[0].split()[-1]) 
               print value
               if value > ping_loss:
                  flag=0
                  argv[1][2] << 'ping %s %s %s %s %s'%(port+1,ip,size,count,interval)    
                  time.sleep(1)
               else:
                  losts[port]= value 
               if try_==14:
                  losts[port]= value    
        if 'error' not in losts:break    
    for port in range(1):
        message = 'Switch  Port %s %s Long Ping lost : %s ( <= %s ) speed: %s ( %s )'%(port,speed,losts[port],ping_loss,speeds[port],speed) 
        if losts[port] > ping_loss:
           raise Except('ErrorCode(E00155):%s'%message)
        argv[-4]('%s'%message)
    argv[-4]('1Port (%s) Switch Ping Pass'%speed,2)    

def ResetButton_back(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    c_port = argv[0]
    if argv[0] > 3 : c_port = argv[0] - 4
    argv[3](resetbutton)
    lWaitCmdTerm(argv[1][-1],'ErrorCode(E00225):Reset Button Falied','Compressed file is LZMA format',60) 
    argv[-4]('Reset Button Test Pass',2) 
    lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5,2)

def ResetButton(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    ResetButton = "Reset button pressed"
    timeout = eval(argv[-3](argv[-2],'timeout'))
    c_port = argv[0]
    if argv[0] > 3 : c_port = argv[0] - 4
    argv[3](resetbutton)
    #lWaitCmdTerm(argv[1][-1],'ErrorCode(E00138):Reset Button Falied',ResetButton,60) 

    etime=time.time()+timeout
    while time.time()<= etime:
        data = lWaitCmdTerm(argv[1][-1],'Reset_Button','',5) 
        print data
        if ResetButton in data:
           argv[-4]('Reset Button Test Pass',2)   
           return
    raise Except('ErrorCode(00138):Reset Button Falied') 

def ResetButton_ping(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    ResetButton = "Reset button pressed"
    c_port = argv[0]
    if argv[0] > 3 : c_port = argv[0] - 4
    argv[3](resetbutton)
    
    for p in range(20):
        time.sleep(3)
        data = lWaitCmdTerm(argv[1][2],'ping 1 192.168.100.1 -n 1','ping',8,2)
        if '100%' in data:break 
        else:            
            if p==19 :raise Except('ErrorCode(E00155):Not Press Reset Button within 60s')     
    argv[-4]('Reset Button Test Pass',2) 
    #lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5,2)


def WaitResetboot(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    menu = argv[-3]("Base","menu")
    term = argv[1][-1]
    c_port = argv[0]
    if argv[0] > 3 : c_port = argv[0] - 4    
    time.sleep(35)

    lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5,3)
    lWaitCmdTerm(term,'reboot for startup is disable',"",5,5)    
    term.get()
    for i in range(30):
        term << 'ifconfig'
        data = term.wait('lo        Link',5)[-1]
        if 'lo        Link' in data:break             
    #lWaitCmdTerm(argv[1][-1],"ifconfig","lo        Link",8,15)
    lWaitCmdTerm(argv[1][-1],"docsis_init_once","/nvram/1/lsddb.ini",10,3)
    #lWaitCmdTerm(argv[1][-1],"ht_init init","#",10)
    lWaitCmdTerm(argv[1][-1],'testmode',menu,60)
    #lWaitCmdTerm(argv[1][-1],"/usr/sbin/router_init.sh","#",20)
    #lWaitCmdTerm(argv[1][-1],'cli',menu,5,2)
    argv[-4]('Reset boot pass',2)
    ''''
    lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5)
    #lWaitCmdTerm(argv[1][-1],'reboot for startup is disable',"#",3,5)
    lWaitCmdTerm(argv[1][-1],"ifconfig","lo        Link",8,15)
    lWaitCmdTerm(argv[1][-1],"docsis_init_once","/nvram/1/lsddb.ini",10,3)
    #lWaitCmdTerm(argv[1][-1],"ht_init init","#",10)
    lWaitCmdTerm(argv[1][-1],'testmode',menu,40)
    #lWaitCmdTerm(argv[1][-1],"/usr/sbin/router_init.sh","#",20)
    #lWaitCmdTerm(argv[1][-1],'cli',menu,5,2)
    argv[-4]('Reset boot pass',2)
    '''
    
def WaitResetboot_RES(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    menu = argv[-3]("Base","menu")
    c_port = argv[0]
    if argv[0] > 3 : c_port = argv[0] - 4    
    time.sleep(20)
    lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5,3)
    lWaitCmdTerm(argv[1][-1],'reboot for startup is disable',"#",3,5)
    time.sleep(30)
    lWaitCmdTerm(argv[1][-1],"","#",10)
    lWaitCmdTerm(argv[1][-1],"docsis_init_once","#",10)
    lWaitCmdTerm(argv[1][-1],"ht_init init","#",10)
    lWaitCmdTerm(argv[1][-1],'testmode',menu,10)
    argv[-4]('Reset boot pass',2) 
    
def WaitReboot(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    c_port = argv[0]
    if argv[0] > 3 : c_port = argv[0] - 4  
    lWaitCmdTerm(argv[1][-1],'setstartup -e',"#",5)  
    lWaitCmdTerm(argv[1][-1],'reboot','to abort autoboot ',50)
    #lWaitCmdTerm(argv[1][-1],'reset prod','to abort autoboot ',50)   # path is wrong 
    lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5,3)
    time.sleep(50)
    lWaitCmdTerm(argv[1][1],'rf %s c'%(c_port+1),'OK',5)
    lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5,3)
    lWaitCmdTerm(argv[1][-1],"Wait Reboot","#",5,10)
    argv[-4]('Reboot pass',2)    

def WaitReboot_CDA3(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    c_port = argv[0]
    menu = argv[-3]("Base","menu")
    ETH0IP = argv[-3]('AFI','ETH0IP').split('|')
    ETH0IP_ = ETH0IP[0].strip()
    if argv[0] > 3 : 
       c_port = argv[0] - 4
       ETH0IP_ = ETH0IP[1].strip()
    port = c_port + 1
    pid = '30%s1'%(port+1)
    timeout = int(argv[-3](argv[-2],'timeout'))
    username = argv[-3]('Base','username').strip()
    password_ = argv[-3]('Base','password_').strip()
    term = argv[1][-1] 
    
    #lWaitCmdTerm(argv[1][-1],"top","nu>",8,2)               
    lWaitCmdTerm(argv[1][-1],"doc","sis>",5,3)
    lWaitCmdTerm(argv[1][-1],"Production","ion>",5,2)  
    #lWaitCmdTerm(argv[1][-1],"Prod",":",8,2)
    #lWaitCmdTerm(argv[1][-1],"D0nt4g3tcda3","ion>",8,2)       
    lWaitCmdTerm(argv[1][-1],"Calibration","ion>",5,2)  
    lWaitCmdTerm(argv[1][-1],"Do","ion>",5,2) 
    lWaitCmdTerm(argv[1][-1],"exit","#",8,1)
    lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5,2)
    time.sleep(55)
    #lWaitCmdTerm(argv[1][1],'rf %s c'%(c_port+1),'OK',5,2)
    lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5,2)
    #argv[1][-1] = lLogin(ETH0IP_,pid,username,password_) #Telnet again
    lWaitCmdTerm(argv[1][-1],"Wait Rebooot",'#',5,10)
    argv[-4]('Waiting DUT up pass',2) 

def WaitResetboot_telnet(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    time.sleep(120)    
    for p in range(15):
        time.sleep(6)
        data = lWaitCmdTerm(argv[1][2],'ping 1 192.168.100.1 -n 1','ping',8,2)
        print data
        if '100%' not in data:break             
        if p==14 :raise Except('ErrorCode(E00155):Reset boot failed') 
    argv[-4]('Waiting DUT up pass',2) 
    time.sleep(3)

def CmtsLockCheck(term,CMTS_freq,Tuner_Menu):
    data = lWaitCmdTerm(term,"phy 0","docsis>",5,5)
    data=data.split("QAM Lock:")[-1].split("Carrier offset")[0].count("YES")
    if data  == 3: 
       return 1
    else:
       if Tuner_Menu.lower()=='general':
          lWaitCmdTerm(term,"G","General>",5,5)
          lWaitCmdTerm(term,"tune %s"%CMTS_freq,"General>",5,5)
          lWaitCmdTerm(term,"exit","docsis>",5)
       else:
          lWaitCmdTerm(term,"tune %s"%CMTS_freq,"docsis>",5,5)
       time.sleep(10)
    return 0  


def WaitCMRegistration(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''

    timeout = eval(argv[-3](argv[-2],'timeout'))
    CMTS_freq = argv[-3]('Base','CMTS_freq')
    Tuner_Menu = argv[-3]('Base','Tuner_Menu')
    Telnet = eval(argv[-3]('Base','TELNET'))
    username = argv[-3]('Base','username')
    password_ = argv[-3]('Base','password_')
    cbterm = argv[1][1]
    term = argv[1][-1]

    ETH0IP = argv[-3]('AFI','ETH0IP').split('|')
    ETH0IP_ = ETH0IP[0].strip()
    c_port = argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4
       ETH0IP_ = ETH0IP[1].strip()
    port = c_port + 1
    pid = '30%s1'%(port+1)
    
    dhcp=0
    stime=time.time()
    etime=time.time()+timeout
    while time.time()<= etime:
         lWaitCmdTerm(cbterm,'rf %s c'%port,'rf',5,3)
         data = lWaitCmdTerm(argv[1][-1],"cmstatus","docsis>",5,5)
         argv[-4](data)
         if "OPERATIONAL" in data: 
            argv[-4]('\nCM Operational OK\n',2)
            return 
         if time.time()-stime>20:
            if 'NOT_SYNCHRONIZED' in data:    
               CmtsLockCheck(argv[1][-1],CMTS_freq,Tuner_Menu)
         time.sleep(10)     
    raise Except("ErrorCode(E00125):Registration %3.2f sec Timeout. [ %s ]"%((time.time()-t),data)) 
        

def WaitCMRegistration_Tune(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''

    timeout = eval(argv[-3](argv[-2],'timeout'))
    CMTS_freq = argv[-3]('Base','CMTS_freq')
    Tuner_Menu = argv[-3]('Base','Tuner_Menu')
    Telnet = eval(argv[-3]('Base','TELNET'))
    username = argv[-3]('Base','username')
    password_ = argv[-3]('Base','password_')
    cbterm = argv[1][1]
    term = argv[1][-1]

    ETH0IP = argv[-3]('AFI','ETH0IP').split('|')
    ETH0IP_ = ETH0IP[0].strip()
    c_port = argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4
       ETH0IP_ = ETH0IP[1].strip()
    port = c_port + 1
    pid = '30%s1'%(port+1)
    
    dhcp=0
    stime=time.time()
    etime=time.time()+timeout
    while time.time()<= etime:
         lWaitCmdTerm(cbterm,'rf %s c'%port,'rf',5,3)
         data = lWaitCmdTerm(argv[1][-1],"cmstatus","docsis>",5,5)
         argv[-4](data)
         #if "RANGING_COMPLETE" in data: 
         #if "DS_TOPOLOGY_RESOLUTION_IN_PROGRESS" in data:
         if "NOT_SYNCHRONIZED" not in data:
            argv[1][-1]<<"quit"
            argv[-4]('\nTune Ds freq OK\n',2)
            return 
         if time.time()-stime>20:
            if 'NOT_SYNCHRONIZED' in data:    
               CmtsLockCheck(argv[1][-1],CMTS_freq,Tuner_Menu)
         time.sleep(6)     
    raise Except("ErrorCode(E00125):Tune Ds freq fail")  

def GetWanIP(term):
    for try_ in range(6):
        data = lWaitCmdTerm(term,"ifconfig wan0","#",5,5)
        print data
        if 'inet addr' in data and "Bcast:" in data:
           break
        #if try_ == 4:lWaitCmdTerm(term,"shell","#",5,5)
        elif try_== 5:raise Except('ErrorCode(0006):Get wan ip error')
    wan_ip = data.split("inet addr:")[1].split("Bcast:")[0].strip()
    if not wan_ip:
       raise Except('ErrorCode(0006):Get wan ip error')
    return wan_ip     

def SyncTest(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    log = argv[-4]
    password_ = argv[-3]('Base','shell_password').strip()
    lWaitCmdTerm(term,"shell","Password:",5,3)
    lWaitCmdTerm(term,"%s"%password_,"#",5,3)
    lWaitCmdTerm(term,"sync","#",5,3)
    time.sleep(0.3)
    print lWaitCmdTerm(term,"sync","#",5,3)

def GetWanIPTelnet_CCR(term,shellpassword):
    for try_ in range(6):
        lWaitCmdTerm(term,"top","",5,5)
        lWaitCmdTerm(term,"shell","ord:",5,1)
        print shellpassword
        lWaitCmdTerm(term,shellpassword,"$",5,1)
        data = lWaitCmdTerm(term,"ifconfig wan0","$",5,5)
        print data
        if 'inet addr' in data and "Bcast:" in data:
           break
        elif try_==5:raise Except('ErrorCode(0006):Get wan ip error')
    wan_ip = data.split("inet addr:")[1].split("Bcast:")[0].strip()
    if not wan_ip:
       raise Except('ErrorCode(0006):Get wan ip error')
    return wan_ip         

def TunerDS_8channel(term,CMTS_freq,freq_step):
    lWaitCmdTerm(term,"Tuner","er>",5,2)
    dsfreqlist=[]
    for i in range(4):
        dsfreqlist.append(CMTS_freq + freq_step * i )
    for i in range(4):
        dsfreqlist.append(CMTS_freq + freq_step * i )

    for i in xrange(3):
        lWaitCmdTerm(term,"lock8ds %d %d %d %d %d %d %d %d"%tuple(dsfreqlist),"er>",5,3)
        #lWaitCmdTerm(term,"lockRec %d %d %d %d %d %d %d %d"%tuple(dsfreqlist),"er>",5,3)
        time.sleep(3)
        data = lWaitCmdTerm(term,"ds","Tuner>",5)
        if data.count("YES") == 24:
           break
    lWaitCmdTerm(term,"exit","st>",5)


def Check4X4UsDsLock(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    mac = argv[2][0]
    #sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    CMTS_freq = eval(argv[-3]('Base','CMTS_freq'))
    freq_step = eval(argv[-3]('Base','freq_step'))
    Ds_n = 0
    for i in range(3):
        print i 
        TunerDS_8channel(term,CMTS_freq,freq_step)
        data = lWaitCmdTerm(term,"dsstatus","st>",5,2)
        print data
        if data.count("YES") != 16:
           if i ==2:raise Except("ErrorCode(E00242):4X4 DS Lock Check: FAIL") 
        else:
           break
    log("4X4 DS Lock Check: PASS (PASS)",2)
    lWaitCmdTerm(term,"exit","ion>",5)
    lWaitCmdTerm(term,"exit","sis>",5)        
    lWaitCmdTerm(term,'Debug',"bug>",5)
    for i in range(4):
        try:
            Ds_n=0
            data = lWaitCmdTerm(term,'usstatus',"ug>",5)
            US = data.split("Upstream    :")[-1].split("Phigh       :")[0].strip().split()
            for  i in US:
                 Ds_n += int(i)
            if Ds_n != 10:
               if i==3:raise Except("ErrorCode(E00242):4X4 US Lock Check: FAIL") 
            else:break
        except:
            if i==3:raise Except("ErrorCode(E00242):8X4 US Lock Check: FAIL")     
    log("4X4 US Lock Check: PASS (PASS)",2)

def Check24X8UsDsLock(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    ''' 
    term = argv[1][-1]
    log = argv[-4]
    try:
        for k in range(3):
            data = lWaitCmdTerm(term,"dsstatus","Test>",5,2)
            #log(data,2)
            print data
            print data.count('YES')
            # if data.count('YES') == 96:break ################## IRIGINAL
            if data.count('YES') == 32:break  ############11/25 TOAN
            if k == 2:raise Except("ErrorCode(E00242):8 DS Channel Lock Check: FAIL")
            time.sleep(1)             
        log("8 DS Channel Lock Check: PASS (PASS)",2)
        lWaitCmdTerm(term,"exit","tion>",10)
        lWaitCmdTerm(term,"exit","docsis>",8)
        lWaitCmdTerm(term,'Debug',"Debug>",8,2)
        for k in range(3):
            Ds_n = 0
            data = lWaitCmdTerm(term,'usstatus',"Debug>",5,2)
            print data
            US = data.split("Upstream    :")[-1].split("Phigh      :")[0].strip().split()
            print US 
            #for i in US:  ##################         
              #Ds_n += int(i)############## ORIGINAL 
              #print Ds_n ###############
            for i in range (4):  ############# 11/25 TOAN          
              Ds_n += int(US[i])
              print Ds_n  
            #############
            print Ds_n
            #if Ds_n != 36:   ##########ORIGINAL 
            if Ds_n != 10:          ##########11/25 TOAN
               if k==2:raise Except("ErrorCode(E00242):4 US Channel Lock Check: FAIL")
            else:break 
        log("4 US Channel Lock Check: PASS (PASS)",2)
    except:
        raise Except("ErrorCode(E00242):24X8 DS US Lock Check: FAIL") 

     
def CheckRePower(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    pn = argv[-3]('Base','PN')
    mac = argv[2][0]
    #sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    freq_step = argv[-3]('Base','freq_step')
    system_snr = eval(argv[-3]('Base','system_snr'))
    snr_offset = eval(argv[-3]('Base','snr_offset'))
    system_dspower = eval(argv[-3]('Base','system_dspower'))
    dspower_offset = eval(argv[-3]('Base','dspower_offset'))
    system_uspower = eval(argv[-3]('Base','system_uspower'))
    uspower_offset = eval(argv[-3]('Base','uspower_offset'))
    ds_chanel =eval(argv[-3]('Base','ds_chanel'))
    cpkdata={}
    for try_ in range(3): 
        sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
        if len(sn)==12:break
    port =argv[0]+1
    if port > 4 : port -= 4
    dspower=eval('dspower_%s_%s_%s'%(freq_step,sn,port))
    freq_uspower_EU = eval('uspower_%s'%freq_step)
    #DS & MSE Check
    for i in range(ds_chanel):
        result = []
        for try_ in range(3):
            try:
                data = ' '*800  
                message = ''
                while len(data) > 600:
                      data = lWaitCmdTerm(term,"phy %i"%i,"sis>",5,2)
    
                value = abs(float(data.split("MSE:")[-1].split("dB")[0].strip()))
                msg = "Channel %s MSE: %.2f ( > %.2f)\n"%(i+1,value,system_snr)
                if value - system_snr < 0:
                    result.append('MSE')
                print msg
                message += msg
                cpkdata['Channel_%s_MSE'%(i+1)]=(system_snr,system_snr+10,value)
                #DS
                value = float(data.split("Reported power is")[-1].split("dBmv")[0].strip())
                freq = int(str(int(round(float(data.split("RF frequency:")[-1].split("MHz")[0].strip()))))[0:3])
                
                message += "Channel %s CMTS Measure= %.2f\n"%((i+1),dspower[freq])
                message += "Channel %s DSPower = %.2f\n"%((i+1),value)
                #print freq
                value = value - dspower[freq]
                msg = "Channel %s DSpower  Diff: %.2f (%.2f ~ %.2f)"%(i+1,value,system_dspower-dspower_offset,system_dspower+dspower_offset)
                if abs(value - system_dspower) > dspower_offset:
                    result.append('DS')  
                print msg
                message += msg
                cpkdata['Channel_%s_DSpower'%(i+1)]=(system_dspower-dspower_offset,system_dspower+dspower_offset,value)
            except:
                if try_==2:
                   log(message)
                   raise Except("ErrorCode(108005):Get DS/MSE value failed")
                continue
            if result:
               if try_==2:
                  log(message)
                  raise Except("ErrorCode(108005):Get DS/MSE value failed")
            else:
                log(message)
                break   
    log('Check DS/MSE value pass',2)
      
    # US power 
    '''
    lWaitCmdTerm(term,"Debug","ug>",5,2)
    data = lWaitCmdTerm(term,"usstatus","Debug>",5,2)
    print "3333333333333333"
    print data
    print "44444444444444444444"
    us_data = [[0 for j in xrange(3)] for i in xrange(8)]
    for try_ in range(3):
        result=1
        try:
           for i in data.splitlines():
               if 'Frquency' in i:
                   freq = i.split("Frquency    :")[-1].split("Symbol")[0].strip().split()
                   freq = ''.join(freq)
                   freq = freq.split('|'); #print freq
                   print freq
                   print '\n'
               if 'modulation' in i:
                   mod = i.split("modulation  :")[-1].split("SCDMA")[0].strip().split()
                   mod = ''.join(mod)
                   mod = mod.split('|'); #print mod
                   print mod
                   print '\n'
                   print "zzzzzzzzzzzzzzzzzzzzzzzzz"
               if 'rep power  :' in i:
                   #pwr = i.split("rep power   :")[-1].split("rep power1_6")[0].strip().split() #############original
                   pwr = i.split("rep power  :")[-1].split("Upstream")[0].strip().split() ########11/26 toan
                   pwr = ''.join(pwr)
                   pwr = pwr.split('|'); #print pwr
                   print pwr
                   print '\n'
                   print "kkkkkkkkkkkkkkkkkkkkkkkkkkk"
           count = 0
           count_ = 0
           print "ok"
           for j in range(us_chanel):
                #us_data[j][0] = round(float(freq[j]),2)
                us_data[j][0] = int(round(decimal.Decimal(freq[j]),1)*1000000)
                print us_data[j][0]
                print "ssssssssssssssssssssssss"
                us_data[j][1] = mod[j]
                print us_data[j][1]
                print "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
                us_data[j][2] = round(float(pwr[j]),2); #print us_data
                #us_data[j][2] = round(decimal.Decimal(pwr[j]),1)
                print "55555555555555555555555"
                print us_data
                print "666666666666666666666666666666"
                print us_data[j][1]
                print "777777777777777777777777777777"
                if us_data[j][1] != "ERR":
                     count+=1
                     
                     ############################### original#####################
                     #a=int(us_data[j][2]-40) + freq_uspower_NA[j]
                     a=int(us_data[j][2]-40) + freq_uspower_NA[us_data[j][0]] ## viet 0909
                     print a ######################
                     if us_data[j][2] >40 :us_data[j][2]= us_data[j][2]- a
                     if us_data[j][2] <40 :us_data[j][2]= us_data[j][2]-a                                           
                     print '####################'
                     print us_data[j][2]
                     #diff = us_data[j][2] - int(system_uspower) + freq_uspower_EU[j]                 
                     #diff = us_data[j][2] - int(system_uspower) + freq_uspower_NA[j] #### 0909 viet
                     diff = us_data[j][2] - int(system_uspower) + freq_uspower_NA[us_data[j][0]]
                     #msg = "US Freq = %d MHz, Power = %.2f,freq_uspower = %.2f, diff = %.2f(%.2f ~ %.2f)"%(us_data[j][0], us_data[j][2]+freq_uspower_EU[j],freq_uspower_EU[j], diff, uspower_offset*-1,uspower_offset)
                     #msg = "US Freq = %d MHz, DUT_uspower = %.2f,CMTS_uspower = %.2f, diff = %.2f(%.2f ~ %.2f)"%(us_data[j][0], us_data[j][2]+freq_uspower_NA[j], system_uspower, diff, uspower_offset*-1,uspower_offset) # 0909 viet
                     msg = "US Freq = %d MHz, DUT_uspower = %.2f,CMTS_uspower = %.2f, diff = %.2f(%.2f ~ %.2f)"%(us_data[j][0], us_data[j][2]+freq_uspower_NA[us_data[j][0]], system_uspower, diff, uspower_offset*-1,uspower_offset)
                     print msg 
                     
                     #############################################################
                     
                     diff = us_data[j][2] -freq_uspower_NA[us_data[j][0]]
                     msg = "US Freq = %d MHz, DUT_uspower = %.2f,Base Power = %.2f, diff = %.2f(%.2f ~ %.2f)"%(us_data[j][0],us_data[j][2],freq_uspower_NA[us_data[j][0]], diff, uspower_offset*-1,uspower_offset)
                     if  abs(diff) > uspower_offset:
                          count_+=1; result=0
                     argv[-4](msg)          
           if count != us_chanel or count_ > 0: raise Except("US Signal Check FAIL")
           
           #lWaitCmdTerm(term,'exit',"docsis>",5)
           #cpkdata['Channel_1_USPower']=(system_uspower-uspower_offset,system_uspower+uspower_offset,data)
        except:
             if try_==2:
                log(msg)
                raise Except("ErrorCode(107024):Get US Power failed")
             continue
        if not result:
           if try_==2:
              log(msg)
              raise Except("ErrorCode(107024):Check US Power failed")
        else:
           break
    log('Check %d Chanel US repwr pass'%us_chanel,2)    
    if insertcpk:
       if not InsertCPK_DB(mac,pn,'System',cpkdata):
          raise Except("ErrorCode(0005):Insert CPK data to db failed")
    '''
    ###################################
    
    lWaitCmdTerm(term,"Debug","ug>",5,3)
    data = lWaitCmdTerm(term,"usstatus","Debug>",5,3)
    print data
    us_data = [[0 for j in xrange(3)] for i in xrange(8)]
    for try_ in range(3):
        try:
            for i in data.splitlines():
               if 'Frquency' in i:
                   freq = i.split("Frquency   :")[-1].split("Symbol")[0].strip().split()
               if 'modulation' in i:
                   mod = i.split("modulation :")[-1].split("SCDMA")[0].strip().split()
               if 'rep power' in i:
                   pwr = i.split("rep power  :")[-1].split("Upstream")[0].strip().split()
            count = 0
            count_ = 0
            for j in range(8):
                us_data[j][0] = (round(float(freq[j])))
                us_data[j][1] = mod[j]
                us_data[j][2] = round(float(pwr[j]),2)
                if us_data[j][1] <> "ERR":
                     #if us_data[j][0]>15 and us_data[j][0]<40:    ######original
                     # if us_data[j][0]>10 and us_data[j][0]<40:
                     count+=1
                     print us_data[j][2]        
                     #a=int(us_data[j][2]-40)+ freq_uspower_EU[j]                        
                     #if us_data[j][2] >40 or  us_data[j][2] <40:
                     #   us_data[j][2]= us_data[j][2]- a
                                
                     #if us_data[j][2] <40 :us_data[j][2]= us_data[j][2]-a                                                   
                                
                     diff = us_data[j][2] - int(system_uspower) + freq_uspower_EU[j]
                     #msg = "US Freq = %d MHz, Power = %.2f,freq_uspower = %.2f, diff = %.2f(%.2f ~ %.2f)"%(us_data[j][0], us_data[j][2]+freq_uspower_EU[j],freq_uspower_EU[j], diff, uspower_offset*-1,uspower_offset)
                     msg = "US Freq = %d MHz, DUT_uspower = %.2f,CMTS_uspower = %.2f, diff = %.2f(%.2f ~ %.2f)"%(us_data[j][0], us_data[j][2]+freq_uspower_EU[j], system_uspower, diff, uspower_offset*-1,uspower_offset)
                     if  abs(diff) > uspower_offset:
                          count_+=1
                     argv[-4](msg)
            if count < ds_chanel or count_ > 0: raise Except("US Signal Check FAIL")
            #lWaitCmdTerm(term,'exit',"docsis>",5) 
            cpkdata['Channel_1_USPower']=(system_uspower-uspower_offset,system_uspower+uspower_offset,data)
        except:
             if try_==2:
                log(msg)
                raise Except("ErrorCode(107024):Get US Power failed")
             continue
        if result :
           if try_==2:
              log(msg)
              raise Except("ErrorCode(107024):Check US Power failed")
        else:
           break
    if insertcpk:
       if not InsertCPK_DB(mac,pn,'System',cpkdata):
          raise Except("ErrorCode(0005):Insert CPK data to db failed")
          
    #######################################################            
def CheckCWError(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    mac = argv[2][0]
    #sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    cw_error_rate = eval(argv[-3]('Base','cw_error_rate'))
    #CW error rate
    #for i in xrange(0,7,4): 
    for i in xrange(4):
        for c in range(3):
            try:
                lWaitCmdTerm(term,"cerreset %i"%i,"docsis>",5,4)
                time.sleep(1 + c) #by James_Huang 2015/12/04
                data = lWaitCmdTerm(term,"phy %i"%i,"sis>",5,4)      
                value = float(data.split("CW Error Rate:")[-1].split("\n")[0].strip())   #gu
                if value - cw_error_rate <= 0:
                   break
            except ValueError:
                if c==2:raise Except('ErrorCode(E00144):Get CW Error Failed')
        msg = "Channl %d CW Error Rate: %.2e ( < %.2e)"%(i,value,cw_error_rate)
        if value - cw_error_rate > 0:
           raise Except('ErrorCode(E00144):'+msg)
        else:
           log(msg,2)

def CheckCWError_SMCD3GNV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    mac = argv[2][0]
    sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    cw_error_rate = eval(argv[-3]('Base','cw_error_rate'))
    #CW error rate
    for i in xrange(4): 
        for c in range(3):
            try:
                lWaitCmdTerm(term,"cerreset %i"%i,"sis>",5,4)
                data = lWaitCmdTerm(term,"phy %i"%i,"sis>",5,4)      
                value = float(data.split("CW Error Rate:")[-1].split("\n")[0].strip())   #gu
                if value - cw_error_rate <= 0:
                   break
            except ValueError:
                if c==2:raise Except('ErrorCode(E00144):Get CW Error Failed')
        msg = "Channl %d CW Error Rate: %.2e ( < %.2e)"%(i,value,cw_error_rate)
        if value - cw_error_rate > 0:
           raise Except('ErrorCode(E00144):'+msg)
        else:
           log(msg,2)
 
def CheckVen(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    mac = argv[2][0]
    sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    prod_info_dic = eval(argv[-3]('Base','prod_info_dic'))
    ven_info_dic = eval(argv[-3]('Base','ven_info_dic_'))
    menu = argv[-3]('Base','menu')

    data=lWaitCmdTerm(term,"ven","sis>",5,3)
    if 'Error: Command not found.' in data:
       lWaitCmdTerm(term,"top",menu,5)
    for try_ in range(6):
        data = lWaitCmdTerm(term,"ven",">",5,3)
        value=ReleaseInformationCheck(data,ven_info_dic,':')
        if not value:break
    if value:raise Except('ErrorCode(0008):'+value)
    log(data)
    log('Check Vendor information PASS',2) 
    
def InformationCheck(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    mac = argv[2][0]
    #sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    prod_info_dic = eval(argv[-3]('Base','prod_info_dic'))
    ven_info_dic = eval(argv[-3]('Base','ven_info_dic'))
    menu = argv[-3]('Base','menu')
    for try_ in range(3):
        data = lWaitCmdTerm(term,"prodsh","ion>",5)
        #print data
        value=ReleaseInformationCheck(data,prod_info_dic,'- <')
        #print value
        if not value:break
        
    if value:raise Except('ErrorCode(0008):'+value)
    log(data)
    log('Check Product information PASS',2)

    lWaitCmdTerm(term,"exit","docsis>",5)
    data=lWaitCmdTerm(term,"ven","docsis>",5)
    if 'Error: Command not found.' in data:
       lWaitCmdTerm(term,"top",menu,5)
    for try_ in range(3):
        data = lWaitCmdTerm(term,"ven","docsis>",5)
        value=ReleaseInformationCheck(data,ven_info_dic,':')
        if not value:break
    if value:raise Except('ErrorCode(0008):'+value)
    log(data)
    log('Check Vendor information PASS',2)
       
def HtMsoFreqCheck(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    term = argv[1][-1]
    log = argv[-4]
    mso_freq_dic = eval(argv[-3]('Base','mso_freq_dic'))
    for try_ in range(3):
        data = lWaitCmdTerm(term,"HtMSOFreq show","sis>",5)
        value=ReleaseInformationCheck(data,mso_freq_dic,'| Freq is')
        if not value:break
    if value:raise Except('ErrorCode(0009):'+value)
    log(data)
    log('Check HtMSOFreq information PASS',2)   
      
    
def AddHtMsoFreq(term):
    lWaitCmdTerm(term,"htMsoFreq erase","docsis>",6)
    #lWaitCmdTerm(term,ticliHead+"ca/doc/htMsoFreq erase","#",5,3)
    for i in range(len(MsoFre)):
        lWaitCmdTerm(term,"htMsoFreq add %s"%(str(MsoFre[i])+"000"),"docsis>",5,2)
        #lWaitCmdTerm(term,ticliHead+"ca/doc/htMsoFreq add %s"%(str(MsoFre[i])+"000"),"#",5,3)

def InstallMsoGoldenFreq(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    term = argv[1][-1]
    log = argv[-4]
    mso_freq = eval(argv[-3]('Base','mso_freq'))
    lWaitCmdTerm(term,"HtMSOFreq erase","Erase Success",15)
    log("HtMSOFreq erase: OK")
    for i in mso_freq:
        lWaitCmdTerm(term,"HtMSOFreq add %d"%i,"Success",15,2)
    log('Add HtMSOFreq list OK',2)

def CheckMsoGoldenFreq(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    term = argv[1][-1]
    log = argv[-4]
    mso_freq = eval(argv[-3]('Base','mso_freq'))
    for try_ in range(3):
        try:
            data = lWaitCmdTerm(term,"HtMSOFreq show","sis>",15)
            if len(data.splitlines()) > len(mso_freq): break 
        except:
            pass
        if try_ ==2: raise Except('ErrorCode(0009):HtMSOFreq show FAIL ')
        else: continue
    log(data)     
    for i in mso_freq:
        get_val = 0
        for j in data.splitlines(): 
              if "Freq %d"%i in j :                   
                  get_val = 1 
                  break
        if not get_val: raise Except('ErrorCode(0009): Check MSOFreq %d FAIL'%i) 
        
    log('Check HtMSOFreq PASS',2)  

def GetDialogValue(dialog,dutid,msg,check=0):
    dialog.ScanLabel.SetBackgroundColour( "yellow" )
    dialog.DUT.SetLabel('       %s        '%dutid)
    dialog.LabelName.SetLabel(msg)
    while 1:
          dialog.ScanLabel.Refresh()
          while not dialog.Label_:     #wait scan label
                time.sleep(0.5)
          value = dialog.Label_
          dialog.Label_ = ''
          #print len(value),value
          if check :
             if value.upper() not in ('OK','NG'):
                dialog.ScanLabel.SetBackgroundColour( "red" ) 
                continue
             else:
                #print value,len(value)
                return value.upper()
          else:
             try:
                 if len(value) <> 12 or not int(value,16):
                    dialog.ScanLabel.SetBackgroundColour( "red" ) 
                    continue
             except:
                 print value
                 dialog.ScanLabel.SetBackgroundColour( "red" ) 
                 continue       
             return value     
          
'''
def CheckMACandLED(*argv):
    
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
        
    argv[3](checkled)
    CML_Lock.acquire()
    dialog = argv[-1][0][0]
    message = ''
    try:
        while not dialog.IsModal():     #wait scan 'check' label then dialog gui ShowModal
              time.sleep(0.5)
        mac = GetDialogValue(dialog,argv[0]+1,'Scan MAC Address')
        if mac <> argv[2][0]:
           raise Except('ErrorCode(0010):MAC %s (%s) scan error'%(mac,argv[2][0]))
        argv[-4]('MAC %s (%s) comparison of pass'%(mac,argv[2][0]),2)
        dialog.LabelName.SetLabel('MAC %s (%s) comparison of pass'%(mac,argv[2][0]))
        
        #lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5)
        #time.sleep(3)
        if GetDialogValue(dialog,argv[0]+1,'Check Ether 1000F LED',1) <> 'OK':
           raise Except('ErrorCode(402053):Ether 1000F LED Check Faied')
        argv[-4]('Ether 1000F LED Check pass',2)
        dialog.LabelName.SetLabel('Ether 1000F LED Check pass')
        
        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 100F','speed',5)
        #time.sleep(3)
        if GetDialogValue(dialog,argv[0]+1,'Check Ether 100F LED',1) <> 'OK':
           raise Except('ErrorCode(402053):Ether 100F LED Check Faied')
        argv[-4]('Ether 100F LED Check pass',2)
        dialog.LabelName.SetLabel('Ether 100F LED Check pass')
  
        lWaitCmdTerm(argv[1][-1],"mml 0x40000150 0x08610904","st>",5,2) #LED ALL ON, WPS green
        if GetDialogValue(dialog,argv[0]+1,'LED ALL ON, WPS Green',1) <> 'OK':
           raise Except("ErrorCode(402053):LED ALL ON, WPS green : FAIL (PASS)")
        argv[-4]("LED ALL ON, WPS green : PASS (PASS)" ,2)
        dialog.LabelName.SetLabel('LED ALL ON, WPS green : PASS (PASS)')
        lWaitCmdTerm(argv[1][-1],"mml 0x40000130 0x08610904","st>",5)             #LED ALL ON, WPS Red
        if GetDialogValue(dialog,argv[0]+1,'LED ALL ON, WPS Red',1) <> 'OK':
           raise Except("ErrorCode(402053):LED ALL ON, WPS red : FAIL (PASS)")
        argv[-4]("LED ALL ON, WPS Red : PASS (PASS)" ,2) 
        dialog.LabelName.SetLabel('LED ALL ON, WPS Red : PASS (PASS)')
        lWaitCmdTerm(argv[1][-1],"mml 0x4003317f 0x08610904","st>",5) #LED ALL off
        if GetDialogValue(dialog,argv[0]+1,'LED ALL OFF ',1) <> 'OK':
           raise Except("ErrorCode(402053):LED ALL OFF : FAIL (PASS)")
        argv[-4]("LED ALL OFF : PASS (PASS)",2)
        
    except Except,msg:
        message = 'ErrorCode(0000):%s'%msg
    except Exception,e:
        message = 'ErrorCode(0001):%s'%e.message
    dialog.Close()
    if CML_Lock.locked():CML_Lock.release()   
    if message:
       raise Except(message)
'''
def CheckMACandLED(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''     
    argv[3](checkled)
    CML_Lock.acquire()
    message = ''    
    cbterm = argv[1][1]
    port=argv[0]+1
    if port >4 : port -= 4
    #lWaitCmdTerm(cbterm,'rf %s c'%port,'rf',5,5)
    try:
        UDPort = os.popen("netstat -a -p UDP").read()
        while ":1808 " not in UDPort:
              UDPort = os.popen("netstat -a -p UDP").read()
              #argv[1][-1].get()
              #argv[1][-1]<<"wait mac"
              time.sleep(0.2)
              #data=argv[1][-1].get()
              #print data
        #time.sleep(0.5)
        #argv[1][-1]<<"\n"
        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5) 
        time.sleep(1)             
        mac = GetDialogValue(argv[0]+1,'Scan MAC Address')
        if mac[0]=="2":mac=getmac(mac)    
        if mac <> argv[2][0]:
           raise Except('ErrorCode(0010):MAC %s (%s) scan error'%(mac,argv[2][0]))
        argv[-4]('MAC %s (%s) comparison of pass'%(mac,argv[2][0]),2)
                        
        #lWaitCmdTerm(argv[1][-1],"mml 0x40000150 0x08610904","st>",5,3) #LED ALL ON, WPS green
        if GetDialogValue(argv[0]+1,'Check Ether 1000F and ALL ON WPS Red') <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 1000F and ALL ON,WPS Red Faied')
        argv[-4]('Check Ether 1000F and ALL ON,WPS Red pass',2)
        
        #lWaitCmdTerm(argv[1][-1],"mml 0x40000130 0x08610904","st>",5)             #LED ALL ON, WPS Red
        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 100F','speed',5)
        time.sleep(3)
        if GetDialogValue(argv[0]+1,'Check Ether 100F LED ON') <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 100F LED ON Faied')
        argv[-4]('Check Ether 100F LED ON Pass',2)
        #dialog.LabelName.SetLabel('Ether 100F and ALL ON,WPS Red pass')
        
        #time.sleep(0.5) 
        #lWaitCmdTerm(argv[1][-1]," ","st>",5)   
        #lWaitCmdTerm(argv[1][-1],"mml 0x4003317f 0x08610904","st>",5) #LED ALL off
        #if GetDialogValue(argv[0]+1,'LED ALL OFF ') <> 'OK':
           #raise Except("ErrorCode(402053):LED ALL OFF : FAIL (PASS)")
        #argv[-4]("LED ALL OFF : PASS (PASS)",2)
        
    except Except,msg:
        message = 'ErrorCode(0000):%s'%msg
    except Exception,e:
        message = 'ErrorCode(0001):%s'%e.message
    os.popen("taskkill /F /IM Dialog.exe").read()
    for try_ in range(10):
        if "Dialog.exe" not in os.popen("tasklist").read(): break
        time.sleep(0.1)
    if CML_Lock.locked():CML_Lock.release()   
    if message:
       raise Except(message)   
 

def CheckMACandLED_WPS(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''     
    argv[3](checkled)
    CML_Lock.acquire()
    dialog = argv[-1][0][0]
    message = ''
    try:
        while not dialog.IsModal():     #wait scan 'check' label then dialog gui ShowModal
              time.sleep(0.5)
        mac = GetDialogValue(dialog,argv[0]+1,'Scan MAC Address')
        if mac <> argv[2][0]:
           raise Except('ErrorCode(0010):MAC %s (%s) scan error'%(mac,argv[2][0]))
        argv[-4]('MAC %s (%s) comparison of pass'%(mac,argv[2][0]),2)
        dialog.LabelName.SetLabel('MAC %s (%s) comparison of pass'%(mac,argv[2][0]))
        
        #lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5)
        #time.sleep(3)
        argv[-4]('Press WPS Button within 60 sec')
        lWaitCmdTerm(argv[1][-1],'Check WPS Button',"wps_status",3,20)
        argv[-4]('WPS Button test PASS (PASS)',2)
        
        lWaitCmdTerm(argv[1][-1],"mml 0x40000150 0x08610904","st>",5,3) #LED ALL ON, WPS green
        if GetDialogValue(dialog,argv[0]+1,'Check Ether 1000F and ALL ON,WPS Green',1) <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 1000F and ALL ON,WPS Green Faied')
        argv[-4]('Check Ether 1000F and ALL ON,WPS Green pass',2)
        dialog.LabelName.SetLabel('Ether 1000F ALL ON,WPS Green pass')
        
        lWaitCmdTerm(argv[1][-1],"mml 0x40000130 0x08610904","st>",5)             #LED ALL ON, WPS Red
        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 100F','speed',5)
        #time.sleep(3)
        if GetDialogValue(dialog,argv[0]+1,'Check Ether 100F and ALL ON,WPS Red',1) <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 100F and ALL ON,WPS Red Faied')
        argv[-4]('Check Ether 100F and ALL ON,WPS Red pass',2)
        dialog.LabelName.SetLabel('Ether 100F and ALL ON,WPS Red pass')
  
        #lWaitCmdTerm(argv[1][-1],"mml 0x40000150 0x08610904","st>",5,2) #LED ALL ON, WPS green
        #if GetDialogValue(dialog,argv[0]+1,'LED ALL ON, WPS Green',1) <> 'OK':
        #   raise Except("ErrorCode(402053):LED ALL ON, WPS green : FAIL (PASS)")
        #argv[-4]("LED ALL ON, WPS green : PASS (PASS)" ,2)
        #dialog.LabelName.SetLabel('LED ALL ON, WPS green : PASS (PASS)')
        #lWaitCmdTerm(argv[1][-1],"mml 0x40000130 0x08610904","st>",5)             #LED ALL ON, WPS Red
        #if GetDialogValue(dialog,argv[0]+1,'LED ALL ON, WPS Red',1) <> 'OK':
        #   raise Except("ErrorCode(402053):LED ALL ON, WPS red : FAIL (PASS)")
        #argv[-4]("LED ALL ON, WPS Red : PASS (PASS)" ,2) 
        #dialog.LabelName.SetLabel('LED ALL ON, WPS Red : PASS (PASS)')
        lWaitCmdTerm(argv[1][-1],"mml 0x4003317f 0x08610904","st>",5) #LED ALL off
        if GetDialogValue(dialog,argv[0]+1,'LED ALL OFF ',1) <> 'OK':
           raise Except("ErrorCode(402053):LED ALL OFF : FAIL (PASS)")
        argv[-4]("LED ALL OFF : PASS (PASS)",2)
        
    except Except,msg:
        message = 'ErrorCode(0000):%s'%msg
    except Exception,e:
        message = 'ErrorCode(0001):%s'%e.message
    dialog.Close()
    if CML_Lock.locked():CML_Lock.release()   
    if message:
       raise Except(message)
   
def ResetCleanall(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4

    lWaitCmdTerm(term,"reset cleanall","(Y or N)",10)
    time.sleep(0.2)
    data = lWaitCmdTerm(term,"y","",8) 
    time.sleep(5)
    #wait dut ether Down
    for p in range(30):
        time.sleep(1)
        data = lWaitCmdTerm(argv[1][2],'ping 1 192.168.100.1 -n 1','ping',8,2)
        if '100%' in data:
           log('Factory reset PASS',2)
           break             
        if p==29 :raise Except('ErrorCode(E00155):Factory reset failed')

    #log("==============================================",2)
    #log(data[-500:],2)
    #log("==============================================",2)    
    #lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    #log('Factory reset PASS',2)

def ResetCleanall_telnet(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4

    data=lWaitCmdTerm(argv[1][-1],"factoryReset","docsis>",20)        
    print data  
    log(data,2)
    for p in range(6):
        time.sleep(2)
        data = lWaitCmdTerm(argv[1][2],'ping 1 192.168.100.1 -n 1','ping',8,2)
        if '100%' in data:break             
        if p==5 :raise Except('Fail:After reset cleanall not ping')     
    time.sleep(40)
    log('Factory reset PASS',2)

def Check4X4UsDsLock(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    ''' 
    term = argv[1][-1]
    log = argv[-4]
    try:
       for k in range(3):
           data = lWaitCmdTerm(term,"dsstatus","Test>",5)
           print data
           print data.count('YES')
           if data.count('YES') == 36:break
           if k == 2:raise Except("ErrorCode(E00242):4X4 DS Lock Check: FAIL")
           time.sleep(1)             
       log("4X4 DS Lock Check: PASS (PASS)",2)
       lWaitCmdTerm(term,"exit","Production>",10)
       lWaitCmdTerm(term,"exit","docsis>",5)
       lWaitCmdTerm(term,'Debug',"Debug>",5)
       for k in range(3):
           Ds_n = 0
           data = lWaitCmdTerm(term,'usstatus',"Debug>",5)
           print data
           US = data.split("Upstream    :")[-1].split("Phigh")[0].strip().split("           ")
           for i in US:
             Ds_n += int(i)
           if Ds_n != 10:
              if k==2:raise Except("ErrorCode(E00242):4X4 US Lock Check: FAIL")
           else:break 
       log("4X4 US Lock Check: PASS (PASS)",2)
    except:
        raise Except("ErrorCode(E00242):4X4 DS Lock Check: FAIL")         

def FactoryReset_SMCD3GNV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    mac = argv[2][0]
    port=argv[0]+1
    if port >4 : port -= 4
    log('Fcy-Reset&WlsSecurity check...')
    lWaitCmdTerm(term,"top",">",5,3)
    lWaitCmdTerm(term,"rg",">",5,3)
    lWaitCmdTerm(term,"reset cleanall","(Y or N)",5,3)
    lWaitCmdTerm(term,"y","F-RESET",20)
    lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5,3)
    lWaitCmdTerm(argv[1][1],'rf %s n'%(c_port+1),'OK',5)
    time.sleep(40)
    lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5,3)
    lWaitCmdTerm(argv[1][-1],"Wait Reboot","#",5,10)
    log('Factory reset OK',2)
    
    
def CheckWlsSec(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    mac = argv[2][0]
    ssid='HOME-%04X'%(int(mac[-4:],16)+8)
    lWaitCmdTerm(term,"cli","RootMenu>",8)
    lWaitCmdTerm(term,"rg",">",5)
    for k in range(5):
        data=lWaitCmdTerm(term,"script","Main>",5,2)
        if ("wireless_authentication 1 WPAPSK" in data and "wireless_encrypt 1 TKIP" not in data and ssid not in data and wpakey not in data):
            break
        else:
            if k == 5:    
               raise Except("WlsSecurity Check Fali")
    log("WlsSecurity Check PASS")   
                  
def ResetCleanall_CCR(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
     Model:SMCD3G-CCR
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
    lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    lWaitCmdTerm(term,"reset cleanall","Are you sure you want to reset to factory defaults? (Y or N)",10)
    time.sleep(0.2)
    lWaitCmdTerm(term,"y","Compressed file is LZMA format",40) 
    data = lWaitCmdTerm(term,"waitdutboot","Press SPACE to abort autoboot",80) #waitting second reboot 
    #data = lWaitCmdTerm(term,"","Compressed file is LZMA format",40) 
    log("==============================================",2)
    log(data[-500:],2)
    log("==============================================",2)
    #lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    log('Factory reset PASS',2)
    
def ResetCleanallTelnet_CCR(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
     Model:SMCD3G-CCR
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
    lWaitCmdTerm(term,"reset cleanall","Are you sure you want to reset to factory defaults? (Y or N)",5)
    time.sleep(0.2)
    lWaitCmdTerm(term,"y","F-RESET",10) 
    lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    time.sleep(20)
    log('Factory reset PASS',2)    
    
################20121130 cve30360 mx ###################
def CheckWiFiChipVersionAndE2p(*argv): 
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
     Model:CVE30360-MX
    '''
    WIFI_Device_Ver = argv[-3]('Base','WIFI_Device_Ver')
    WIFI_E2P_Val = argv[-3]('Base','WIFI_E2P_Val')
    term = argv[1][-1]
    term.get()
    term << 'iwpriv ra0 show driverinfo'
    data = term.wait('Driver version',5)[-1]
    term <<''
    data += term.wait('#',5)[-1]
    print data   
    drive_ver=data.split('Driver version:')[-1].strip().split()[0]
    print drive_ver
    e2p_val = lWaitCmdTerm(term,"iwpriv ra0 e2p 03",'#',5).split('[0x0003]:')[-1].strip().split()[0]
    print e2p_val
    if WIFI_Device_Ver <> drive_ver:
       raise Except("Wrong WiFi chip version %s(%s)!"%(drive_ver,WIFI_Device_Ver))
    argv[-4]('WiFi version checked pass %s(%s)'%(drive_ver,WIFI_Device_Ver),2)
    if WIFI_E2P_Val <> e2p_val:
       raise Except("Check e2p 03 error %s(%s)"%(e2p_val,WIFI_E2P_Val)) 
    argv[-4]('Check e2p 03 pass %s(%s)'%(e2p_val,WIFI_E2P_Val),2)

def PowerButton(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    c_port = argv[0]
    #argv[3](powerbutton)
    if argv[0] > 3 : c_port = argv[0] - 4  
    lWaitCmdTerm(argv[1][-1],'setstartup -e',"#",5)  
    argv[3](powerbutton)    
    lWaitCmdTerm(argv[1][-1],'ErrorCode(E00249):Power Button Falied','to abort autoboot ',60)
    argv[3]('start')
    lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5)
    time.sleep(40)
    lWaitCmdTerm(argv[1][1],'rf %s c'%(c_port+1),'OK',5)
    lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5)
    #lWaitCmdTerm(argv[1][-1],"Wait Reboot","*********RG INIT start start SUCCESS!*********",60)
    lWaitCmdTerm(argv[1][-1],"Wait Reboot","#",5,10)
    argv[-4]('Power Button test pass',2)   
    
   
def ResetCleanall_Y(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
    log('Factory reset .....',2)
    lWaitCmdTerm(term,"reset cleanall","Are you sure you want to reset to factory defaults? (Y or N)",10)
    print "Factory reset ....."
    lWaitCmdTerm(term,"y","F-RESET",10)
    term.wait("Compressed file is LZMA format.",40)

    time.sleep(6)
    term.get()
    term << ""  
    data = lWaitCmdTerm(term,"factory default","debug: 0 0",20)    
    print data
    time.sleep(5)
    if "debug: 0 0" in data:
        for i in range(3):
            data = lWaitCmdTerm(term,"","",2,10)
            print data     
            if '#' in data:
                raise Except('Factory reset fail')
            else:
                pass      
    else:
        raise Except('Factory reset fail')
          
    lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    log('Factory reset PASS',2)

    
    
    

def checke2p35(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
     Model:CDE-30364R2
    '''
    term = argv[1][-1]
    for try_ in range(2):
        data=lWaitCmdTerm(term,"iwpriv ra0 e2p 35","#",5)
        print data   
        if '0x240C' not in data:
           if try_==1:raise Except('Check %s e2p 35 = %s (0x240C)'%(count,data))
        else:break   
    argv[-4]('Check the temperature-compensation & e2p35 success.',2)
         
def CheckTemperatureCompensation(*argv): 
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
     Model:CVE30360-MX
    '''
    term = argv[1][-1]
    checke2p35(term,0)
    lWaitCmdTerm(term,"iwpriv ra0 e2p 36=0024","#",5)
    time.sleep(1)
    for i in range(3):
        data = lWaitCmdTerm(term,"iwpriv ra0 e2p 36","#",5)
        print data        
        if not '0x0024' in data:
           if i==2:raise Except ("Disable the temperature-compensation Fail!")
        else:break   
    checke2p35(term,1)   
    argv[-4]('Disable the temperature-compensation success.',2)
    
def ResetCleanall_R2(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
    lWaitCmdTerm(term,"reset cleanall","Set default Frequency Plan: Hybrid",5)
    term.wait("Compressed file is LZMA format",40)
    lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    log('Factory reset PASS',2)

def factoryReset(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
    lWaitCmdTerm(term,"factoryReset","Set default Frequency Plan: Hybrid",5)
    time.sleep(20)
    lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    log('Factory reset PASS',2)
   
##########################################WiFi TEST###################################  
def WiFiTeststart(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    wifi_target = argv[-3]('Base','wifi_target').strip()
    menu = argv[-3]('Base','menu').strip()
    wpakey = argv[-3]('Base','wpakey').strip()
    packetsize = eval(argv[-3]('Base','packetsize').strip())
    ping_loss = eval(argv[-3]('Base','ping_loss').strip())
    id = argv[0]
    log = argv[-4]
    
    ssid='%s'%(mac[6:12])
    print 'ssid:' + ssid
    #if mac[-4:]=='0D90':
       #ssid='HOME-%06X'%(int(mac[-6:],16)+8)
    #else:ssid='HOME-%04X'%(int(mac[-4:],16)+8)
    SetWIFISSID(term,mac,menu,ssid,log)
    argv[-1][0][-1]=WIFIThread(id,ssid,wpakey,wifi_target,packetsize,ping_loss,log)
    argv[-1][0][-1].start()

def WiFiTeststart_SMCD3GNV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    mac = argv[2][0]
    term = argv[1][-1]
    wifi_target = argv[-3]('Base','wifi_target').strip()
    menu = argv[-3]('Base','menu').strip()
    wpakey = argv[-3]('Base','wpakey').strip()
    packetsize = eval(argv[-3]('Base','packetsize').strip())
    ping_loss = eval(argv[-3]('Base','ping_loss').strip())
    id = argv[0]
    log = argv[-4]
    
    ssid='HOME-%04X'%(int(mac[-4:],16)+8)
    #ssid='%s'%(mac[6:12])
    #print 'ssid:' + ssid
    #if mac[-4:]=='0D90':
       #ssid='HOME-%06X'%(int(mac[-6:],16)+8)
    #else:ssid='HOME-%04X'%(int(mac[-4:],16)+8)
    SetWIFISSID_SMCD3GNV(term,mac,menu,ssid,log)
    argv[-1][0][-1]=WIFIThread(id,ssid,wpakey,wifi_target,packetsize,ping_loss,log)
    argv[-1][0][-1].start()
    
def SetWIFISSID(term,mac,menu,ssid,log): 
    lWaitCmdTerm(term,"","#",5,2)    
    lWaitCmdTerm(term,"ifconfig ra0 up","#",5,2)
    data=lWaitCmdTerm(term,"ifconfig |grep 'ra0'","#",5,2) #wait ra0 up
    if 'ra0' not in data:raise Except('ra0 not running')
    lWaitCmdTerm(term,"cli",menu,5,5)
    lWaitCmdTerm(term,"wireless_network 1 true %s"%ssid,"The RG script has been changed",8,2)
    lWaitCmdTerm(term,"wireless_security 1 none","The RG script has been changed",8,2)
    lWaitCmdTerm(term,"commit","OK",25,2) 
    #lWaitCmdTerm(term,"rg",">",5,3)
    #lWaitCmdTerm(term,"toggle","MAIN>",5,2) 
    #toggleMain(term,'MAIN>')
    #for i in range(3):
        #lWaitCmdTerm(term,"WlsSecurity 1 open none","success",5,3) #clear wpakey
    #toggleMain(term,'Main>')
    #lWaitCmdTerm(term,"quit","#",5,2) 
    #for i in range(3):
        #lWaitCmdTerm(term,"iwpriv ra0 set SSID=%s"%ssid,"#",5,2) #set ssid
    log('Set WIFI SSID: %s'%(ssid),2)

def SetWIFISSID_SMCD3GNV(term,mac,menu,ssid,log):
    lWaitCmdTerm(term,"quit","#",5,2) 
    lWaitCmdTerm(term,"ifconfig ra0 up","#",5,2)
    data=lWaitCmdTerm(term,"ifconfig |grep 'ra0'","#",5,2) #wait ra0 up
    if 'ra0' not in data:raise Except('ra0 not running')
    lWaitCmdTerm(term,"cli",menu,5,5)
    lWaitCmdTerm(term,"RG","in>",5,3)
    lWaitCmdTerm(term,"toggle","IN>",5,3)
    #toggleMain(term,'MAIN>')
    for i in range(3):
        lWaitCmdTerm(term,"WlsSecurity 1 open none","success",5,3) #clear wpakey
    lWaitCmdTerm(term,"toggle","in>",5,3)
    lWaitCmdTerm(term,"quit","#",5,2) 
    print 'ssid:' + ssid
    for i in range(3):
        lWaitCmdTerm(term,"iwpriv ra0 set SSID=%s"%ssid,"#",5,2) #set ssid
    log('Set WIFI SSID: %s'%ssid)
    
def WiFiPingTest(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    ping_loss = argv[-3]('Base','ping_loss').strip()
    log = argv[-4]
    
    log('Wait WIFI Ping Test',2)
    while argv[-1][0][-1].running:time.sleep(1)
    print 'WIFI Ping test : %s ( < %s)'%(argv[-1][0][-1].msg[1],ping_loss)
    if argv[-1][0][-1].msg[0]:raise Except(argv[-1][0][-1].msg[1])
    log('WIFI Ping test : %s ( < %s)'%(argv[-1][0][-1].msg[1],ping_loss),)
    
def toggleMain(term,menu):
    for try_ in range(3):
        term.get()
        term << 'toggle'
        if menu in term.wait('>',5)[-1]:
           term.get()
           term <<''
           if menu in term.wait('>',5)[-1]:break   
 
##################################ADD Telnet TEST################################
def isPortConnect(ip,port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result=1
    try:
        s.connect((ip,int(port)))
    except Exception:
        result = 0
    s.close() 
    return result

###############################2013-04-10-SMCD3GNV##########################
def Cf_E2P_0x39(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    menu = argv[-3]('Base','Menu').strip()
    log = argv[-4]
    c_port = argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4    
    type=lWaitCmdTerm(term,"iwpriv ra0 e2p 00","~ #",5)#read 0x00
    type=type.split("0x")[-1].split("~ #")[0].strip()
    print "Read iNIC Type:%s"%type
    if 'Invalid command' in type:raise Except("WIFI E2PROM Check Fail.")
    if "3662" in type:
        target="3E"
    else:
        target="39"
    print "Read 0x%s from EEPROM."%target
    data=lWaitCmdTerm(term,"iwpriv ra0 e2p %s"%target,"#",5)#read 0x39  or 0x3E
    print data
    if "[0x00%s]"%target in data:
        values=data.split("[0x00%s]"%target)[-1].strip().split("0x")[-1].strip()
        value2=values[2:]
        value1=values[:2]
        if not "FF" in value2:
            new_value=value1 + "FF"
            lWaitCmdTerm(term,"iwpriv ra0 e2p %s=%s"%(target,new_value),"#",5)
            data=lWaitCmdTerm(term,"iwpriv ra0 e2p %s"%target,"#",5)#read 0x39 or 0x3E
            print data
            if  new_value in data:
                log('E2PROM 0x%s Check Pass'%target)
            else:
                raise Except("E2PROM 0x%s Check Fail."%target)
        else:
            log('E2PROM 0x%s value : %s'%(target,value2))

def beamfoaminigCK(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    log = argv[-4]
    
    data = lWaitCmdTerm(term,"iwpriv ra0 e2p 1a0","~ #",5,3)
    print data
    data = data.split("[0x01A0]:")[1].split("~ #")[0].strip()
    count_flag = 0
    while (len(data)!=6 or "0x" not in data) and count_flag < 5:
          data = lWaitCmdTerm(term,"iwpriv ra0 e2p 1a0","#",5,3)
          print data
          time.sleep(3)
          data = data.split("[0x01A0]:")[1].split("~ #")[0].strip()
          count_flag  = count_flag + 1
    if data == "0xffff" or data == "0xFFFF" :
       raise Except ("beam foaming check  Fail!")
    log('beam foaming check %s success.'%data)

def LedSwitch(term,sy):
    lWaitCmdTerm(term,"cli","RootMenu>",10,2)
    lWaitCmdTerm(term,"cable","cable>",5)
    lWaitCmdTerm(term,"doc","docsis>",5)
    lWaitCmdTerm(term,"Prod",":",5)
    lWaitCmdTerm(term,"stProd2new","Production>",5)
    lWaitCmdTerm(term,"Test","Test>",5)
    if sy:state='mml 0x40000150 0x08610904'
    else:state='mml 0x4003317f 0x08610904' #LED OFF
    for i in range(2):
        lWaitCmdTerm(term,state,">",5)
    lWaitCmdTerm(term,"quit","#",5)

def inPorduction(term):
    for try_ in range(3):
        term.get()
        term << 'prod'
        term.wait(':',3)
        term << 'stProd2new'
        if 'Production>' in term.wait('>',5)[-1]:
           break

def InformationCheck_SMCD3GNV(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''   
    mac = argv[2][0]
    sn =  argv[2][1]
    term = argv[1][-1]
    log = argv[-4]
    prod_info_dic = eval(argv[-3]('Base','prod_info_dic'))
    ven_info_dic = eval(argv[-3]('Base','ven_info_dic'))
    menu = argv[-3]('Base','menu')
    for try_ in range(3):
        data = lWaitCmdTerm(term,"prodsh","ion>",5)
        #print data
        value=ReleaseInformationCheck(data,prod_info_dic,'-')
        #print value
        if not value:break
        
    if value:raise Except('ErrorCode(0008):'+value)
    log(data)
    log('Check Product information PASS',2)
    
    lWaitCmdTerm(term,"top","nu>",5)
    lWaitCmdTerm(term,"rg","Main>",5)
    data=lWaitCmdTerm(term,"ven","Main>",5)
    if 'Error: Command not found.' in data:
       lWaitCmdTerm(term,"top",menu,5)
    for try_ in range(3):
        data = lWaitCmdTerm(term,"ven",">",5)
        value=ReleaseInformationCheck(data,ven_info_dic,':')
        if not value:break
    if value:raise Except('ErrorCode(0008):'+value)
    log(data)
    log('Check Vendor information PASS',2)

def WPSButton(*argv): 
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
     Model:CVE30360-MX
    '''
    timeout = eval(argv[-3](argv[-2],'timeout'))
    WPSButton = argv[-3]('Base','WPSButton').strip()
    term = argv[1][-1]
    argv[3](wpsbutton)
    etime=time.time()+timeout
    while time.time()<= etime:
        data = lWaitCmdTerm(argv[1][-1],'WPS Button','#',5) 
        print data
        if WPSButton in data:
           argv[-4]('WPS Button Test Pass',2)    
           return
    raise Except('ErrorCode(00138):WPS Button Falied')          


############################# CGN3-ROG 2013/ 07 /01 #############################

def CloseJournal(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    menu = argv[-3]('Base','Menu').strip()
    term = argv[1][-1]
    
    lWaitCmdTerm(term,'quit','#',6,10)
    lWaitCmdTerm(term,'cli',menu,8,10)
    lWaitCmdTerm(term,'logger','logger>',6,10)
    lWaitCmdTerm(term,'disable','logger>',6,10)
    lWaitCmdTerm(term,'AllComponentsConfig 0','logger>',6,10)
    lWaitCmdTerm(term,'quit','#',6,10)

def LockDSCheck(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    CMTS_freq = argv[-3]('Base','CMTS_freq').strip()
    freq_step = argv[-3]('Base','freq_step').strip()
    lock_ch = argv[-3]('Base','lock_ch').strip()
    CMTS_DS_ch = argv[-3]('Base','CMTS_DS_ch').strip()
    log = argv[-4]
    term = argv[1][-1]
    
    dsfreqlist=[]
    for k in range(8):
        for i in range(4):
            dsfreqlist.append(int(CMTS_freq) + int(freq_step) * i ) 
    for k in range(5):
        for i in range(int(CMTS_DS_ch),int(lock_ch)):
            lWaitCmdTerm(term,"lockRec %s %s"%(i,dsfreqlist[i]),"Tuner>",10,3)
        time.sleep(3)    
        lWaitCmdTerm(term,"exit","Test>",8)
        lWaitCmdTerm(term,"exit","Production>",8)
        lWaitCmdTerm(term,'exit',"docsis>",8)
        lWaitCmdTerm(term,"Debug","Debug>",5,3)
        data = lWaitCmdTerm(term,"dsstatus","Debug>",5,3)
        #log(data,2)
        print data
        if data.count("YES") == 4*int(lock_ch):
            log("Lock %s Channels PASS (PASS)"%lock_ch)
            break
        else:
            if k == 4:
               raise Except("DS %s channel Lock FAIL"%lock_ch)
            lWaitCmdTerm(term,'exit',"docsis>",8)
            lWaitCmdTerm(term,"Production","Production>",5,2)
            lWaitCmdTerm(term,"Test","Test>",5,2)
            lWaitCmdTerm(term,"Tuner","Tuner>",5,2)
    #lWaitCmdTerm(term,"exit","docsis>",5)


def CountWiFiKey(term,sn):
    data = sn[7:]
    wifikey = hex(int(data,16)^int('DEADF',16))
    wifikey = wifikey[2:].upper() + 'Rogers'
    print 'count wifikey: %s'%wifikey
    if len(wifikey) <> 11:
        return 0
    return wifikey     
    
def CountWiFiKey_ROG(term,sn):
    data = sn[7:]
    wifikey = hex(int(data,16)^int('DEADF',16))
    wifikey = wifikey[2:].upper() + 'Rogers'
    print 'count wifikey: %s'%wifikey
    if len(wifikey) <> 11:
        return 0
    return wifikey   


def GetWpaKeyandInsert_CGN3(*argv):#key_dic,mode '0:send keys to each DB(SQL+ORACLE)|1:just send to ORACLE(MES)'
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())    
    key_dic = {'SSID_PASSWORD':'','NETWORK_KEY':'','WPS_PIN':'','FON_KEY':''}
    mac = argv[2][0]
    sn =  argv[2][1]
    term = argv[1][-1]
    wifikey_ = GetWpaKeyandInsert(term,sn)
    
    key_dic['NETWORK_KEY'] = wifikey_
    key_dic['WPS_PIN'] = wifikey_
    #key_dic['SSID_PASSWORD'] = wifikey_
    log = argv[-4]
    if insert :Insert_WiFiKEY(mac,key_dic,log)
 
def GetWpaKeyandInsert_RES(*argv):#key_dic,mode '0:send keys to each DB(SQL+ORACLE)|1:just send to ORACLE(MES)'
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())    
    key_dic = {'SSID_PASSWORD':'','NETWORK_KEY':'','WPS_PIN':'','FON_KEY':''}
    mac = argv[2][0]
    sn =  argv[2][1]
    term = argv[1][-1]
    wifikey_ = sn
    key_dic['NETWORK_KEY'] = wifikey_
    key_dic['WPS_PIN'] = wifikey_
    #key_dic['SSID_PASSWORD'] = wifikey_
    log = argv[-4]
    
    if insert :Insert_WiFiKEY(mac,key_dic,log)    
    
def GetWiFiKEY_CGN3(mac):
    db = odbc.odbc("TESTlog/TEST/test")
    SQL = db.cursor()
    SQL.execute("SELECT NetworkKey FROM SSIDkey WHERE MAC = '%s' ORDER BY [Time] DESC"%mac)  #wifiKey path is different
    data = SQL.fetchone()[0]
    return data 

def CheckGetWpaKey_ROG(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insert = int(argv[-3](argv[-2],'Insert').strip())
    mac = argv[2][0]
    log = argv[-4]
    term = argv[1][-1]
    for try_ in range(3):
        #lWaitCmdTerm(term,'script',"Main>",5,2)
        data = lWaitCmdTerm(term,'script mshow14',"Main>",5,2)
        wifikey_back = data.split("wls_ssid_wpa_psk 1 ")[-1].split("wls_ssid_access_mode 1")[0].strip()
        print wifikey_back
        if wifikey_back==GetWiFiKEY_CGN3(mac):break 
        if try_==2:raise Except("check wpakey %s digit fail"%wifikey_back)
    log('Check wpakey %s digit OK!'%wifikey_back)   
        
def CheckMACandLED_CGN3(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''     
    argv[3](checkled)
    CML_Lock.acquire()
    dialog = argv[-1][0][0]
    message = ''
    try:
        while not dialog.IsModal():     #wait scan 'check' label then dialog gui ShowModal
              time.sleep(0.5)
        mac = GetDialogValue(dialog,argv[0]+1,'Scan MAC Address')
        if mac <> argv[2][0]:
           raise Except('ErrorCode(0010):MAC %s (%s) scan error'%(mac,argv[2][0]))
        argv[-4]('MAC %s (%s) comparison of pass'%(mac,argv[2][0]),2)
        dialog.LabelName.SetLabel('MAC %s (%s) comparison of pass'%(mac,argv[2][0]))
        
        #lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5)
        #time.sleep(3)

        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5) 
        time.sleep(1)             
        lWaitCmdTerm(argv[1][-1],"echo 0x1 > /proc/hitron/led_mode","#",5,3) #LED ALL ON
        if GetDialogValue(dialog,argv[0]+1,'Check Ether 1000F and ALL ON',1) <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 1000F and ALL ON Faied')
        argv[-4]('Check Ether 1000F and ALL ON pass',2)
        dialog.LabelName.SetLabel('Ether 1000F ALL ON pass')
        
        lWaitCmdTerm(argv[1][-1],"echo 0x3 > /proc/hitron/led_mode","#",5,2)             #LED ALL Twinkling
        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 100F','speed',5)
        time.sleep(1)
        if GetDialogValue(dialog,argv[0]+1,'Check Ether 100F and LED ALL Twinkling',1) <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 100F and ALL Twinkling Faied')
        argv[-4]('Check Ether 100F and ALL Twinkling pass',2)
        dialog.LabelName.SetLabel('Ether 100F and ALL Twinkling pass')
  
        lWaitCmdTerm(argv[1][-1],"echo 0x2 > /proc/hitron/led_mode","#",5) #LED ALL off
        if GetDialogValue(dialog,argv[0]+1,'LED ALL OFF ',1) <> 'OK':
           raise Except("ErrorCode(402053):LED ALL OFF : FAIL (PASS)")
        argv[-4]("LED ALL OFF : PASS (PASS)",2)
        
    except Except,msg:
        message = 'ErrorCode(0000):%s'%msg
    except Exception,e:
        message = 'ErrorCode(0001):%s'%e.message
    dialog.Close()
    if CML_Lock.locked():CML_Lock.release()   
    if message:
       raise Except(message) 
       

def CheckMACandLED_CGNV4_20170905(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''     
    argv[3](checkled)
    CML_Lock.acquire()
    message = ''
    try:
        UDPort = os.popen("netstat -a -p UDP").read()
        while ":1808 " not in UDPort:
              UDPort = os.popen("netstat -a -p UDP").read()
              time.sleep(0.1)
        #time.sleep(0.5)   
        
        mac = argv[2][1]  #MAC = SN 
        while 1:        
            mac = GetDialogValue(argv[0]+1,'Scan MAC Address') 
            if mac <> argv[2][1]:                
                break
            else:
                time.sleep(1)  
                
        time.sleep(0.5)        
                   
        #mac = GetDialogValue(argv[0]+1,'Scan MAC Address')
        if mac <> argv[2][0]:
           raise Except('ErrorCode(0010):MAC %s (%s) scan error'%(mac,argv[2][0]))
        argv[-4]('MAC %s (%s) comparison of pass'%(mac,argv[2][0]),2)

        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5) 
        time.sleep(1)           

        #lWaitCmdTerm(argv[1][-1],"killall ledd pcd","#",8,2)        
        #for i in range(1,7,1):
        #    time.sleep(0.5)   
        #    lWaitCmdTerm(argv[1][-1],"ledd -m %d 1"%i,"#",10,2) #LED ALL ON
        if GetDialogValue(argv[0]+1,'Check Ether 1000F and ALL ON') <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 1000F and ALL ON Faied')
        argv[-4]('Check Ether 1000F and ALL ON pass',2)
        #dialog.LabelName.SetLabel('Ether 1000F ALL ON pass')
        
        #for i in range(1,7,1):
        #    time.sleep(0.5)   
        #    lWaitCmdTerm(argv[1][-1],"ledd -m %d 3"%i,"#",10,2) ##LED ALL Twinkling
        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 100F','speed',5)
        time.sleep(1)
        if GetDialogValue(argv[0]+1,'Check Ether 100F ') <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 100F Faied')
        argv[-4]('Check Ether 100F pass',2)
        #dialog.LabelName.SetLabel('Ether 100F pass')
  
        #for i in range(1,7,1):
        #    time.sleep(0.5)   
        #   lWaitCmdTerm(argv[1][-1],"ledd -m %d 0"%i,"#",10,2) ##LED ALL off

        #if GetDialogValue(dialog,argv[0]+1,'LED ALL OFF ',1) <> 'OK':
        #   raise Except("ErrorCode(402053):LED ALL OFF : FAIL (PASS)")      
        #argv[-4]("LED ALL OFF : PASS (PASS)",2) 
        
    except Except,msg:
        message = 'ErrorCode(0000):%s'%msg
    except Exception,e:
        message = 'ErrorCode(0001):%s'%e.message
    os.popen("taskkill /F /IM Dialog.exe").read()
    for try_ in range(10):
        if "Dialog.exe" not in os.popen("tasklist").read(): break
        time.sleep(0.1)
    if CML_Lock.locked():CML_Lock.release()   
    if message:
       raise Except(message)    

def getmac(mac):
    ServerIP = '127.0.0.1'
    ServerPort = 1800
    timeout = 30
    sn = ""
    MesSocket=htx.UDPService(ServerIP,int(ServerPort),int(timeout))
    MesSocket.set('2,' + mac)  
    Result=MesSocket.get()
    print Result
    Result=Result.strip()
    if Result:
       if len(Result)<>12 or Result[0] == '2':
          raise Except("ErrorCode(0005):Get MAC Failed:%s"%Result)
       else:
          sn = Result
          return sn
    raise Except("ErrorCode(0005):Connection MES Server Fail ")

def CheckMACandLED_CGNV4_back(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''     
    argv[3](checkled)
    mac = argv[2][0]
    #sn = argv[2][1]
    password_ = argv[-3]('Base','shell_password').strip()
    #sn = GetSN(mac)
    CML_Lock.acquire()
    message = ''
    cbterm = argv[1][1]
    port=argv[0]+1
    if port >4 : port -= 4
    lWaitCmdTerm(cbterm,'rf %s c'%port,'rf',5,5)
    lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5,2)
    lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2) 
    time.sleep(2)             
    
    lWaitCmdTerm(argv[1][-1],"shell","Password:",5,3)
    argv[1][-1].get()
    argv[1][-1]<<"%s"%password_
    time.sleep(2)
    data=argv[1][-1].get()
    if "Wrong password!" in data:
        lWaitCmdTerm(argv[1][-1],"shell","Password:",5,3)
        lWaitCmdTerm(argv[1][-1],"AccessDeny","#",5,3)

    #lWaitCmdTerm(argv[1][-1],"%s"%password_,"#",5,3)

    try:
        UDPort = os.popen("netstat -a -p UDP").read()
        while ":1808 " not in UDPort:
              UDPort = os.popen("netstat -a -p UDP").read()
              time.sleep(0.1)

        mac = GetDialogValue(argv[0]+1,'Scan MAC Address')
        if mac[0]=="2":mac=getmac(mac)
        if mac <> argv[2][0]:
           raise Except('ErrorCode(0010):MAC %s (%s) scan error'%(mac,argv[2][0]))
        argv[-4]('MAC %s (%s) comparison of pass'%(mac,argv[2][0]),2)
        
        lWaitCmdTerm(argv[1][-1],"ht_led_test 1234 start&","#",5,3)
        argv[1][-1]<<"nc 192.168.254.254 1234"
        time.sleep(1)
        argv[1][-1]<<"cd /sys/class/gpio; echo 18 > export && echo out > gpio18/direction && echo 0 > gpio18/value  && echo 18 > unexport && cd ~"  #Orange
        time.sleep(0.5)
        argv[1][-1]<<"cd /sys/class/gpio; echo 16 > export && echo out > gpio16/direction && echo 0 > gpio16/value  && echo 16 > unexport && cd ~"  #Red 
        time.sleep(0.5)
        argv[1][-1]<<"cd /sys/class/gpio; echo 19 > export && echo out > gpio19/direction && echo 0 > gpio19/value  && echo 19 > unexport && cd ~"  #Blue
        time.sleep(0.5)
        if GetDialogValue(argv[0]+1,'Check Ether 1000F ON') <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 1000F ON Faied')
        argv[-4]('Check Ether 1000F ON pass',2)
        
        lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        lWaitCmdTerm(argv[1][2],'speed 0 100F','speed',5)
        time.sleep(1)
        if GetDialogValue(argv[0]+1,'Check Ether 100F ') <> 'OK':
           raise Except('ErrorCode(402053):Check Ether 100F Faied')
        argv[-4]('Check Ether 100F pass',2)
        
        argv[1][2] << chr(0x03) #ctrl+c
        time.sleep(0.5)
        argv[1][2] << chr(0x03) #ctrl+c
        argv[1][2]<<'exit'

    except Except,msg:
        message = 'ErrorCode(0000):%s'%msg
    except Exception,e:
        message = 'ErrorCode(0001):%s'%e.message
    os.popen("taskkill /F /IM Dialog.exe").read()
    for try_ in range(10):
        if "Dialog.exe" not in os.popen("tasklist").read(): break
        time.sleep(0.1)
    if CML_Lock.locked():CML_Lock.release()   
    if message:
       raise Except(message)  


def CheckMACandLED_CGNV4(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''     
    argv[3](checkled)
    mac = argv[2][0]
    #sn = argv[2][1]
    password_ = argv[-3]('Base','shell_password').strip()
    #sn = GetSN(mac)
    CML_Lock.acquire()
    message = ''
    cbterm = argv[1][1]
    port=argv[0]+1
    if port >4 : port -= 4
    lWaitCmdTerm(cbterm,'rf %s c'%port,'rf',5,5)
    lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5,2)
    lWaitCmdTerm(argv[1][2],'speed 0 AUTO','speed',5,2) 
    time.sleep(2)             
    try:
        UDPort = os.popen("netstat -a -p UDP").read()
        while ":1808 " not in UDPort:
              UDPort = os.popen("netstat -a -p UDP").read()
              time.sleep(0.1)
        '''
        mac = GetDialogValue(argv[0]+1,'Scan MAC Address')
        if mac[0]=="2":mac=getmac(mac)
        if mac <> argv[2][0]:
           raise Except('ErrorCode(0010):MAC %s (%s) scan error'%(mac,argv[2][0]))
        argv[-4]('MAC %s (%s) comparison of pass'%(mac,argv[2][0]),2)
        '''
        if GetDialogValue(argv[0]+1,'Check LED ALL ON') <> 'OK':
           raise Except('ErrorCode(402053):Check LED ALL ON Faied')
        argv[-4]('Check LED ALL ON pass',2)
        
        #lWaitCmdTerm(argv[1][2],'cable 0 s','cable',5)
        #lWaitCmdTerm(argv[1][2],'speed 0 100F','speed',5)
        #time.sleep(1)
        #if GetDialogValue(argv[0]+1,'Check Ether 100F ') <> 'OK':
        #   raise Except('ErrorCode(402053):Check Ether 100F Faied')
        #argv[-4]('Check Ether 100F pass',2)
        lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,5)    
    except Except,msg:
        lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,5)    
        message = 'ErrorCode(0000):%s'%msg
    except Exception,e:
        lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,5)    
        message = 'ErrorCode(0001):%s'%e.message
    os.popen("taskkill /F /IM Dialog.exe").read()
    for try_ in range(10):
        if "Dialog.exe" not in os.popen("tasklist").read(): break
        time.sleep(0.1)
    if CML_Lock.locked():CML_Lock.release()   
    if message:
       raise Except(message)  

def GetDialogValue(dutid,msg):
    term = htx.UDPService("127.0.0.1",1808)
    term << "%s,%s"%(dutid,msg)
    data = ""
    data = term.get()
    while not data and term.isConnect():
          data = term.get()
    term.close()
    return data
       
def FresetProd(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
    for i in range(3):
        data = lWaitCmdTerm(term,"ping -c 3 -s 1024 192.168.254.254 ","#",10,2) #ATOM IP=192.168.254.254 
        lost = data.split("received")[-1].split(" packet loss")[0].strip()
        if "0%" in lost:
            log("ATOM ping connect pass",2)
            break
        if i == 2:raise Except("ATOM ping Disable")

    lWaitCmdTerm(term,"cli","nu>",8,2)   
    data = lWaitCmdTerm(term,"freset prod","Success!Exit!",30,2)
    log(data[-500:],2)
    #lWaitCmdTerm(cbterm,'rf %s n'%port,'rf',5,3)
    log('Prod reset PASS',2)

def ChangeGAmode(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    term = argv[1][-1]
    cbterm = argv[1][1]
    log = argv[-4]
    port=argv[0]+1
    if port >4 : port -= 4
     
    lWaitCmdTerm(term,"setenv usbenable y","#",8,2)   
    for i in range(3):
        data = lWaitCmdTerm(term,"printenv","#",8,2)   
        #log(data,2)
        if "usbenable=y" not in data:            
            lWaitCmdTerm(term,"setenv usbenable y","#",8,2)
            if i == 2: raise Except("Change USB enable failed")           
        else:              
             log('Change USB enable success',2)
             break 
                        
    for i in range(3):
        lWaitCmdTerm(term,"setenv MFG no","#",8,2)
        data = lWaitCmdTerm(term,"printenv","#",8,2)        
        if "MFG=no" in data:
            log(data[-50:],2)
            log('Change GA mode success',2)
            break    
        else:              
            if i == 2: raise Except("Change MFG no failed")           
    #by WCY 2015/12/29
    ''' 
    term << "reboot"   
    time.sleep(5)
    for p in range(30):
        time.sleep(1)
        data = lWaitCmdTerm(argv[1][2],'ping 1 192.168.100.1 -n 1','ping',8,2)
        if '100%' in data:
           time.sleep(10)
           log('Change GA mode success',2)
           break             
        if p==29 :raise Except('ErrorCode(E00155):Change GA mode failed')
    ''' 

##################################ADD Telnet TEST################################
def isPortConnect(ip,port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result=1
    try:
        s.connect((ip,int(port)))
    except Exception:
        result = 0
    s.close() 
    return result


def lLogin_back(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    print 'Telnet login Start'
    if isPortConnect(dstip,pid):
       print 'The port is open,wait telnet'
    else:raise Except('The port is close')
    for i in range(20):
        term = htx.Telnet(dstip,pid)
        data = term.wait("login:",5)[-1]
        print '[%s]%s'%(time.ctime(),data)
        print username
        print password
        term << username
        time.sleep(3)
        term << password
        data=term.wait('>',5)[-1]
        print '[%s]%s'%(time.ctime(),data)
        if '>' in data  or '#' in data:
            time.sleep(1)
            return term 
            break
        if i == 19:raise Except('Telnet login Failure')

def lLogin_20170901(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    print 'Telnet login Start'
    if isPortConnect(dstip,pid):
       print 'The port is open,wait telnet'
    else:raise Except('The port is close')
    print dstip
    print pid
    for i in range(20):
        #term = htx.Telnet(dstip,pid)
        term=htx_local.Telnet(dstip,pid)
        data = term.wait("#",5)[-1]     
        print '[%s]%s'%(time.ctime(),data)
        if '>' in data  or '#' in data:
            time.sleep(1)
            return term 
            break
        if i == 19:raise Except('Telnet login Failure')
        
def lLogin_20170905(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    #uid must be 101
    print 'Telnet login Start'
    for k in range(5):
        if isPortConnect(dstip,pid):
           print 'The port is open,wait telnet'
           break
        else:
           time.sleep(2)
           if k==4:raise Except('The port is close')          
    for a in range(5):
      access=0
      #term = htx.Telnet(dstip,pid)
      term=Telnet(dstip,pid,3)
      data = term.wait("login as:",5)[-1]
      print '[%s]%s'%(time.ctime(),data)
      print username
      print password    
      for i in range(5):
          term << username
          time.sleep(2)
          term << password
          data=term.wait('u>',15)[-1]
          print '[%s]%s'%(time.ctime(),data)
          if '101' in data: access=1; break 
          else: term<<'\x03'; break
          if i == 4:raise Except('Telnet login Failure')
      if access: return term            

#TOD_ESTABLISHED
def lLogin_(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    #uid must be 101
    print 'Telnet login Start'
    for k in range(5):
        if isPortConnect(dstip,pid):
           print 'The port is open,wait telnet'
           break
        else:
           time.sleep(2)
           if k==4:raise Except('The port is close')          
    for a in range(20):
      print "00000000000"
      time.sleep(5)
      access=0
      #term = htx.Telnet(dstip,pid)
      print dstip
      print pid
      term=Telnet(dstip,pid,3)
      data = term.wait("login:",5)[-1]
      print '[%s]%s'%(time.ctime(),data)
      print username
      print password    
      for i in range(5):
          print "111111111111"
          term << username
          time.sleep(2)
          term << password
          data=term.wait('>',15)[-1]
          print "222222222222222222"
          print '[%s]%s'%(time.ctime(),data)
          if '101' in data: access=1; break 
          else: term<<'\x03'; break
          if i == 4:
            term << '\x03'
            raise Except('Telnet login Failure')
      if access: return term            

def lLogin__(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    #uid must be 101
    print 'y--Telnet login Start--y'
    for k in range(5):
        if isPortConnect(dstip,pid): break ; print 'The port is open,wait telnet'           
        else:
           time.sleep(2)
           if k==4: raise Except('The port is close')          
    for a in range(20):
      time.sleep(1)
      access=0
      term = htx_local.Telnet(dstip,pid)
      #term=Telnet(dstip,pid,3)
      data = term.wait("login:",5)[-1]
      print '[%s]%s'%(time.ctime(),data)
      print username
      print password    
      for i in range(3):
          term << username
          time.sleep(1)
          term << password
          data=term.wait('mainMenu>',25)[-1]
          print '[%s]%s'%(time.ctime(),data)
          if '101' in data: access=1; break 
          else: term.close(); break
          if i == 2:
            term.close()
            raise Except('Telnet login Failure')
      if access: return term

def lLogin_20180807(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    #uid must be 101
    print 'y--Telnet login Start--y'
    for k in range(5):
        if isPortConnect(dstip,pid): break ; print 'The port is open,wait telnet'           
        else:
           time.sleep(2)
           if k==4: raise Except('The port is close')          
    #CML_Lock.acquire()
    uid_list=list()
    for try1 in range(3):
      uid = htx_local.Telnet(dstip,pid); time.sleep(3)
      uid_list.append(uid); time.sleep(0.1)#print pid,uid_list
      for uid in uid_list:
        start_time=time.time()
        while time.time()-start_time<=10:
          print 'uid:', uid
          if uid:
            try2=0
            while try2<=2:
              if uid.wait("login as:",2)[0]: uid << username
              if uid.wait("Password:",2)[0]: uid << password
              data=uid.wait("mainMenu>",13); print data
              if '101' in data[-1]: 
                #if CML_Lock.locked(): CML_Lock.release()
                return uid
              else: uid.close(); print pid +' telnet close'; break
              if try2 == 2: uid.close(); print pid +' telnet close'
              try2+=1
            break
          else: time.sleep(1)
      if uid_list:
        for term in uid_list: 
          try: term.close()
          except: print'ERROR:telnet.close()'; pass
    #if CML_Lock.locked(): CML_Lock.release()
    #raw_input('telnet fail') 
    #raise Except('Telnet login Failure')
    return 0

def lLogin(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    #uid must be 101
    print 'y--Telnet login Start--y'    
    uid = htx_local.Telnet(dstip,pid)
    uid.get()
    if uid:
        for chance in xrange(3):      
            if uid.wait('#',2)[0]: 
                TelnetWaitCmdTerm(uid,username,'#',2)
                data=TelnetWaitCmdTerm(uid,password,'#',3); 
                if '#' in data: return uid
                else: return 0 
            elif uid.wait('#',2)[0]:
                data=TelnetWaitCmdTerm(uid,password,'#',3); 
                if '#' in data: return uid  
                else: return 0 
            else: uid << ''
    for k in range(5):
        if isPortConnect(dstip,pid): break ; print 'The port is open,wait telnet'           
        else:
           time.sleep(2)
           if k==4: raise Except('The port is close')          
    return 0

def lLogin_AFI1(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    #uid must be 101
    print 'y--Telnet login Start--y'    
    uid = htx_local.Telnet(dstip,pid)
    uid.get()
    if uid:
        for chance in xrange(3):      
            if uid.wait('as',2)[0]: 
                TelnetWaitCmdTerm(uid,username,'Password:',2)
                data=TelnetWaitCmdTerm(uid,password,'nu>',15); 
                if '101' in data: return uid
                else: return 0 
            elif uid.wait('Password:',2)[0]:
                data=TelnetWaitCmdTerm(uid,password,'nu>',15); 
                if '101' in data: return uid  
                else: return 0 
            else: uid << ''
    for k in range(5):
        if isPortConnect(dstip,pid): break ; print 'The port is open,wait telnet'           
        else:
           time.sleep(2)
           if k==4: raise Except('The port is close')          
    return 0

def SnmpGetDUTipOpenTelnet_LAN(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut
    '''
    for p in range(20):
        time.sleep(1)
        data = lWaitCmdTerm(argv[1][2],'ping 1 192.168.100.1 -n 1','ping',8,2)
        #lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5)
        print data
        if '100%' not in data:break             
        if p==99 :raise Except('ErrorCode(E00155):switch port 1 ping failed')

    mac = argv[2][0]
    log = argv[-4]
    c_port = argv[0]
    ETH0IP = argv[-3]('AFI','ETH0IP').split('|')
    ETH0IP_ = ETH0IP[0].strip()
    print argv[0]
    if argv[0] > 3 : 
       c_port = argv[0] - 4
       ETH0IP_ = ETH0IP[1].strip()
    port = c_port + 1
    pid = '30%s1'%(port+1)
    timeout = int(argv[-3](argv[-2],'timeout'))
    username = argv[-3]('Base','username').strip()
    password_ = argv[-3]('Base','password_').strip()
    #argv[1][-1] = lLogin(ETH0IP_,pid,username,password_)
    argv[-4]('LAN login OK!')

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
    mac = argv[2][0]
    #if mac[-1] <> '8':
    #    raise Except("Fail:mac[-1] not is 8")
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
    raise Except("%s Connect Fail,Please Check LAN Port"%ip)
    
    
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
    
                
def lLogin_select(dstip,pid,username,password):
    #term.host -- dst ip
    #term.port -- dst port
    print 'Telnet login Start'
    if isPortConnect(dstip,pid):
       print 'The port is open,wait telnet'
    else:raise Except('The port is close')
    for i in range(5):
        term = htx.Telnet(dstip,pid)
        data = term.wait("#",8)[-1]
        print '[%s]%s'%(time.ctime(),data)
        term << "\n"
        data=term.wait('#',10)[-1]
        print '[%s]%s'%(time.ctime(),data)
                    
        if 'login as:' in data:
            print username
            print password
            term << username
            time.sleep(2)
            term << password
            data=term.wait('Menu>',10)[-1]
            print '[%s]%s'%(time.ctime(),data)
            if 'Menu>' in data:
                time.sleep(2) 
                                            
                lWaitCmdTerm(term,"","nu>",8,3)            
                lWaitCmdTerm(term,"shell","rd:",8,2)
                lWaitCmdTerm(term,"AccessDeny","#",15,2)
                lWaitCmdTerm(term," ","#",15,2)                                                             

                for n in range(5):            
                    lWaitCmdTerm(term,"setenv MFG yes","#",8,2) 
                    data1 = lWaitCmdTerm(term,"printenv","#",15,2)
                    time.sleep(1)        
                    if "MFG=yes" in data1:
                        time.sleep(1)
                        term << "reboot"   
                        time.sleep(70)                             
                        raise Except("MFG mode is No,Please Retest")  
                    else:
                        if n == 4:                    
                            raise Except("MFG mode is not yes")               
            else: 
                raise Except(" Telnet login as: password FAIL") 
                
        if '#' in data:        
            time.sleep(1)
            return term 
            break                                          
        if i == 4:raise Except('Telnet login Failure')  
    

#parameter=dict()
argv_locks=thread.allocate_lock()
def TelnetLogin_select(*argv):
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
    lanip = argv[-3]('Base','LANIP') 
    for p in range(30):
        time.sleep(2)
        data = lWaitCmdTerm(argv[1][2],'ping 1 %s -n 1'%lanip,'ping',8,2); print data
        #lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5)
        if '100%' not in data:break             
        if p==29 :raise Except('ErrorCode(E00155):switch port 1 ping failed')
    argv[1][-1]=lLogin(ETH0IP_,pid,username,password_)
    #argv[1].append(lLogin(ETH0IP_,pid,username,password_))
    if argv[1][-1]:
        argv_locks.acquire()  
        import temp
        temp.pid_parameter.update({str(ETH0IP_)+'-'+pid:argv}) #print temp.pid_parameter 
        argv=temp.pid_parameter[str(ETH0IP_)+'-'+pid]
        if argv_locks.locked(): 
            argv_locks.release()
            print pid+'lock-close'
        argv[-4]('ARM Telnet login')      
        return argv[1][-1]
    if argv_locks.locked(): argv_locks.release()
    raise Except('Telnet login Failure')

def TelnetLogin_select_AFi1(*argv):
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
    lanip = argv[-3]('Base','LANIP') 
    for p in range(30):
        time.sleep(2)
        data = lWaitCmdTerm(argv[1][2],'ping 1 %s -n 1'%lanip,'ping',8,2); print data
        #lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5)
        if '100%' not in data:break             
        if p==29 :raise Except('ErrorCode(E00155):switch port 1 ping failed')
    argv[1][-1]=lLogin_AFI1(ETH0IP_,pid,username,password_)
    #argv[1].append(lLogin(ETH0IP_,pid,username,password_))
    if argv[1][-1]:
        argv_locks.acquire()  
        import temp
        temp.pid_parameter.update({str(ETH0IP_)+'-'+pid:argv}) #print temp.pid_parameter 
        argv=temp.pid_parameter[str(ETH0IP_)+'-'+pid]
        if argv_locks.locked(): 
            argv_locks.release()
            print pid+'lock-close'
        argv[-4]('ARM Telnet login')      
        return argv[1][-1]
    if argv_locks.locked(): argv_locks.release()
    raise Except('Telnet login Failure')



def RepairLanLoss(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    log = argv[-4]
    term = argv[1][-1]
    
    lWaitCmdTerm(term,'quit','#',10,3)
    lWaitCmdTerm(term,'cd /sys/devices/switch/QCA8337/register/','#',10,3)
    lWaitCmdTerm(term,'echo 0x4 > address','#',10,3)
    lWaitCmdTerm(term,'echo 0x87700000 > data','#',10,3)
    #lWaitCmdTerm(term,'quit','#',10,3)
    time.sleep(2)
    log('Repair Lan Loss PASS',2)
