from testlibs.toolslib import *


def voice_init(term,log):
    #lWaitCmdTerm(term,"cli",">",5)
    #lWaitCmdTerm(term,"cable","cable>",5)  
    lWaitCmdTerm(term,"voice\n","MXP>",5,5) 
    #data = lWaitCmdTerm(term,"tiuhw ird 0 0x73 2\n","MXP>",5,5)
    #print data
    #log(data)
    #lWaitCmdTerm(term,ticliHead+"ca/voice","MXP>",5)
    lWaitCmdTerm(term,"prodtest enable on\n","MXP>",5,5) #enable the EMTA port

def Checkhook(term,vmterm,vmport,log):  
    for try_ in range(3):
        lWaitCmdTerm(vmterm,"dc %s min"%vmport[0],"dc",5)
        lWaitCmdTerm(vmterm,"dc %s min"%vmport[1],"dc",5) 
        data = lWaitCmdTerm(term,"prodtest gethookstatus 0",">",5,2) 
        if "offHook" not in data:   
           log("check telphone offhook status Failed")
           if try_ == 2:
              data = lWaitCmdTerm(term,"tiuhw ird 0 0x73 2\n","MXP>",5,5)
              log(data)
              raise Except('ErrorCode(0000): check telphone line 0 offhook status fail !')
           continue
        
        data = lWaitCmdTerm(term,"prodtest gethookstatus 1",">",5,2) 
        if "offHook" not in data:   
           log("check telphone offhook status Failed")
           
           if try_ == 2:
              data = lWaitCmdTerm(term,"tiuhw ird 0 0x73 2\n","MXP>",5,5)
              log(data)
              raise Except('ErrorCode(0000): check telphone line 1 offhook status fail !')   
           continue
           
        log("check telphone offhook status pass" )   
        break   
    
    for try_ in range(3):
        lWaitCmdTerm(vmterm,"ring %s 1"%vmport[0],"ring",8)
        lWaitCmdTerm(vmterm,"ring %s 1"%vmport[1],"ring",8)
        data = lWaitCmdTerm(term,"prodtest gethookstatus 0",">",5,2) 
        if "onHook" not in data:   
           if try_ == 2:
              data = lWaitCmdTerm(term,"tiuhw ird 0 0x73 2\n","MXP>",5,5)
              log(data)
              raise Except('ErrorCode(0000): check telphone line 0 onhook status fail !')
           continue
        
        data = lWaitCmdTerm(term,"prodtest gethookstatus 1",">",5,2) 
        if "onHook" not in data:   
           if try_ == 2:
              data = lWaitCmdTerm(term,"tiuhw ird 0 0x73 2\n","MXP>",5,5)
              log(data)
              raise Except('ErrorCode(0000): check telphone line 1 onhook status fail !')   
           continue
        
        log("check telphone onhook status pass" )   
        break     

def voice_ring_on(term,port,log):
    #if en=='on':
    #data = lWaitCmdTerm(term,"tiuhw ird 0 0x73 2\n","MXP>",5,5)
    #print data
    #log(data)
    
    if port == 1 or port == 3:    
      lWaitCmdTerm(term,"tiuhw set 1 hwcfg ringer sin 25 66 0","MXP>",8,3)    
      lWaitCmdTerm(term,"tiuhw wr 1 0x56 0x27","MXP>",8,3)
    else:
      lWaitCmdTerm(term,"tiuhw set 0 hwcfg ringer sin 25 66 0","MXP>",8,3)
      lWaitCmdTerm(term,"tiuhw wr 0 0x56 0x27","MXP>",8,3)
    
    
    #lWaitCmdTerm(term,"prodtest setring 0 %s"%en,"MXP>",5,2)
    #lWaitCmdTerm(term,"prodtest setring 1 %s"%en,"MXP>",5,2)  

def voice_ring_off(term,port):
    #if en=='on':
       #lWaitCmdTerm(term,"tiuhw set 0 hwcfg ringer sin 25 66 0","MXP>",5)
       #lWaitCmdTerm(term,"tiuhw set 1 hwcfg ringer sin 25 66 0","MXP>",5)
    
    if port == 1 or port == 3: lWaitCmdTerm(term,"tiuhw wr 1 0x56 0x2b","MXP>",5,3)
    else: lWaitCmdTerm(term,"tiuhw wr 0 0x56 0x2b","MXP>",5,3)
    
    
    
def exit_voice(term):
    lWaitCmdTerm(term,"prodtest enable off","MXP>",5,3) #disable the EMTA port  
    #lWaitCmdTerm(term,"exit","cable>",5)
 
def LoopCurrent(vmport,vmterm,ohm,log,loopc,loopc_offset)  :
    #ohm = max > ohm = 1.4k
    #ohm = min > ohm = 300
    flag = 0
    cpkdata={}
    if vmport in (1,3):line=0
    else:line=1

    result=0
    if ohm == 'max': flag = 1

    for try_ in range(10):
        r=lWaitCmdTerm(vmterm,'dc %s %s'%(vmport,ohm),'dc',5,3)
        if "Failed to read voltage" in r:
           for i in range(3):
               lWaitCmdTerm(vmterm,'dc %s %s'%(vmport,ohm),'dc',5,3)
        r=lWaitCmdTerm(vmterm,'dc %s %s'%(vmport,ohm),'dc',5,3)
        r=r.split('\t')[-1]
        print r
        try:
           r=float(r.split('mA')[0])
        except:
           if try_==9: raise Except('ErrorCode(101016):Loop current line:%s ohm:%s read failure'%(line,ohm))
           continue   
        if r <= loopc[flag] + loopc_offset[flag] and  r >= loopc[flag] - loopc_offset[flag]:
              result=1
              break 

    msg="Loop Current mode line %d LENTHohm state %s boost (mA): %3.2f (%.2f ~ %.2f)"%(line,ohm,r,loopc[flag] - loopc_offset[flag],loopc[flag] + loopc_offset[flag])
    #msg="Loop Current mode line %d LENTHohm state %s boost (mA): %3.2f"%(line,ohm,r)
    #message='%s,2,0,%s'%(id,msg)
    #SendData(message,log)
    #cpkdata['LoopCurrent_Line_%s_%s'%(line,ohm)]=(loopc[flag] - loopc_offset[flag],loopc[flag] + loopc_offset[flag],r)
    log('%s'%msg)
    if not result :
       raise Except('ErrorCode(101016):Loop current line:%s ohm:%s boost: %3.2f mA (%.2f ~ %.2f)'%(line,ohm,r,loopc[flag] - loopc_offset[flag],loopc[flag] + loopc_offset[flag]))
    return cpkdata

def IdleStateVoltage(vmport,vmterm,log,idle,idle_offset):
    if vmport in (1,3):line=0
    else:line=1
    result = 0
    cpkdata={}
    for try_ in range(5):
        r=lWaitCmdTerm(vmterm,'dc %s none'%vmport,'dc',5).split('\t')[-1]
        if "Failed to read voltage" in r:
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
    #msg="Idle Voltage mode line %d (V): %3.2f"%(line,r)
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
    retryflag=0
    cpkdata={}
    t = v = 0
    test_fail = 0
    for try_ in range(5):
        # Ring 1 REN
        lWaitCmdTerm(vmterm,'ring %s 1'%vmport,'ring',10)
        voice_ring_on(term,vmport,log)
        #voice_ring_off(term,vmport)
        #time.sleep(0.5)
        for i in range(3):
            time.sleep(0.5)
            r1=lWaitCmdTerm(vmterm,'ring %s 1'%vmport,'ring',10).split('\t')[-1]
            if 'Out of range!' in r1:
               r1=lWaitCmdTerm(vmterm,'ring %s 1'%vmport,'ring',10).split('\t')[-1]
            #r1=lWaitCmdTerm(vmterm,'ring %s 1'%vmport,'ring',10).split('\t')[-1]
            if 'No ring signal' not in r1:
                t=float(r1.split('ms')[0])
                v=float(r1.split(',')[-1].split('V')[0])
                if 58>= v >= 53: 
                   msg="Ring source mode line %d 1REN voltage(V): %3.2f"%(line,v)
                   #log(msg)
                   retryflag=0 
                   break
                else:
                   retryflag=1 
                   if try_ == 4: 
                      msg="Ring source mode line %d 1REN voltage(V): %3.2f"%(line,v)
                      #log(msg)
            else:
               #log('###############################')
               #log('Check DUT No ring signal!')
               retryflag=1
               
        if retryflag: continue
        else: voice_ring_off(term,vmport); break
    
    for try_ in range(5):
        # Ring 1 REN
        lWaitCmdTerm(vmterm,'ring %s 4'%vmport,'ring',10)
        voice_ring_on(term,vmport,log)
        #time.sleep(0.5)
        for i in range(3):
           time.sleep(0.5)
           r5=lWaitCmdTerm(vmterm,'ring %s 4'%vmport,'ring',10).split('\t')[-1]        
           #try:
           #t=float(r1.split('ms')[0])
           #v=float(r1.split(',')[-1].split('V')[0])
           v5=float(r5.split('V')[0])
           if abs(v-v5)<=5: retryflag=0; break 
           else: 
              retryflag=1
              if try_ == 4:
                 msg="Ring source mode line %d 5REN voltage(V): %3.2f"%(line,v5)
                 #log(msg)
                 
           #except:
           #   if try_==4: raise Except('ErrorCode(101018):Ring Source line:%s read failure'%line)
           #   voice_ring_off(term)
           #    continue 
           #if (t <=ringtime+ringtime_offset) and (t >=ringtime-ringtime_offset) and (v <=ring[0]+ring_offset[0]) and (v5 >=ring[1]-ring_offset[1]) and (v5 <=ring[1]+ring_offset[1]) and (v5 >=ring[1]-ring_offset[1]) :
           #   result = 1
           #   break
        if retryflag: continue
        else: break
    msg="Ring source mode line %d time(ms): %s (%.2f ~ %.2f)"%(line,t,ringtime-ringtime_offset,ringtime+ringtime_offset)
    #msg="Ring source mode line %d time(ms): %s"%(line,t)
    log(msg)
    #cpkdata['Ring_source_line_%d_time'%line]=(ringtime-ringtime_offset,ringtime+ringtime_offset,t)
    msg="Ring source mode line %d 1REN voltage(V): %3.2f (%.2f ~ %.2f)"%(line,v,ring[0]-ring_offset[0],ring[0]+ring_offset[0])
    #msg="Ring source mode line %d 1REN voltage(V): %3.2f"%(line,v)
    log(msg)
    #cpkdata['Ring_source_line_%d_1REN'%line]=(ring[0]-ring_offset[0],ring[0]+ring_offset[0],v)
    msg="Ring source mode line %d 5REN voltage(V): %3.2f (%.2f ~ %.2f)"%(line,v5,ring[1]-ring_offset[1],ring[1]+ring_offset[1])
    #msg="Ring source mode line %d 5REN voltage(V): %3.2f"%(line,v5)
    log(msg)
    #cpkdata['Ring_source_line_%d_5REN'%line]=(ring[1]-ring_offset[1],ring[1]+ring_offset[1],v5)
    if retryflag:
       raise Except('ErrorCode(101018):Line %d Ring Test: 1REN:%3.2f V(%.2f ~ %.2f) 5REN:%3.2f V(%.2f ~ %.2f) time: %3.2f(%.2f ~ %.2f)'%(line,v,ring[0]-ring_offset[0],ring[0]+ring_offset[0],v5,ring[1]-ring_offset[1],ring[1]+ring_offset[1],t,ringtime-ringtime_offset,ringtime+ringtime_offset))
    voice_ring_off(term,vmport) 
    #return cpkdata    

def DtmfSource(term,vmterm,vmport,log):
    result=0
    #message='%s,2,1,DTMF Source Test '
    #SendData(message,log)
    for try_ in range(5):
        lWaitCmdTerm(vmterm,'dtmf 1 %s %s'%(vmport,vmport+1),'dtmf',10)
        data=lWaitCmdTerm(term,'prodtest setport2portxc 0 1 on','>',25)
        if 'Can not' in data:
           if try_== 4 :
              raise Except('ErrorCode(405061):Xconnect set faiure')
              continue
        tone1=lWaitCmdTerm(vmterm,'dtmf 8 %s %s'%(vmport,vmport+1),'dtmf',10).split('\t')[-1].strip()
        tone2=lWaitCmdTerm(vmterm,'dtmf 9 %s %s'%(vmport+1,vmport),'dtmf',10).split('\t')[-1].strip()
        if '8' in tone1 and '9' in tone2:
           result = 1
           break
    log('Dtmf Source line 0: %s (8) , line 1: %s (9)'%(tone1,tone2))
    if not result:
       raise Except('ErrorCode(405061):DTMF Source Failure') 


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
    #voice_init(term)  
    if argv[0] in (0,2,4,6):vmport=(1,2)
    else:vmport=(3,4) 
    #Checkhook(term,vmterm,vmport,log) 
    cpkdata=[]
 
    for i in range(1): 
        #log("======================= 'Test Index: %s'====================================="%i,2)
        log('HUB4 voice loop test cont :%s'%i)
        voice_init(term,log)
        for port in vmport:
            for ohm in ('min','max'):
                cpkdata.append(LoopCurrent(port,vmterm,ohm,log,loopc,loopc_offset))  
                #lWaitCmdTerm(vmterm,'ring %s 1'%port,'ring',10)
             
        for port in vmport:
            cpkdata.append(IdleStateVoltage(port,vmterm,log,idle,idle_offset))       
    
        for port in vmport:    
            cpkdata.append(RingSource(term,vmterm,port,log,ring,ring_offset,ringtime,ringtime_offset))
        '''if insertcpk:
           cpkdatas={}
           for cpk in cpkdata:
               for key in cpk:
                   cpkdatas[key]=cpk[key] 
           if not InsertCPK_DB(mac,pn,'VOICE',cpkdatas):
              raise Except("ErrorCode(0005):Insert CPK data to db failed")'''   
        DtmfSource(term,vmterm,vmport[0],log)  
        for i in range(1): 
            Checkhook(term,vmterm,vmport,log)
        #lWaitCmdTerm(term,chr(0x03),'nu>',8,1)
        #term<< 'reboot'
        #time.sleep(120)
        #lWaitCmdTerm(term,'qu','#',5)
        #lWaitCmdTerm(term,'cli','nu>',8,3)
        #log('DUT reset pass',2)
    argv[-4]('Voice Test Pass',2)  
        
        
