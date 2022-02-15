

class WIFIThread(threading.Thread):
      def __init__(self,id,ssid,wpakey,wifi_target,packetsize,ping_loss,log):
          threading.Thread.__init__(self)
          self.id=id
          self.wifi_id=int((id-1)/2)
          self.ssid=ssid
          self.wpakey=wpakey
          self.wifi_target=wifi_target
          self.packetsize = packetsize
          self.ping_loss = ping_loss
          self.running=True
          self.mainrunning=True
          self.msg=[1,'[%s]wifi error,no test'%self.ssid]
      def run(self):
          try:              
              WIFIMutex[0].acquire()
              print '[%s]WIFI function to start the test'%self.ssid
              Connected=''
              testflag=1
              value='[%s]wifi error,no test'%self.ssid
              for i in range(6):
                  if self.mainrunning:
                      #if not Connected:
                         #Connected=SetDongleConnection(0,self.ssid,self.wpakey)
                      Connected=WLAN(self.ssid).connect()
                      print Connected
                      if 'ERROR' not in Connected:
                         try:
                             print '[%s]%s to wait for wireless connectivity'%(self.ssid,self.wifi_target)
                             os.system('arp -d')
                             if htx.IsConnect(self.wifi_target,10):
                                print 'Ping function to start the test'
                                print self.wifi_target,self.packetsize
                                
                                value = Ping(self.wifi_target,self.packetsize,10,800)
                                print '#############################'
                                print value
                                print '#############################'
                             else:
                                value=200
                         except ValueError:
                             value=200    
                         if value > self.ping_loss:
                            if value ==200:
                               Connected=0
                         if value < self.ping_loss:
                            testflag=0
                            break
                      else:
                         value=Connected
                         if not('search' in value or 'too low' in value or 'connect %s failed'%self.ssid in value ):break
                         print value
                         time.sleep(5)
              self.msg= testflag,value
          except:
             pass
          if WIFIMutex[0].locked():
             WIFIMutex[0].release()
          self.running=False
           
class WLAN:
      def __init__(self,ssid,signal=30,pwd='u'):
          #self.mac=bssid.lower()
          #self.bssid=self.mac[:2] + ' ' + self.mac[2:4] + ' ' + self.mac[4:6] + ' ' + self.mac[6:8] + ' ' + self.mac[8:10] + ' ' + self.mac[10:]
          self.ssid=ssid
          self.pwd=pwd
          self.signal=signal
          self.StartSVC()
          msg=self.GetGUID()
          if 'ERROR' in msg:return msg
          self.guid,self.state=msg
          self.profilepath='profile.xml'
          
          
      def StartSVC(self):
          os.popen('net start wzcsvc')
          
      def StopSVC(self):
          os.popen('net stop wzcsvc')
      
      def GetGUID(self):
          msg=os.popen('WLAN.exe ei').read()
          print msg
          if 'GUID' not in msg:
             raise Except('ERROR : No wifi dongle')
          for g in msg.split('\n'):
              if 'GUID' in g:
                 guid=g.split('GUID:')[-1].strip()
              if 'State' in g:
                 state=msg.split('State: "')[-1].split('"')[0]  
          return guid,state
          
      def scan(self):
          msg=os.popen('WLAN.exe scan %s'%self.guid).read()
          if 'successfully' not in msg:
             raise Except('ERROR:WIFI dongle scan failed')
          return 'WIFI dongle scan successfully'
      
      def GetBSSID(self):
          msg=os.popen('WLAN.exe gbs %s'%self.guid).read()
          if 'successfully' not in msg:
             raise Except('ERROR:WIFI dongle get bssid failed')
          if self.bssid in msg:
             ssid=msg.split(self.bssid)[-1].split('Beacon period:')[0].split('SSID:')[-1].strip()
             if self.ssid <> ssid:
                raise Except('ERROR:DUT SSID set failed:%s(%s)'%(ssid,self.ssid))
             return 'WIFI dongle get ssid successfully'
          if self.ssid in msg:
            bssid=msg.split(self.ssid)[0].split('MAC address:')[-1].strip().split()[0]
            if self.bssid<>bssid:
               raise Except('ERROR:DUT BSSID set failed:%s(%s)'%(bssid,self.bssid))
          raise Except('ERROR:WIFI dongle not search for \'%s\' signal'%self.ssid)
             
      def GetVNL(self):
          msg=os.popen('wlan.exe gvl %s'%self.guid).read() 
          if 'successfully' not in msg:
             raise Except('ERROR:WIFI dongle get visible wireless networks failed')  
          if self.ssid not in msg:
             raise Except('ERROR:WIFI dongle not search for \'%s\' signal'%self.ssid)
          msg=msg.split(self.ssid)[-1].split('Default')[0]
          if self.pwd<>'u' and 'Security not enabled' in msg:
             raise Except('ERROR:DUT WIFI did not set up encryption')
          elif self.pwd=='u' and 'Security enabled' in msg:
             raise Except('ERROR:DUT WIFI set up encryption')    
          if 'Infrastructure' in msg:
             bsstype='i'
          else:
             bsstype='a' 
          signal=int(msg.split('Signal quality:')[-1].split('%')[0].strip())
          if signal < self.signal:
             raise Except('ERROR:DUT WIFI signal is too low:%s (<%s)'%(signal,self.signal))
          #return bsstype
          return 'WIFI dongle check %s network info successfully'%self.ssid
      
      def GetQI(self):
          for try_ in range(6):
              msg=os.popen('WLAN.exe qi %s'%self.guid).read() 
              if 'successfully' not in msg:
                 raise Except('ERROR:WIFI dongle query interface failed')  
              if self.ssid not in msg:
                 time.sleep(0.5)
                 if try_==5:raise Except('ERROR:WIFI dongle connect %s failed'%self.ssid)
              else:return 'WIFI dongle connect %s successfully'%self.ssid
           
      def disconnect(self):
          msg=os.popen('WLAN.exe dc %s'%self.guid).read() 
          if 'successfully' not in msg:
             raise Except('ERROR:WIFI dongle disconnect failed')
          return 'WIFI dongle disconnect successfully'  
      
      def delprofile(self):
          msg=os.popen('WLAN.exe gpl %s'%self.guid).read() 
          if 'successfully' not in msg:
             raise Except('ERROR:WIFI dongle list profile failed')
          profile=msg.split('Command')[0].split('interface.')[-1]
          for f in profile.split('\n'):
              f=f.strip()
              if f:
                  msg=os.popen('WLAN.exe dp %s %s'%(self.guid,f)).read() 
                  if 'successfully' not in msg:
                     raise Except('ERROR:WIFI dongle delete %s profile failed'%f)
          return 'WIFI dongle delete profile list successfully'
            
      def setprofile(self):
          msg=os.popen('wlan.exe sp %s %s'%(self.guid,self.profilepath)).read() 
          if 'successfully' not in msg:
             raise Except('ERROR:WIFI dongle set profile failed')
          return 'WIFI dongle set profile successfully'
      
             
      def createprofile(self):
          ssid_=''
          for s in self.ssid:
              ssid_ += '%X'%ord(s)
          xml='''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
	<name>AFI_WLAN</name>
	<SSIDConfig>
		<SSID>
			<hex>%s</hex>
			<name>%s</name>
		</SSID>
	</SSIDConfig>
	<connectionType>ESS</connectionType>
	<MSM>
		<security>
			<authEncryption>
				<authentication>open</authentication>
				<encryption>none</encryption>
				<useOneX>false</useOneX>
			</authEncryption>
		</security>
	</MSM>
</WLANProfile>
'''%(ssid_,self.ssid)       
          f=open(self.profilepath,'w')
          f.write(xml)
          f.close()
          return 'Create profile successfully'   
                     
      def discover(self):
          try:
             self.StartSVC()
             print '[%s]%s'%(self.ssid,self.scan()) 
             time.sleep(1)
             print '[%s]%s'%(self.ssid,self.GetVNL())
             #print '[%s]%s'%(self.ssid,self.GetBSSID())
             guid,state=self.GetGUID()
             if state=='connected':
                print '[%s]%s'%(self.ssid,self.disconnect())
                time.sleep(1)
             time.sleep(1)
             msg=os.popen('wlan.exe disc %s %s %s %s'%(self.guid,self.ssid,bss,self.pwd)).read()
             if 'successfully' not in msg:
                raise Except('ERROR:WIFI dongle connect %s failed'%self.ssid)  
             return '[%s]%s'%(self.ssid,self.GetQI())    
          except Except,msg:
             return '[%s]%s'%(self.ssid,msg)
             
      def connect(self):
          try:
             self.StopSVC()
             self.StartSVC()

             print '[%s]%s'%(self.ssid,self.createprofile())
             print '[%s]%s'%(self.ssid,self.scan())
             time.sleep(1)
             '''
             for i in range(5):
                 print '[%s]%s'%(self.ssid,self.createprofile())
             for k in range(5):    
                 print '[%s]%s'%(self.ssid,self.scan()) 
                 time.sleep(1)
             '''    
             print '[%s]%s'%(self.ssid,self.GetVNL())
             guid,state=self.GetGUID()
             if state=='connected':
                print '[%s]%s'%(self.ssid,self.disconnect())
             print '[%s]%s'%(self.ssid,self.delprofile())
             print '[%s]%s'%(self.ssid,self.setprofile())
             return '[%s]%s'%(self.ssid,self.GetQI())    
          except Except,msg:
             return '[%s]%s'%(self.ssid,msg)    
                         
                  
#print WLAN('HOME-67A8').connect()                      
#print WLAN('Test5/6/7/8 AP').connect() 
          
          
def Ping(ip,length,count,interval):
    """    Ping(ip,length,count,interval), return the loss rate (float)
        where ip is target ip address, length is IP packet length
              count is packet number, interval is ms unit"""        
    result = os.popen(tool_dir+"/hrping -f -l %d -s %d -n %d %s"%(length-14,interval,count,ip)).read()
    #print result
    return float(result[result.rfind("(")+1:result.rfind("%")])   
          
def Pingtry(term,ip,port,timeout):
    stime=time.time()
    while time.time()-stime < timeout:
          data=lWaitCmdTerm(term,'ping %s %s 64 5 200'%(port,ip),'%',15)
          if ('0%' in data) and ('100%' not in data):
             return 1
    return 0         
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
