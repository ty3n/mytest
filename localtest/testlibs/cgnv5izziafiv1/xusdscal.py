from toolslib_local import *
import odbc,pyodbc

def ConfirmM261CalInfo(data,FreqCompC0,FreqCompC0_offset,FreqCompC2,FreqCompC2_offset):
    try:
        message=''
        cpkdata={}
        #FreqComp_FC_list = [140000000,164000000,452000000,660000000,930000000]
        #FreqComp_FC_list = [212000000,452000000,660000000,930000000]
        FreqComp_FC_list = []
        FreqComp0_C0_list = []
        FreqComp0_C2_list = []
        FreqComp1_C0_list = []
        FreqComp1_C2_list = []
        fail = 0
        FreqComp0 = data.split("% FreqComp[0]")[1].split("% FreqComp[1]")[0]
        FreqComp1 = data.split("% FreqComp[1]")[1].split("% TiltComp[0]")[0]
        
        for i in FreqComp0.splitlines():
            if i.find("96000000")>=0:
                FreqComp0_C0_list.append(float(i.split()[1]))
                FreqComp0_C2_list.append(float(i.split()[3]))
                FreqComp_FC_list.append(int(i.split()[4]))
                
        for i in FreqComp1.splitlines():
            if i.find("96000000")>=0:
                FreqComp1_C0_list.append(float(i.split()[1]))
                FreqComp1_C2_list.append(float(i.split()[3]))
      
        
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[0] F_C :%d ,C0: %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp0_C0_list[j],
                                                             FreqCompC0[j]-FreqCompC0_offset[j],
                                                             FreqCompC0[j]+FreqCompC0_offset[j])
            if abs(FreqComp0_C0_list[j] - FreqCompC0[j]) > FreqCompC0_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C0'%FreqComp_FC_list[j]]=(FreqCompC0[j]-FreqCompC0_offset[j],FreqCompC0[j]+FreqCompC0_offset[j],FreqComp0_C0_list[j])
            #SendData(message,log)     
    
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[0] F_C :%d ,C2: %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp0_C2_list[j],
                                                             FreqCompC2[j]-FreqCompC2_offset[j],
                                                             FreqCompC2[j]+FreqCompC2_offset[j])
            if abs(FreqComp0_C2_list[j] - FreqCompC2[j]) > FreqCompC2_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C2'%FreqComp_FC_list[j]]=(FreqCompC2[j]-FreqCompC2_offset[j],FreqCompC2[j]+FreqCompC2_offset[j],FreqComp0_C2_list[j])
            #message='%s,2,0,%s'%(id,msg)
            #SendData(message,log) 
        
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[1] F_C :%d ,C0:  %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp1_C0_list[j],
                                                             FreqCompC0[j]-FreqCompC0_offset[j],
                                                             FreqCompC0[j]+FreqCompC0_offset[j])
            if abs(FreqComp1_C0_list[j] - FreqCompC0[j]) > FreqCompC0_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C0'%FreqComp_FC_list[j]]=(FreqCompC0[j]-FreqCompC0_offset[j],
                                                                  FreqCompC0[j]+FreqCompC0_offset[j],
                                                                  FreqComp1_C0_list[j])
                                                            
            #message='%s,2,0,%s'%(id,msg)
            #SendData(message,log)       
        
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[1] F_C :%d ,C2:  %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp1_C2_list[j],
                                                             FreqCompC2[j]-FreqCompC2_offset[j],
                                                             FreqCompC2[j]+FreqCompC2_offset[j])
            if abs(FreqComp1_C2_list[j] - FreqCompC2[j]) > FreqCompC2_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C2'%FreqComp_FC_list[j]]=(FreqCompC2[j]-FreqCompC2_offset[j],
                                                                  FreqCompC2[j]+FreqCompC2_offset[j],
                                                                  FreqComp1_C2_list[j])
                                                            
            #message='%s,2,0,%s'%(id,msg)
            #SendData(message,log) 
    except:
        fail=10 
    #print cpk_data      
    return fail,message,cpkdata
    #if fail > 0:raise Except("Fail: DSCal M261CalInfo")
    
def ConfirmIFVGA(data,Back_Off,Back_Off_IF_Reg,Back_Off_IF_Reg_offset,log,cpkdata)  :
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    IF_Reg = []
    f = 0
    #print data.splitlines()
    for i in data.splitlines():
      if i.find(". Back-Off =")>=0:                
          IF_Reg.append(int(i.split('IF_Reg =')[1].strip()))     
    for j in range(len(Back_Off)):
        msg = "Back-Off = %d, IF_Reg = %d (%d ~ %d)"%(Back_Off[j],IF_Reg[j],
                                                         Back_Off_IF_Reg[j]-Back_Off_IF_Reg_offset[j],
                                                         Back_Off_IF_Reg[j]+Back_Off_IF_Reg_offset[j])
        if abs(IF_Reg[j] - Back_Off_IF_Reg[j]) > Back_Off_IF_Reg_offset[j]:
            f= f+1
        print msg
        cpkdata[0]['Back_Off_%d_IF_Reg'%Back_Off[j]]=( Back_Off_IF_Reg[j]-Back_Off_IF_Reg_offset[j],
                                                       Back_Off_IF_Reg[j]+Back_Off_IF_Reg_offset[j],
                                                       IF_Reg[j])
        log(msg,2)
    if f > 0:raise Except("ErrorCode(108065): IF VGA Calibration") 

def ConfirmGCDNC(data,GC_DNC_code,GC_DNC_IF_AGC,GC_DNC_IF_AGC_offset,log,cpkdata):
    IF_AGC = []
    f = 0
    for i in data.splitlines():
      if i.find("GC_DNC_code")>=0:
          IF_AGC.append(int(i.split('IF_AGC =')[1].strip()))
    for j in range(len(GC_DNC_code)):
        msg = "GC_DNC_code = %d, IF_AGC = %d (%d ~ %d)"%(GC_DNC_code[j],IF_AGC[j],
                                                         GC_DNC_IF_AGC[j]-GC_DNC_IF_AGC_offset[j],
                                                         GC_DNC_IF_AGC[j]+GC_DNC_IF_AGC_offset[j])
        if abs(IF_AGC[j] - GC_DNC_IF_AGC[j]) > GC_DNC_IF_AGC_offset[j]:
            SetPatternColor(0)
            f= f+1
        print msg
        cpkdata[0]['GC_DNC_Code_%d_IF_AGC'%GC_DNC_code[j]]=(GC_DNC_IF_AGC[j]-GC_DNC_IF_AGC_offset[j],
                                             GC_DNC_IF_AGC[j]+GC_DNC_IF_AGC_offset[j],
                                             IF_AGC[j])
        log(msg,2)
    if f > 0:raise Except("ErrorCode(108065): DSCal GC_DNC_IF_AGC")


def MT2170DSCalibration(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    log = argv[-4]
    ds_freqs = eval(argv[-3]('Base','ds_freqs'))
    bandwidth = argv[-3]('Base','BandWidth')
    basepower = argv[-3]('Base','BasePower')
    ns_offset = float(argv[-3]('Base','ns_offset'))
    gcATTN =  eval(argv[-3]('Base','gcATTN'))
    Back_Off = eval(argv[-3]('Base','Back_Off'))
    Back_Off_IF_Reg = eval(argv[-3]('Base','Back_Off_IF_Reg'))
    Back_Off_IF_Reg_offset = eval(argv[-3]('Base','Back_Off_IF_Reg_offset'))
    GC_DNC_code = eval(argv[-3]('Base','GC_DNC_code'))
    GC_DNC_IF_AGC = eval(argv[-3]('Base','GC_DNC_IF_AGC'))
    GC_DNC_IF_AGC_offset = eval(argv[-3]('Base','GC_DNC_IF_AGC_offset'))
    
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    
    lWaitCmdTerm(argv[1][1],"dsa %s"%(int(coarse)+int(ns_offset)),"OK",5,2)
    lWaitCmdTerm(argv[1][1],"dsa %s %s"%(port,int(fine)+int((ns_offset-int(ns_offset))/0.25)),"OK",5,2)

    lWaitCmdTerm(argv[1][-1],"gaincontrol %d 50 127"%gcATTN,">",5)
    data = lWaitCmdTerm(argv[1][-1],"sfreq %s"%ds_freq,">",5,2)
    #print data
    CheckInputData(data,ds_freq)
    data = lWaitCmdTerm(argv[1][-1],"spow %s"%ds_power,">",5)
    #print data
    CheckInputData(data,ds_power)
    argv[-4]('CB SN : %s\tcoarse: %s\tfine: %s'%(sn,coarse,fine))
    argv[-4]('freqs : %s \npowers: %s '%(ds_freq,ds_power))
    
    data = lWaitCmdTerm(argv[1][-1],"runc","Anti Alias Filter Calibration finished.",70)
    if "Channel Calibration finished" not in data:
              raise Except("ErrorCode(108065):Ds calibration Error!!")
    data = data + lWaitCmdTerm(argv[1][-1],"","D/S Calibration Finished",100)
    cpkdata={}       
    ConfirmIFVGA(data,Back_Off,Back_Off_IF_Reg,Back_Off_IF_Reg_offset,log,[cpkdata])   
    ConfirmGCDNC(data,GC_DNC_code,GC_DNC_IF_AGC,GC_DNC_IF_AGC_offset,log,[cpkdata])
    
    if "IF_Reg = 511"  in data:
        raise Except("ErrorCode(108065): DS Calibration IF_Reg = 511")
    if "IF_AGC = 511" in data:
        raise Except("ErrorCode(108065): DS Calibration IF_AGC = 511") 
               
    argv[-4]('Downstream calibration OK',2)    
    if insertcpk:
       if not InsertCPK_DB(mac,pn,'DS_CALIBRATION',cpkdata):
          raise Except("ErrorCode(0005):Insert CPK data to db failed") 
    
def USCalibration(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    freqs = eval(argv[-3]('Base','us_freqs'))
    us_average = eval(argv[-3]('Base','us_average'))
    us_offset =  eval(argv[-3]('Base','us_offset'))
    powerdetector_gain_offset = float(argv[-3]('Base','powerdetector_gain_offset').strip())
    port = argv[0]+1
    if port >4 : port -= 4
    for i in range(4):
        lWaitCmdTerm(argv[1][-1],"upstream %s 0"%i,">",5,2)
    lWaitCmdTerm(argv[1][-1],"scmf 3",">",5,2)
    lWaitCmdTerm(argv[1][-1],"er 0",">",5,2)
    lWaitCmdTerm(argv[1][-1],"freq 0 20",">",5,2)
    lWaitCmdTerm(argv[1][-1],"modulation 0 1",">",5,2)
    lWaitCmdTerm(argv[1][-1],"symb 0 1",">",10,2)
    lWaitCmdTerm(argv[1][-1],"cont 0 1",">",5,2)
    lWaitCmdTerm(argv[1][-1],"upstream 0 1",">",5,2)
    lWaitCmdTerm(argv[1][-1],"sdattn 0 0",">",5,2)
    lWaitCmdTerm(argv[1][-1],"sapdelta 0",">",5,2)
    lWaitCmdTerm(argv[1][-1],"uf",">",5,2)   
    lWaitCmdTerm(argv[1][-1],"er 2",">",5,2)
    a=0
    cpkdata={}
    for f in freqs:
        for try_ in range(6):
            lWaitCmdTerm(argv[1][-1],"freq 0 %f"%f,">",5,2)
            lWaitCmdTerm(argv[1][-1],"gain 35",">",5,3)
            r= lWaitCmdTerm(argv[1][1],'pwr %s'%port,'pwr',5,2).split('\t')[-1]
            try:
               print r
               r=float(r.split('dBmV')[0])+powerdetector_gain_offset   
            except:
               if try_==5:raise Except("ErrorCode(E00136):Upstream Read Power Failure") 
               continue
            msg = "Freq=%.1f measure=%.2f (%.2f ~ %.2f)"%(f,r,us_average[a]-us_offset[a],us_average[a]+us_offset[a])
            if r<us_average[a]-us_offset[a] or r>us_average[a]+us_offset[a]:
               if try_==3:raise Except("ErrorCode(E00136):"+msg)
            else:break
        cpkdata['Freq_%s_MHz'%'_'.join(str(f).split('.'))]=(us_average[a]-us_offset[a],us_average[a]+us_offset[a],r)
        a+=1
        lWaitCmdTerm(argv[1][-1],"sfreq %.1f %.2f"%(f,r),">",5,3)  
        argv[-4](msg)      
    #lWaitCmdTerm(argv[1][-1],"uf",">",5,2)
    # check save table Number of Frequencies=17
    for i in range(5):
        lWaitCmdTerm(argv[1][-1],"uf",">",8,2)
        data=lWaitCmdTerm(argv[1][-1],"p 1",">",5,2)
        if data.split('ies=')[-1].split()[0]<> str(len(freqs)):
           if i==4:raise Except('ErrorCode(E00136):save us table index error %s (%s)'%(data.split('ies=')[-1].split()[0],len(freqs)))
        else:break
    '''
    data=lWaitCmdTerm(argv[1][-1],"p 1",">",5,2)
    if data.split('ies=')[-1].split()[0]<> str(len(freqs)):
       raise Except('ErrorCode(E00136):save us table index error %s (%s)'%(data.split('ies=')[-1].split()[0],len(freqs)))
    '''
    argv[-4]('US Calibration Test Pass',2)
    if insertcpk:
       if not InsertCPK_DB(mac,pn,'US_CALIBRATION',cpkdata):
          raise Except("ErrorCode(0005):Insert CPK data to db failed")  
       

def GetDsCalTable(type_,port,sn,ds_freqs,bandwidth,basepower):
    '''
       Local : read local host config file
       Remote : read remote server database
    '''
    freqs = powers =''
    cattn = fattn = 0
    if type_=='LOCAL':
       cattn,fattn = GetAttnValue("NoiseSource_%sdbmv_%sMHz_%s_%s"%(float(basepower),int(bandwidth),sn,port),"C:\\Cal")
       gSA_offset=lReadEquipmentOffsetTable("NoiseSource_%sdbmv_%sMHz_%s_%s"%(float(basepower),int(bandwidth),sn,port),"C:\\Cal")
       for freq in ds_freqs:
           powers= powers + '%0.2f '%lDownstreamFrequencyPower(gSA_offset,freq)
       powers=powers.strip()
       if len(powers.split())<>len(ds_freqs):
           raise Except("ErrorCode(0003):Read Ds Table Falied")
       for freq in ds_freqs:
           freqs = freqs + '%s '%freq
       freqs=freqs.strip()       
    else:
       #logserver = '172.28.10.52'
       #ipconfig = os.popen('ipconfig').read()
       #if '172.28.209' in ipconfig:logserver = '172.28.209.253'
       #if '172.28.206' in ipconfig:logserver = '172.28.206.253'  
       #db = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(logserver,'test','test','test')) 
       db = odbc.odbc("TESTlog/TEST/test")
       cursor = db.cursor()
       sql="select module_ID,Freqs,Attn1_01dB_1,Attn1_01dB_2,Attn1_01dB_3,Attn1_01dB_4,powers_1,\
powers_2,powers_3,powers_4,Attn2_1dB from NoiseSource_table where (module_ID='%s') and (BasePower='%s') \
and (BandSpan='%s') order by DateTime DESC"%(sn,float(basepower),int(bandwidth))
       cursor.execute(sql)
       data = cursor.fetchone()
       print data
       if data:
          cattn = data[10]
          fattn = data[port+1]
          freqs_ = data[1].split()
          powers_ = data[port+5].split()
          freqs=powers=''
          
          power540 = powers_[freqs_.index(str('540'))] 
          if abs(float(power540) - float(basepower)) > 1:
             raise Except("ErrorCode(0003):Calibration basepower error!")          
          for freq in ds_freqs:
              if str(freq) not in  freqs_:raise Except("ErrorCode(0003):Not found freq %s value fo ds table"%freq)
              freqs +='%s '%freq
              powers +='%s '%powers_[freqs_.index(str(freq))] 
         
          freqs=freqs.strip()  
          powers=powers.strip()                    
       else:
          raise Except("ErrorCode(0003):Not found ds table")
       
    return (cattn,fattn,freqs,powers)


def ConfirmM261CalInfo(data,FreqCompC0,FreqCompC0_offset,FreqCompC2,FreqCompC2_offset):
    try:
        message=''
        cpkdata={}
        #FreqComp_FC_list = [140000000,164000000,452000000,660000000,930000000]
        #FreqComp_FC_list = [212000000,452000000,660000000,930000000]
        FreqComp_FC_list = []
        FreqComp0_C0_list = []
        FreqComp0_C2_list = []
        FreqComp1_C0_list = []
        FreqComp1_C2_list = []
        fail = 0
        FreqComp0 = data.split("% FreqComp[0]")[1].split("% FreqComp[1]")[0]
        FreqComp1 = data.split("% FreqComp[1]")[1].split("% TiltComp[0]")[0]
        
        for i in FreqComp0.splitlines():
            if i.find("96000000")>=0:
                FreqComp0_C0_list.append(float(i.split()[1]))
                FreqComp0_C2_list.append(float(i.split()[3]))
                FreqComp_FC_list.append(int(i.split()[4]))
                
        for i in FreqComp1.splitlines():
            if i.find("96000000")>=0:
                FreqComp1_C0_list.append(float(i.split()[1]))
                FreqComp1_C2_list.append(float(i.split()[3]))
      
        
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[0] F_C :%d ,C0: %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp0_C0_list[j],
                                                             FreqCompC0[j]-FreqCompC0_offset[j],
                                                             FreqCompC0[j]+FreqCompC0_offset[j])
            if abs(FreqComp0_C0_list[j] - FreqCompC0[j]) > FreqCompC0_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C0'%FreqComp_FC_list[j]]=(FreqCompC0[j]-FreqCompC0_offset[j],FreqCompC0[j]+FreqCompC0_offset[j],FreqComp0_C0_list[j])
            #SendData(message,log)     
    
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[0] F_C :%d ,C2: %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp0_C2_list[j],
                                                             FreqCompC2[j]-FreqCompC2_offset[j],
                                                             FreqCompC2[j]+FreqCompC2_offset[j])
            if abs(FreqComp0_C2_list[j] - FreqCompC2[j]) > FreqCompC2_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C2'%FreqComp_FC_list[j]]=(FreqCompC2[j]-FreqCompC2_offset[j],FreqCompC2[j]+FreqCompC2_offset[j],FreqComp0_C2_list[j])
            #message='%s,2,0,%s'%(id,msg)
            #SendData(message,log) 
        
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[1] F_C :%d ,C0:  %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp1_C0_list[j],
                                                             FreqCompC0[j]-FreqCompC0_offset[j],
                                                             FreqCompC0[j]+FreqCompC0_offset[j])
            if abs(FreqComp1_C0_list[j] - FreqCompC0[j]) > FreqCompC0_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C0'%FreqComp_FC_list[j]]=(FreqCompC0[j]-FreqCompC0_offset[j],
                                                                  FreqCompC0[j]+FreqCompC0_offset[j],
                                                                  FreqComp1_C0_list[j])
                                                            
            #message='%s,2,0,%s'%(id,msg)
            #SendData(message,log)       
        
        for j in range(len(FreqComp_FC_list)):
            msg = "FreqComp[1] F_C :%d ,C2:  %d (%d ~ %d)"%(FreqComp_FC_list[j],FreqComp1_C2_list[j],
                                                             FreqCompC2[j]-FreqCompC2_offset[j],
                                                             FreqCompC2[j]+FreqCompC2_offset[j])
            if abs(FreqComp1_C2_list[j] - FreqCompC2[j]) > FreqCompC2_offset[j]:
                fail= fail+1
            message=message+'\n\r'+msg
            cpkdata['F_C_%d_C2'%FreqComp_FC_list[j]]=(FreqCompC2[j]-FreqCompC2_offset[j],
                                                                  FreqCompC2[j]+FreqCompC2_offset[j],
                                                                  FreqComp1_C2_list[j])
                                                            
            #message='%s,2,0,%s'%(id,msg)
            #SendData(message,log) 
    except:
        fail=10 
    #print cpk_data      
    return fail,message,cpkdata
    #if fail > 0:raise Except("Fail: DSCal M261CalInfo")
    
def Mx261DSCalibration(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    ds_freqs = eval(argv[-3]('Base','ds_freqs'))
    bandwidth = argv[-3]('Base','BandWidth')
    basepower = argv[-3]('Base','BasePower')
    ns_offset = float(argv[-3]('Base','ns_offset'))
    gcATTN =  eval(argv[-3]('Base','gcATTN'))
    FreqCompC0 = eval(argv[-3]('Base','FreqCompC0'))
    FreqCompC0_offset = eval(argv[-3]('Base','FreqCompC0_offset'))
    FreqCompC2 = eval(argv[-3]('Base','FreqCompC2'))
    FreqCompC2_offset = eval(argv[-3]('Base','FreqCompC2_offset'))
    
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    
    lWaitCmdTerm(argv[1][1],"dsa %s"%(int(coarse)+int(ns_offset)),"OK",5,2)
    lWaitCmdTerm(argv[1][1],"dsa %s %s"%(port,int(fine)+int((ns_offset-int(ns_offset))/0.25)),"OK",5,2)

    lWaitCmdTerm(argv[1][-1],"gaincontrol %d 50 127"%gcATTN,">",5)
    
    data = lWaitCmdTerm(argv[1][-1],"ds_freq %s"%ds_freq,">",5,2)
    print data
    CheckInputData(data,ds_freq)
    data = lWaitCmdTerm(argv[1][-1],"spow %s"%ds_power,">",5)
    #print data
    CheckInputData(data,ds_power)
    argv[-4]('CB SN : %s\tcoarse: %s\tfine: %s'%(sn,coarse,fine))
    argv[-4]('freqs : %s \npowers: %s '%(ds_freq,ds_power))
    
    lWaitCmdTerm(argv[1][-1],"runc","D/S Calibration Finished",70)
    for i in range(8):
        data = lWaitCmdTerm(argv[1][-1],"printTunerCalInfo",">",10)
        result,msg,cpkdata= ConfirmM261CalInfo(data,FreqCompC0,FreqCompC0_offset,FreqCompC2,FreqCompC2_offset)
        if not result:
           argv[-4](msg)
           break
        if result<>10 or i==7:
           argv[-4](msg)
           raise Except("ErrorCode(108065):DSCal M261CalInfo")
    argv[-4]('Downstream calibration OK',2)     
    if insertcpk:
       if not InsertCPK_DB(mac,pn,'DS_CALIBRATION',cpkdata):
          raise Except("ErrorCode(0005):Insert CPK data to db failed")   

############20121129 add function ##############
def ConfirmIFVGA(data,Back_Off,Back_Off_IF_Reg,Back_Off_IF_Reg_offset,log,cpkdata)  :
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    IF_Reg = []
    f = 0
    #print data.splitlines()
    for i in data.splitlines():
      if i.find(". Back-Off =")>=0:                
          IF_Reg.append(int(i.split('IF_Reg =')[1].strip()))     
    for j in range(len(Back_Off)):
        msg = "Back-Off = %d, IF_Reg = %d (%d ~ %d)"%(Back_Off[j],IF_Reg[j],
                                                         Back_Off_IF_Reg[j]-Back_Off_IF_Reg_offset[j],
                                                         Back_Off_IF_Reg[j]+Back_Off_IF_Reg_offset[j])
        if abs(IF_Reg[j] - Back_Off_IF_Reg[j]) > Back_Off_IF_Reg_offset[j]:
            f= f+1
        print msg
        cpkdata[0]['Back_Off_%d_IF_Reg'%Back_Off[j]]=( Back_Off_IF_Reg[j]-Back_Off_IF_Reg_offset[j],
                                                       Back_Off_IF_Reg[j]+Back_Off_IF_Reg_offset[j],
                                                       IF_Reg[j])
        log(msg,2)
    if f > 0:raise Except("ErrorCode(108065): IF VGA Calibration") 

def ConfirmGCDNC(data,GC_DNC_code,GC_DNC_IF_AGC,GC_DNC_IF_AGC_offset,log,cpkdata):
    IF_AGC = []
    f = 0
    for i in data.splitlines():
      if i.find("GC_DNC_code")>=0:
          IF_AGC.append(int(i.split('IF_AGC =')[1].strip()))
    for j in range(len(GC_DNC_code)):
        msg = "GC_DNC_code = %d, IF_AGC = %d (%d ~ %d)"%(GC_DNC_code[j],IF_AGC[j],
                                                         GC_DNC_IF_AGC[j]-GC_DNC_IF_AGC_offset[j],
                                                         GC_DNC_IF_AGC[j]+GC_DNC_IF_AGC_offset[j])
        if abs(IF_AGC[j] - GC_DNC_IF_AGC[j]) > GC_DNC_IF_AGC_offset[j]:
            SetPatternColor(0)
            f= f+1
        print msg
        cpkdata[0]['GC_DNC_Code_%d_IF_AGC'%GC_DNC_code[j]]=(GC_DNC_IF_AGC[j]-GC_DNC_IF_AGC_offset[j],
                                             GC_DNC_IF_AGC[j]+GC_DNC_IF_AGC_offset[j],
                                             IF_AGC[j])
        log(msg,2)
    if f > 0:raise Except("ErrorCode(108065): DSCal GC_DNC_IF_AGC")

def Mx267DSCalibration_back(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    ds_freqs = eval(argv[-3]('Base','ds_freqs'))
    bandwidth = argv[-3]('Base','BandWidth')
    basepower = argv[-3]('Base','BasePower')
    ns_offset = float(argv[-3]('Base','ns_offset'))
    gcATTN =  eval(argv[-3]('Base','gcATTN'))
    TiltIndex = eval(argv[-3]('Base','TiltIndex'))
    TiltIndex_offset = eval(argv[-3]('Base','TiltIndex_offset'))
    log = argv[-4]
    
    #ds_freqs = []                 #20130424 define by James Huang
    #for i in range(108,1002,48):
        #ds_freqs.append(i)
    #ds_freqs.append(1000)
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    
    for k in range(3):
        log('%s'%k)
        lWaitCmdTerm(argv[1][1],"dsa %s"%(int(coarse)+int(ns_offset)),"OK",5,2)
        lWaitCmdTerm(argv[1][1],"dsa %s %s"%(port,int(fine)+int((ns_offset-int(ns_offset))/0.25)),"OK",5,2)
    
        lWaitCmdTerm(argv[1][-1],"gaincontrol %d 50 127"%gcATTN,">",8,3)
        
        lWaitCmdTerm(argv[1][-1],"sfreq %s"%ds_freq,"Downstream_Calibration>",3)
        lWaitCmdTerm(argv[1][-1],"spow %s"%ds_power,"Downstream_Calibration>",3)
        
        if k == 0:
           argv[-4]('CB SN : %s\tcoarse: %s\tfine: %s'%(sn,coarse,fine))
           argv[-4]('freqs : %s \npowers: %s '%(ds_freq,ds_power))
        
        print "Start to run DS Calibration"
        lWaitCmdTerm(argv[1][-1],"runc","D/S Calibration Finished",30)
        data = lWaitCmdTerm(argv[1][-1],"printTune","Downstream_Calibration>",10)
    
        if ConfirmM267CalInfo(k,data,TiltIndex,TiltIndex_offset,log):break
        #lWaitCmdTerm(argv[1][1],"exit","Calibration>",5)
        #lWaitCmdTerm(argv[1][1],"exit","Production>",3)
        #lWaitCmdTerm(argv[1][1],"exit","docsis>",3)
        #lWaitCmdTerm(argv[1][1],"exit",">",3)


def InProduction(term):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut
    '''
    lWaitCmdTerm(term,'top','nu',5,2)
    lWaitCmdTerm(term,'doc','is>',5,3)
    
    for i in range(10):
        term << "Prod"
        time.sleep(0.5)
        data = lWaitCmdTerm(term,'stProd2new','ion>',8)
        if "Production>" in data:break
        if i == 9:raise Except("Input Password error")

def Mx267DSCalibration_back(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    ds_freqs = eval(argv[-3]('Base','ds_freqs'))
    bandwidth = argv[-3]('Base','BandWidth')
    basepower = argv[-3]('Base','BasePower')
    ns_offset = float(argv[-3]('Base','ns_offset'))
    gcATTN =  eval(argv[-3]('Base','gcATTN'))
    TiltIndex = eval(argv[-3]('Base','TiltIndex'))
    TiltIndex_offset = eval(argv[-3]('Base','TiltIndex_offset'))
    log = argv[-4]
    c_port = argv[0] #only CGN3-ROG
    if argv[0] > 3 : c_port = argv[0] - 4  #only CGN3-ROG
        
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    
    for k in range(3):
        log('%s'%k)
        lWaitCmdTerm(argv[1][1],"dsa %s"%(int(coarse)+int(ns_offset)),"OK",5,2)
        lWaitCmdTerm(argv[1][1],"dsa %s %s"%(port,int(fine)+int((ns_offset-int(ns_offset))/0.25)),"OK",5,2)
    
        #lWaitCmdTerm(argv[1][-1],"gaincontrol %d 50 127"%gcATTN,">",5,2)
        
        lWaitCmdTerm(argv[1][-1],"sfreq %s"%ds_freq,"Downstream_Calibration>",3)
        lWaitCmdTerm(argv[1][-1],"spow %s"%ds_power,"Downstream_Calibration>",3)
        
        if k == 0:
           argv[-4]('CB SN : %s\tcoarse: %s\tfine: %s'%(sn,coarse,fine))
           argv[-4]('freqs : %s \npowers: %s '%(ds_freq,ds_power))
        
        print "Start to run DS Calibration"
        lWaitCmdTerm(argv[1][-1],"runc","D/S Calibration Finished",30)
        ## Set Default to Calibration # 
        lWaitCmdTerm(argv[1][-1],"exit","#",8,1) 
        lWaitCmdTerm(argv[1][0],'uartd close %s'%c_port,'ok',5)
        time.sleep(40)        
        lWaitCmdTerm(argv[1][0],'uartd open %s 0'%c_port,'ok',5)
        lWaitCmdTerm(argv[1][-1],"quit","#",5,2)        
        lWaitCmdTerm(argv[1][-1],"cli","nu>",5,2)        
        lWaitCmdTerm(argv[1][-1],"logger","er>",5,2)        
        lWaitCmdTerm(argv[1][-1],"setDefault","er>",8,2)
        #lWaitCmdTerm(argv[1][-1],"AllModulesConfig 1 0","er>",5,2) #by Jason tell me      
        #lWaitCmdTerm(argv[1][-1],"ModuleConfig 1 51 1","er>",5,2)      
        #lWaitCmdTerm(argv[1][-1],"ComponentConfig 1 1","er>",5,2)           
        lWaitCmdTerm(argv[1][-1],"exit","nu>",8,1)        
        lWaitCmdTerm(argv[1][-1],"doc","sis>",5,2)
        #lWaitCmdTerm(argv[1][-1],"Production",":",8,2)  
        #lWaitCmdTerm(argv[1][-1],"stProd2new","ion>",8,2) 
        InProduction(term)
        lWaitCmdTerm(argv[1][-1],"Test","st>",5,2)        
        lWaitCmdTerm(argv[1][-1],"test","st>",5,2)        
        lWaitCmdTerm(argv[1][-1],"exit","ion>",8,1)        
        lWaitCmdTerm(argv[1][-1],"Calibration","ion>",5,2)  
        lWaitCmdTerm(argv[1][-1],"Downstream_Calibration","ion>",5,2)         
            
        data = lWaitCmdTerm(argv[1][-1],"printTune","Downstream_Calibration>",10)
    
        if ConfirmM267CalInfo(k,data,TiltIndex,TiltIndex_offset,log):break

def Mx267DSCalibration(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
         terms : ccu , cb , sw , vm ,dut 
    '''
    insertcpk = eval(argv[-3](argv[-2],'InsertCPK'))
    mac = argv[2][0]
    pn = argv[-3]('Base','PN')
    ds_freqs = eval(argv[-3]('Base','ds_freqs'))
    bandwidth = argv[-3]('Base','BandWidth')
    basepower = argv[-3]('Base','BasePower')
    ns_offset = float(argv[-3]('Base','ns_offset'))
    gcATTN =  eval(argv[-3]('Base','gcATTN'))
    TiltIndex = eval(argv[-3]('Base','TiltIndex'))
    TiltIndex_offset = eval(argv[-3]('Base','TiltIndex_offset'))
    log = argv[-4]
    c_port = argv[0] #only CGN3-ROG
    if argv[0] > 3 : c_port = argv[0] - 4  #only CGN3-ROG
        
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    
    table_type = argv[-3](argv[-2],'DSCalTable').upper()
    sn=lWaitCmdTerm(argv[1][1],'sn','sn',3,3).split()[-1]
    print "1111111111111"
    print sn
    port =argv[0]+1
    if port > 4 : port -= 4 
    data = GetDsCalTable(table_type,port,sn,ds_freqs,bandwidth,basepower)
    coarse,fine,ds_freq,ds_power = data
    cmd = '''
    top
    logger
    setDefault
    AllModulesConfig 1 0
    ModuleConfig 1 51 1
    ComponentConfig 1 1
    exit
    docsis
    Production
    Test
    testmode
    exit
    Calibration
    Downstream_Calibration
    sfreq 106 124 148 160 172 184 208 220 256 280 304 316 328 340 352 376 400 412 436 460 484 508 520 532 544 556 568 580 604 616 628 652 676 688 700 712 724 736 748 760 772 784 796 820 832 844 856 868 880 892 904 916 928 940 952 964 976 988 1000
    spow 20.38 21.39 20.58 19.67 18.74 18.18 17.75 17.61 18.48 18.62 17.47 16.84 16.08 15.73 15.58 16.11 16.72 17.13 17.07 16.02 14.40 13.79 14.07 14.66 15.31 15.85 16.22 16.46 15.85 15.05 14.47 14.13 14.58 14.96 15.25 14.64 13.04 14.23 14.64 14.16 13.94 13.62 13.63 13.74 13.88 14.04 14.09 14.14 14.32 13.89 13.17 12.54 11.98 11.77 11.76 11.79 11.81 11.23 11.61
    ''' 

    ############## old ################

    lWaitCmdTerm(argv[1][-1],"top","nu>",5,2)        
    lWaitCmdTerm(argv[1][-1],"logger","er>",5,2)        
    lWaitCmdTerm(argv[1][-1],"setDefault","er>",8,2)
    lWaitCmdTerm(argv[1][-1],"AllModulesConfig 1 0","er>",5,2) #by Jason tell me      
    lWaitCmdTerm(argv[1][-1],"ModuleConfig 1 51 1","er>",5,2)      
    lWaitCmdTerm(argv[1][-1],"ComponentConfig 1 1","er>",5,2)           
    lWaitCmdTerm(argv[1][-1],"exit","nu>",8,1)        
    lWaitCmdTerm(argv[1][-1],"doc","sis>",5,2)
    lWaitCmdTerm(argv[1][-1],"Production","ion>",8,2)  
    #lWaitCmdTerm(argv[1][-1],"D0nt4g3tme!","ion>",8,2) 
    lWaitCmdTerm(argv[1][-1],"Test","st>",8,2)        
    lWaitCmdTerm(argv[1][-1],"test","st>",15,2)        
    lWaitCmdTerm(argv[1][-1],"exit","ion>",8,1)        
    lWaitCmdTerm(argv[1][-1],"Calibration","ion>",5,2)  
    lWaitCmdTerm(argv[1][-1],"Downstream_Calibration","ion>",5,2)  
        
    dsf=dsp=""
    for freq in ds_freq.strip().split():
        dsf += freq + " "
    for pwr in ds_power.strip().split(): 
        dsp += str(float(pwr)) + " "
        
    ############## old ################
    for k in range(3):
        print "===============count : %s========================"%k
        lWaitCmdTerm(argv[1][1],"dsa %s"%(int(coarse)+int(ns_offset)),"OK",5,2)
        lWaitCmdTerm(argv[1][1],"dsa %s %s"%(port,int(fine)+int((ns_offset-int(ns_offset))/0.25)),"OK",5,2)    
        #lWaitCmdTerm(argv[1][-1],"gaincontrol %d 50 127"%gcATTN,">",5,2)       
        ##argv[1][-1]<< cmd
        ##time.sleep(3)
        ##print argv[1][-1].get()
        data = lWaitCmdTerm(argv[1][-1],"sfreq %s\n"%dsf,"Downstream_Calibration>",8,2)
        print data
        time.sleep(1)
        data = lWaitCmdTerm(argv[1][-1],"spow %s\n"%dsp,"Downstream_Calibration>",8)
        print data
        time.sleep(1)
        if k == 0:
           argv[-4]('CB SN : %s\tcoarse: %s\tfine: %s'%(sn,coarse,fine))
           argv[-4]('freqs : %s \npowers: %s '%(ds_freq,ds_power))
        
        print "Start to run DS Calibration"
        lWaitCmdTerm(argv[1][-1],"runc","D/S Calibration Finished",30)
        data = lWaitCmdTerm(argv[1][-1],"printTune","TiltIndex:3",20,2)
        print data
        #data = lWaitCmdTerm(argv[1][-1],"printTune","Downstream_Calibration>",20,2)
        if ConfirmM267CalInfo(k,data,TiltIndex,TiltIndex_offset,log):
            lWaitCmdTerm(argv[1][-1],'top',"nu>",5,2)
            lWaitCmdTerm(argv[1][-1],'logger',"logger>",5,2)
            lWaitCmdTerm(argv[1][-1],'AllComponentsConfig 0',"logger>",5,2)
            break


def ConfirmM267CalInfo(k,data,TiltIndex,TiltIndex_offset,log):
    test_fail = 0
    M267CalInfo = ''
    #Segment = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    Segment = [[0 for j in xrange(8)] for i in xrange(3)]
    for i in range(3):
        split_str = data.split('TiltIndex:%d'%i)[-1].split('TiltIndex:%d'%(i+1))[0]
        for j in split_str.splitlines():
            try:
                s_index = int(j.split('Segment:')[-1].split('| c2')[0])
                c0 = int(j.split('c0=')[-1].strip())
                Segment[i][s_index] = c0
            except:
                pass 
    for i in range(3):         
        for j in range(8):
            msg = 'Segment:%d c0= %d (%d ~ %d)'%(j,Segment[i][j],TiltIndex[i][j]-TiltIndex_offset[i][j],TiltIndex[i][j]+TiltIndex_offset[i][j])
            if abs(TiltIndex[i][j] - Segment[i][j]) > TiltIndex_offset[i][j]:
                test_fail+=1
                #log(msg)
            M267CalInfo = M267CalInfo + msg + "\r\n"
    #print '%s'%M267CalInfo
    if test_fail > 0:
       if k == 2:
          log(M267CalInfo)
          raise Except("Fail: DSCal M267CalInfo")
       return 0
    if test_fail == 0:
       log(M267CalInfo)
       return 1
   
    
 
