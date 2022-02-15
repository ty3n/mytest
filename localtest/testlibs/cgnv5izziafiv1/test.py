import sys, shutil, os, string,datetime,glob
import sys, shutil, os, string
import pyodbc,bz2,time,os,datetime,time

def getPK(mac):
    db = pyodbc.connect('DRIVER={SQL Server};SERVER=172.28.10.52;DATABASE=test;UID=test;PWD=test')
    db.autocommit=True
    cursor = db.cursor() 
    cursor.execute("select mac,publickey,testtime from PublicKey where (mac='%s') order by idx "%mac)
    data = cursor.fetchall()
    return data
    
def InsertPK(mac,key):
    db = pyodbc.connect('DRIVER={SQL Server};SERVER=172.28.10.52;DATABASE=test;UID=test;PWD=test')
    db.autocommit=True
    cursor = db.cursor() 
    tmp = time.localtime(time.time())
    testtime =  "%d/%d/%d %d:%d:%d"%tmp[:6]
    cursor.execute("insert into PublicKey (mac,testtime,publickey) values ('%s','%s',?) "%(mac,testtime),(buffer(key)))
    return 

    
def check(filename):
    data = open("%s.txt"%filename).read().split()
    ok = open("ok_all.csv").read()
    ng = open("ng_all.csv").read()
    null = open("not_all.csv").read()
    p = open("%s_ok.csv"%filename,"w")
    f = open("%s_uc.csv"%filename,"w")
    m = open("%s_mf.csv"%filename,"w")
    a=0
    for mac in data:
        print a,mac,
        if mac in ok:
           p.write(mac+"\n")
           print "PASS"
        if mac in ng:
           src = "key\\%012X.der"%(int(mac,16)+1)
           dst = "%s\\%012X.der"%(filename,int(mac,16)+1)
           shutil.copy(src,dst) 
           m.write(mac+"\n")
           print "MODIFY"
        if mac in null:
           f.write(mac+"\n")
           print "FAIL"
        a+=1


def check_mes():
    mes = open("mes_all_data.csv").read().split("\n")
    not_ = open("not_all.csv").read().split("\n")
    ng_ = open("ng_all.csv").read().split("\n")
    n = open("not_all_mes.csv","w")
    f = open("ng_all_mes.csv","w")
    for line in not_:
        print line
        mac = line.split(",")[0]
        for l in mes:
            if mac in l:
               n.write("%s,%s\n"%(line,l.split(",")[3]))
               break
    for line in ng_:
        print line
        mac = line.split(",")[0]
        for l in mes:
            if mac in l:
               f.write("%s,%s\n"%(line,l.split(",")[3]))
               break           

def GetKey():
    data = open("ng_all.csv").read().split("\n")
    a = 0
    for line in data:
        mac,id1 = line.split(",")[:2]
        src = "key-%s\\%012X.der"%(id1,int(mac,16)+1)
        dest = "key\\%012X.der"%(int(mac,16)+1)
        shutil.copy(src,dest) 
        print a,src,dest,'PASS'
        a+=1
        
        
        
def check_rework():
    data = open("rework.csv").read().split()
    ng = open("ng_all.csv").read()
    ok = open("ok_all.csv").read()
    nt = open("not_all.csv").read()
    f = open("rework_ng.csv","w")
    n = open("rework_null.csv","w")
    p = open("rework_ok.csv","w")
    a = 0
    for mac in data:
        print a,mac,
        if mac in ng:
           f.write(mac+"\n")
           print "FAIL"
        elif mac in ok:
           p.write(mac+"\n")
           print "PASS"
        else:
           n.write(mac+"\n")
           print "NULL"
        
def check_rework_key():
    data = open("rework.csv").read().split()
    ng = open("rework_ng.csv").read()
    ok = open("rework_ok.csv").read()
    f = open("rework_ng_ng.csv","w")
    p = open("rework_ok_ng.csv","w")
    o = open("rework_ok_ok.csv","w")
    a = 0
    for mac in data:
        print a,mac,
        if mac in ng:
           src = open("key\\%012X.der"%(int(mac,16)+1),"rb").read()
           df = "CGNV4-LOG\\%012X.der"%(int(mac,16)+1)
           if not os.path.isfile(df):
              print "Not found"
              a+=1
              continue
           dst = open(df,"rb").read()
           if src<>dst:
              f.write(mac+"\n")
              print "FAIL"
           else:
              o.write(mac+"\n")
              print "PASS" 

        if mac in ok:
           src = bz2.decompress(getPK(mac)[-1][1])
           df = "CGNV4-LOG\\%012X.der"%(int(mac,16)+1)
           if not os.path.isfile(df):
              print "Not found"
              a+=1
              continue
           dst = open(df,"rb").read()
           if src<>dst:
              p.write(mac+"\n")
              print "FAIL"
           else:
              o.write(mac+"\n")
              print "PASS" 
        a+=1


def check_key():
    fs = glob.glob(r"F:\TestScript\produt\publicKey\result\CGNV4-LOG\*.der")
    ng = open("ng_all.csv").read()
    ok = open("ok_all.csv").read()
    nt = open("not_all.csv").read()
    f = open("key_ng.csv","w")
    n = open("key_null.csv","w")
    p = open("key_ok.csv","w")
    a=b=c=0
    for f in fs:
        emac = f.split("\\")[-1].split(".")[0]
        mac = "%012X"%(int(emac,16)-1)
        print a,b,c,emac,
        if mac in ng:
           src = open("key\\%s.der"%emac,"rb").read()
           df = "CGNV4-LOG\\%s.der"%emac
           dst = open(df,"rb").read()
           if src<>dst:
              f.write(mac+"\n")
              print "FAIL"
           else:
              p.write(mac+"\n")
              print "NG_PASS" 
              b+=1
        if mac in ok:
           src = bz2.decompress(getPK(mac)[-1][1])
           df = "CGNV4-LOG\\%s.der"%emac
           dst = open(df,"rb").read()
           if src<>dst:
              f.write(mac+"\n")
              print "FAIL"
           else:
              p.write(mac+"\n")
              print "OK_PASS" 
              c+=1
        if mac in nt:
           n.write(mac+"\n")
           print "NULL"  
        a+=1


def GetMac():
    data = open('Lotfile_10841000827_1_RO.CGNV4_20141006.TXT').read().split("\n")
    f = open("Lotfile_10841000827_1_RO.CGNV4_20141006.csv","w")
    a = 0
    for line in data:
        mac = "".join(line.split(";")[7].split(":"))
        f.write(mac+"\n")
        print a,mac
        a+=1
        
def UploadKey():
    ng = open("ng_all.csv").read().split("\n")
    f = open("upload_key_ng.csv","w")
    a = 0
    for line in ng:
        mac = line.split(",")[0]
        print a,mac,
        src = open("key\\%012X.der"%(int(mac,16)+1),"rb").read()
        InsertPK(mac,bz2.compress(src))
        if bz2.decompress(getPK(mac)[-1][1])<>src:
           print "FAIL"
           f.write(mac+"\n")
        else:
           print "PASS"
        a+=1    

UploadKey()#20141014 11:20

#check("Lotfile_10841000827_1_RO.CGNV4_20141006")       
        
#check_rework_key()

#check_mes()

#check("SOW-140300022")
#check("SOW-140400014")
