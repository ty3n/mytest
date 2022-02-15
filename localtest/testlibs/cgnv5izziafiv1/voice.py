from toolslib_local import *


def voice_init(term):
    #lWaitCmdTerm(term,"top","RootMenu>",5)
    #lWaitCmdTerm(term,"cable","cable>",5)  
    lWaitCmdTerm(term,"voice","MXP>",5,5) 
    #lWaitCmdTerm(term,ticliHead+"ca/voice","MXP>",5)
    lWaitCmdTerm(term,"prodtest enable on","MXP>",5,5) #enable the EMTA port

def Checkhook(term,vmterm,vmport,log):  
    for try_ in range(3):
        lWaitCmdTerm(vmterm,"dc %s min"%vmport[0],"dc",5)
        lWaitCmdTerm(vmterm,"dc %s min"%vmport[1],"dc",5) 
        data = lWaitCmdTerm(term,"prodtest gethookstatus 0","MXP>",5,2) 
        if "offHook" not in data:   
           if try_ == 2:raise Except('ErrorCode(0000): check telphone line 0 offhook status fail !')
           continue
        data = lWaitCmdTerm(term,"prodtest gethookstatus 1","MXP>",5,2) 
        if "offHook" not in data:   
           if try_ == 2:raise Except('ErrorCode(0000): check telphone line 1 offhook status fail !')   
           continue
        log("check telphone offhook status pass" )   
        break   
    
    for try_ in range(3):
        lWaitCmdTerm(vmterm,"ring %s 1"%vmport[0],"ring",8)
        lWaitCmdTerm(vmterm,"ring %s 1"%vmport[1],"ring",8)
        data = lWaitCmdTerm(term,"prodtest gethookstatus 0","MXP>",5,2) 
        if "onHook" not in data:   
           if try_ == 2:raise Except('ErrorCode(0000): check telphone line 0 onhook status fail !')
           continue
        data = lWaitCmdTerm(term,"prodtest gethookstatus 1","MXP>",5,2) 
        if "onHook" not in data:   
           if try_ == 2:raise Except('ErrorCode(0000): check telphone line 1 onhook status fail !')   
           continue
        log("check telphone onhook status pass" )   
        break     

def voice_ring_on(term):
    #if en=='on':
    
    lWaitCmdTerm(term,"tiuhw set 0 hwcfg ringer sin 25 66 0","MXP>",8,3)
    lWaitCmdTerm(term,"tiuhw set 1 hwcfg ringer sin 25 66 0","MXP>",8,3)
    lWaitCmdTerm(term,"tiu status 0","MXP>",8,3) 
    lWaitCmdTerm(term,"tiu status 1","MXP>",8,3)
    lWaitCmdTerm(term,"tiuhw set 0 ring on","MXP>",8,3)
    lWaitCmdTerm(term,"tiuhw set 1 ring on","MXP>",8,3)

    #lWaitCmdTerm(term,"tiuhw wr 0 0x56 0x27","MXP>",8,3)
    #lWaitCmdTerm(term,"tiuhw wr 1 0x56 0x27","MXP>",8,3)
    
    
    #lWaitCmdTerm(term,"prodtest setring 0 %s"%en,"MXP>",5,2)
    #lWaitCmdTerm(term,"prodtest setring 1 %s"%en,"MXP>",5,2)  

def voice_ring_off(term):
    #if en=='on':
       #lWaitCmdTerm(term,"tiuhw set 0 hwcfg ringer sin 25 66 0","MXP>",5)
       #lWaitCmdTerm(term,"tiuhw set 1 hwcfg ringer sin 25 66 0","MXP>",5)
    lWaitCmdTerm(term,"tiuhw set 0 ring off","MXP>",5,3)
    lWaitCmdTerm(term,"tiuhw set 1 ring off","MXP>",5,3)
    #lWaitCmdTerm(term,"tiuhw wr 0 0x56 0x2b","MXP>",5,3)
    #lWaitCmdTerm(term,"tiuhw wr 1 0x56 0x2b","MXP>",5,3)

def exit_voice(term):
    lWaitCmdTerm(term,"prodtest enable off","MXP>",5,3) #disable the EMTA port  
    #lWaitCmdTerm(term,"exit","cable>",5)
 
def LoopCurrent_factory(vmport,term,vmterm,ohm,log,loopc,loopc_offset)  :
    #ohm = max > ohm = 1.4k
    #ohm = min > ohm = 300
    #ohm = max > ohm = 600  #for hub4
    #ohm = min > ohm = 385

    flag = 0
    cpkdata={}
    if vmport in (1,3):line=0
    else:line=1
    r_dic={"max":[1400,600],"min":[300,385]}
    result=0
       
    if ohm == 'max':
        flag = 1
        status = 'onHook'
    else:
        status = 'offHook'

    for try_ in range(10):
        if line and try_>=4: lWaitCmdTerm(vmterm,'dc %s %s'%((vmport-1),ohm),'dc',5,3)
        r_=lWaitCmdTerm(vmterm,'dc %s %s'%(vmport,ohm),'dc',5,3)
        print r_
        r_=r_.split('\t')[-1]
        print r_
        try:
           r_=float(r_.split('mA')[0])
        except:
           if try_==9: raise Except('ErrorCode(101016):Loop current line:%s ohm:%s read failure'%(line,ohm))
           continue 
        r=((r_*r_dic[ohm][0])/r_dic[ohm][1]) 
        print r 
        if r <= loopc[flag] + loopc_offset[flag] and  r >= loopc[flag] - loopc_offset[flag]:
              result=1
              break
        else: time.sleep(5) 
    msg="Loop Current mode line %d LENTHohm state %s boost (mA): %3.2f (%.2f ~ %.2f)"%(line,
        ohm,r,loopc[flag] - loopc_offset[flag],loopc[flag] + loopc_offset[flag])
    log('%s'%msg)
    ##### Check Hook Status Test 20180522##########    
    for try_ in range(3):
        if ohm == 'max': 
            lWaitCmdTerm(vmterm,"ring %s 1"%vmport,"ring",8)
            time.sleep(0.3)
        data = lWaitCmdTerm(term,"prodtest gethookstatus %s"%line,"MXP>",8,2) 
        if status not in data:   
            if try_ == 2:raise Except('ErrorCode(0000): check telphone line %s %s status\n'%(line,status)+data)
            continue
        msg_ = "Check line %s Hook Status: %s status Pass"%(line,status)
        result+=1   
        break
    #cpkdata['Hook Status Line %s'%line] = 'PASS'
    log('%s'%msg_)
    if not result :
       raise Except('ErrorCode(101016):Loop current line:%s ohm:%s boost: %3.2f mA (%.2f ~ %.2f)'%(line,ohm,r,loopc[flag] - loopc_offset[flag],loopc[flag] + loopc_offset[flag]))
    #return cpkdata

def LoopCurrent(vmport,term,vmterm,ohm,log,loopc,loopc_offset)  :
    #ohm = max > ohm = 1.4k
    #ohm = min > ohm = 300
    #ohm = max > ohm = 600  #for hub4
    #ohm = min > ohm = 385

    flag = 0
    cpkdata={}
    if vmport in (1,3):line=0
    else:line=1
    r_dic={"max":[1400,600],"min":[300,385]}
    result=0
       
    if ohm == 'max':
        flag = 1
        status = 'onHook'
    else:
        status = 'offHook'

    for try_ in range(10):
        if line and try_>=4: lWaitCmdTerm(vmterm,'dc %s %s'%((vmport-1),ohm),'dc',5,3)
        r_=lWaitCmdTerm(vmterm,'dc %s %s'%(vmport,ohm),'dc',5,3)
        print r_
        r_=r_.split('\t')[-1]
        print r_
        try:
           r_=float(r_.split('mA')[0])
        except:
           if try_==9: raise Except('ErrorCode(101016):Loop current line:%s ohm:%s read failure'%(line,ohm))
           continue 
        #r=((r_*r_dic[ohm][0])/r_dic[ohm][1]) 
        r=r_
        print r 
        if r <= loopc[flag] + loopc_offset[flag] and  r >= loopc[flag] - loopc_offset[flag]:
              result=1
              break
        else: time.sleep(5) 
    msg="Loop Current mode line %d LENTHohm state %s boost (mA): %3.2f (%.2f ~ %.2f)"%(line,
        ohm,r,loopc[flag] - loopc_offset[flag],loopc[flag] + loopc_offset[flag])
    log('%s'%msg)
    if not result :
       raise Except('ErrorCode(101016):Loop current line:%s ohm:%s boost: %3.2f mA (%.2f ~ %.2f)'%(line,ohm,r,loopc[flag] - loopc_offset[flag],loopc[flag] + loopc_offset[flag]))
    result=0
    ##### Check Hook Status Test 20180522##########    
    for try_ in range(3):
        if ohm == 'max': 
            lWaitCmdTerm(vmterm,"ring %s 1"%vmport,"ring",8)
            time.sleep(0.3)
        data = lWaitCmdTerm(term,"prodtest gethookstatus %s"%line,"MXP>",8,2) 
        if status not in data:   
            if  vmport in (1,3):  
                if ohm == 'max': lWaitCmdTerm(vmterm,"ring %d 1"%(vmport+1),"ring",8)
                else:  lWaitCmdTerm(vmterm,'dc %d %s'%((vmport+1),ohm),'dc',5,2) 
            else:
                if ohm == 'max': lWaitCmdTerm(vmterm,"ring %s 1"%(vmport-1),"ring",8)
                else:  lWaitCmdTerm(vmterm,'dc %d %s'%((vmport-1),ohm),'dc',5,2)   
            if try_ == 2:raise Except('ErrorCode(0000): check telphone line %s %s status\n'%(line,status)+data)
            continue
        msg_ = "Check line %s Hook Status: %s status Pass"%(line,status)
        result+=1   
        break
    if result:log('%s'%msg_)
    else:raise Except('ErrorCode(0000): check telphone line %s %s status.\n'%(line,status)+data)

def IdleStateVoltage(vmport,vmterm,log,idle,idle_offset):
    if vmport in (1,3):line=0
    else:line=1
    result = 0
    cpkdata={}
    for try_ in range(5):
        r=lWaitCmdTerm(vmterm,'dc %s none'%vmport,'dc',5).split('\t')[-1]
        try:
           r=float(r.split('V')[0])
        except:
           if try_==4: raise Except('ErrorCode(101017):Idle Voltage line:%s read failure'%line)
           continue   
        if r <= idle + idle_offset and  r >= idle - idle_offset :
              result=1
              break 
    msg="Idle Voltage mode line %d (V): %3.2f (%.2f ~ %.2f)"%(line,r,idle - idle_offset,idle + idle_offset)
    #message='%s,2,0,%s'%(id,msg)
    #SendData(message,log) 
    log(msg)
    #cpkdata['Idle_Voltage_line_%s'%line]=(idle - idle_offset,idle + idle_offset,r)
    if not result:
       raise Except('ErrorCode(101017):Idle Voltage line %d : %3.2f V (%.2f ~ %.2f)'%(line,r,idle - idle_offset,idle + idle_offset))
    return cpkdata
    
    
def RingSource(term,vmterm,vmport,log,ring,ring_offset,ringtime,ringtime_offset):    
    if vmport in (1,3):line=0
    else:line=1
    result = 0
    cpkdata={}
    for try_ in range(5):
        # Ring 1 REN
        lWaitCmdTerm(vmterm,'ring %s 5'%vmport,'ring',10)
        time.sleep(1)
        voice_ring_on(term)
        time.sleep(1)
        r1=lWaitCmdTerm(vmterm,'ring %s 1'%vmport,'ring',10).split('\t')[-1]
        r5=lWaitCmdTerm(vmterm,'ring %s 5'%vmport,'ring',10).split('\t')[-1]
        
        try:
            t=float(r1.split('ms')[0])
            v=float(r1.split(',')[-1].split('V')[0])
            v5=float(r5.split('V')[0])
        except:
            if try_==4: raise Except('ErrorCode(101018):Ring Source line:%s read failure'%line)
            voice_ring_off(term)
            continue 
        if v5>=v: continue
        if (t <=ringtime+ringtime_offset) and (t >=ringtime-ringtime_offset) and (v <=ring[0]+ring_offset[0]) and (v >=ring[0]-ring_offset[0]) and (v5 <=ring[1]+ring_offset[1]) and (v5 >=ring[1]-ring_offset[1]) :
           result = 1
           break
      
    msg="Ring source mode line %d time(ms): %3.2f (%.2f ~ %.2f)"%(line,t,ringtime-ringtime_offset,ringtime+ringtime_offset)
    log(msg)
    #cpkdata['Ring_source_line_%d_time'%line]=(ringtime-ringtime_offset,ringtime+ringtime_offset,t)
    msg="Ring source mode line %d 1REN voltage(V): %3.2f (%.2f ~ %.2f)"%(line,v,ring[0]-ring_offset[0],ring[0]+ring_offset[0])
    log(msg)
    #cpkdata['Ring_source_line_%d_1REN'%line]=(ring[0]-ring_offset[0],ring[0]+ring_offset[0],v)
    
    msg="Ring source mode line %d 5REN voltage(V): %3.2f (%.2f ~ %.2f)"%(line,v5,ring[1]-ring_offset[1],ring[1]+ring_offset[1])
    log(msg)
    #cpkdata['Ring_source_line_%d_5REN'%line]=(ring[1]-ring_offset[1],ring[1]+ring_offset[1],v5)
    if not result:
       raise Except('ErrorCode(101018):Line %d Ring Test: 1REN:%3.2f V(%.2f ~ %.2f) 5REN:%3.2f V(%.2f ~ %.2f) time: %3.2f(%.2f ~ %.2f)'%(line,v,ring[0]-ring_offset[0],ring[0]+ring_offset[0],v5,ring[1]-ring_offset[1],ring[1]+ring_offset[1],t,ringtime-ringtime_offset,ringtime+ringtime_offset))
    voice_ring_off(term) 
    #return cpkdata    

def DtmfSource___20171207(term,vmterm,vmport,log):
    result=0
    
    flag=0
    #message='%s,2,1,DTMF Source Test '
    #SendData(message,log)
    test_time=time.time()
    for try_ in range(2):
        lWaitCmdTerm(vmterm,'dtmf 1 %s %s'%(vmport,vmport+1),'dtmf',10)
        print lWaitCmdTerm(term,'prodtest setport2portxc 0 1 on','',10)
        time.sleep(8)        
        tone1=lWaitCmdTerm(vmterm,'dtmf 8 %s %s'%(vmport,vmport+1),'dtmf',10).split('\t')[-1].strip()
        tone2=lWaitCmdTerm(vmterm,'dtmf 9 %s %s'%(vmport+1,vmport),'dtmf',10).split('\t')[-1].strip()
        if '8' in tone1 and '9' in tone2:
           result = 1
           term << '\n'
           break
        else: term << '\n'
    log('Dtmf Source line 0: %s (8) , line 1: %s (9)'%(tone1,tone2))
    if not result:
       raise Except('ErrorCode(405061):DTMF Source Failure') 

def DtmfSource_(term,vmterm,vmport,log):
    result=0
    lWaitCmdTerm(vmterm,'dc %s min'%vmport,'dc',5,3)
    lWaitCmdTerm(vmterm,'dc %s min'%(vmport+1),'dc',5,3)    
    data=lWaitCmdTerm(term,'prodtest setport2portxc 0 1 on','action',10)
    time.sleep(3)    
    for try_ in range(5):
        tone1=lWaitCmdTerm(vmterm,'dtmf 8 %s %s'%(vmport,vmport+1),'dtmf',10).split('\t')[-1].strip()
        tone2=lWaitCmdTerm(vmterm,'dtmf 9 %s %s'%(vmport+1,vmport),'dtmf',10).split('\t')[-1].strip()
        if 'no ring signal' in tone1 or 'no ring signal' in tone2:
           if try_== 4 : raise Except('ErrorCode(405061):Xconnect set faiure')
           time.sleep(2); continue
        elif '8' in tone1 and '9' in tone2: result = 1; break
    log('Dtmf Source line 0: %s (8) , line 1: %s (9)'%(tone1,tone2))
    if not result:
       raise Except('ErrorCode(405061):DTMF Source Failure') 

def DtmfSource(term,vmterm,vmport,log):
    result=0
    port1=0
    port2=0
    lWaitCmdTerm(vmterm,'dc %s min'%vmport,'dc',5,3)
    lWaitCmdTerm(vmterm,'dc %s min'%(vmport+1),'dc',5,3)    
    lWaitCmdTerm(term,'prodtest setport2portxc 0 1 on','action is 1',10)
    time.sleep(8)    
    for try_ in range(15):
        msg=str()
        if not port1: 
           tone1=lWaitCmdTerm(vmterm,'dtmf 8 %s %s'%(vmport,vmport+1),'dtmf',10).split('\t')[-1].strip()
           msg+=tone1   
        
        time.sleep(2)

        if not port2: 
           tone2=lWaitCmdTerm(vmterm,'dtmf 9 %s %s'%(vmport+1,vmport),'dtmf',10).split('\t')[-1].strip()
           msg+=tone2          
        
        
        if 'no ring signal' in msg:
           if try_== 14: raise Except('ErrorCode(405061):Xconnect set faiure')
           time.sleep(2); continue
        if '8' in tone1: port1=1
        if '9' in tone2: port2=1
        if port1 and port2: result=1; break
        else:
           if not port1: log('retry%s_line0 DTMF:%s'%(try_,tone1)) 
           if not port2: log('retry%s_line1 DTMF:%s'%(try_,tone2))
           if try_==14:
              if port1 or port2: result = 1; log('*-*'); break 
              #if not port1 and not port2: result = 1; log('x_x'); break 
    #log('Dtmf Source line 0: %s (8) , line 1: %s (9)'%(tone1,tone2))
    lWaitCmdTerm(term,'prodtest setport2portxc 0 1 off','action is 0',5)
    #term << 'prodtest setport2portxc 0 1 off'; time.sleep(1)
    if port1: log('DTMF line 0: %s (8)'%tone1)
    if port2: log('DTMF line 1: %s (9)'%tone2)    
    if not result:
       raise Except('ErrorCode(405061):DTMF Source Failure') 
    log('Dtmf Pass')
def Voicefunction_factory(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    loopc = eval(argv[-3]('Base','loopc'))
    loopc_offset = eval(argv[-3]('Base','loopc_offset'))
    idle = eval(argv[-3]('Base','idle'))
    idle_offset = eval(argv[-3]('Base','idle_offset'))
    ring =  eval(argv[-3]('Base','ring'))
    ring_offset = eval(argv[-3]('Base','ring_offset'))
    ringtime = eval(argv[-3]('Base','ringtime'))
    ringtime_offset = eval(argv[-3]('Base','ringtime_offset'))
    log = argv[-4]
    vmterm = argv[1][-2]
    term = argv[1][-1]
    voice_init(term)  
    
    if argv[0] in (0,2,4,6):vmport=(1,2)
    else:vmport=(3,4) 
    #Checkhook(term,vmterm,vmport,log) 
    cpkdata=[]
    for port in vmport:
        for ohm in ('min','max'):
            cpkdata.append(LoopCurrent(port,vmterm,ohm,log,loopc,loopc_offset))  
            #lWaitCmdTerm(vmterm,'ring %s 1'%port,'ring',10)
         
    for port in vmport:
        cpkdata.append(IdleStateVoltage(port,vmterm,log,idle,idle_offset))       

    for port in vmport:    
        cpkdata.append(RingSource(term,vmterm,port,log,ring,ring_offset,ringtime,ringtime_offset))
    if insertcpk:
       cpkdatas={}
       for cpk in cpkdata:
           for key in cpk:
               cpkdatas[key]=cpk[key] 
       if not InsertCPK_DB(mac,pn,'VOICE',cpkdatas):
          raise Except("ErrorCode(0005):Insert CPK data to db failed")   
    #DtmfSource(term,vmterm,vmport[0],log)  
    for i in range(1): 
        Checkhook(term,vmterm,vmport,log)
    #lWaitCmdTerm(term,"exit","",5,1) ### 10/29 add
    #time.sleep(25)                   ### 10/29 add
    #lWaitCmdTerm(term,"waitboot","Menu>",15,2) ### 10/29 add
    argv[-4]('Voice Test Pass',2)  

def Voicefunction(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    #insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    loopc = eval(argv[-3]('Base','loopc'))
    loopc_offset = eval(argv[-3]('Base','loopc_offset'))
    idle = eval(argv[-3]('Base','idle'))
    idle_offset = eval(argv[-3]('Base','idle_offset'))
    ring =  eval(argv[-3]('Base','ring'))
    ring_offset = eval(argv[-3]('Base','ring_offset'))
    ringtime = eval(argv[-3]('Base','ringtime'))
    ringtime_offset = eval(argv[-3]('Base','ringtime_offset'))
    log = argv[-4]
    vmterm = argv[1][3]
    term = argv[1][-1]
    voice_init(term)  
    
    if argv[0] in (0,2,4,6):vmport=(1,2)
    else:vmport=(3,4) 
    #Checkhook(term,vmterm,vmport,log) 
    cpkdata=[]
    
    for i in xrange(1):
        s_time=time.time()
        #log("======================= 'Test Index: %s'====================================="%i,2)
        #log('HUB4 voice loop test cont :%s'%i)
        #try: 
        #for port in vmport:
            #for ohm in ('min','max'):
                #cpkdata.append(LoopCurrent(port,term,vmterm,ohm,log,loopc,loopc_offset))                  
        #DtmfSource(term,vmterm,vmport[0],log)  
        
        for ohm in ('min','max'):
            for port in vmport:
                cpkdata.append(LoopCurrent(port,term,vmterm,ohm,log,loopc,loopc_offset))
            if ohm=="min":DtmfSource(term,vmterm,vmport[0],log)  
        
        for port in vmport:
            cpkdata.append(IdleStateVoltage(port,vmterm,log,idle,idle_offset))
        
        for port in vmport:    
            cpkdata.append(RingSource(term,vmterm,port,log,ring,ring_offset,ringtime,ringtime_offset))
        '''
        if insertcpk:
           cpkdatas={}
           for cpk in cpkdata:
               for key in cpk:
                   cpkdatas[key]=cpk[key] 
           if not InsertCPK_DB(mac,pn,'VOICE',cpkdatas):
              raise Except("ErrorCode(0005):Insert CPK data to db failed")
        '''
        
        #Checkhook(term,vmterm,vmport,log)
        log('total_time_cost=%dsec'%(time.time()-s_time))
        #lWaitCmdTerm(term,"exit","",5,1) ### 10/29 add
        #time.sleep(25)                   ### 10/29 add
        #lWaitCmdTerm(term,"waitboot","Menu>",15,2) ### 10/29 add
        #except: log('HUB4 voice loop test%s fail'%i); continue 
    argv[-4]('Voice Test Pass',2)  
    
