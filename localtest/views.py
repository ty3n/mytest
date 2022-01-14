from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .testlibs import test
import configparser
import threading, traceback
from localtest.models import Panel, Percent
import sys, requests
from django.http import JsonResponse
import time, json, zipfile
from scapy.all import *
# Create your views here.
m = {}
success = []

class Monitor(threading.Thread):
    def __init__(self, c,flows):
        threading.Thread.__init__(self)
        self.term = ''
        self._id = c[1]
        self.card = Panel.objects.get(pk=self._id)
        self.card._status = 'running'
        self.card.content = ''
        self.flows = flows
        self.ip = '192.168.100.1'+c[1]
        self.card.save()
    def msg(self,n):
        self.card = Panel.objects.get(pk=self._id)
        s = n+'\n'
        self.card.content += s
        self.card.save()
    def run(self):
        l = len(self.flows)
        try:
            for s,t in enumerate(self.flows):
                self.card = Panel.objects.get(pk=self._id)
                if s+1 < l: 
                    self.card.next_test = self.flows[s+1]
                else: 
                    self.card.next_test = 'None'
                self.card.cur_test = t
                self.card.save()
                eval("test.{}(self)".format(t))
            # self.status = 'pass'
            self.card = Panel.objects.get(pk=self._id)
            self.card._status = 'pass'
            self.card._pass += 1
            self.card.save()
        except Exception as e:
            error_class = e.__class__.__name__
            detail = e.args[0]
            cl, exc, tb = sys.exc_info()
            CallStack = traceback.extract_tb(tb)
            for q in CallStack:
                fileName = q[0]
                lineNum = q[1]
                funcName = q[2]
                errMsg = "File \"{}\", line {}, in {}: [{}] {}\n".format(fileName, lineNum, funcName, error_class, detail)
                self.msg(errMsg)
            # self.status = 'fail'
            self.card._status = 'fail'
            self.card._fail += 1
            self.card.save()

def index(request):
    return render(request = request,
                  template_name='main/index.html',
                  context={"Panels":Panel.objects.all()})

class Collect(APIView):
    authentication_classes = []
    permission_classes = []
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./localtest/testlibs/config.ini')
        self.flows = config['flows']['Test'].split(',')
    def get(self , request):
        context={'log':'1111','card':'1111','status':'111'}
        d = request.GET.dict()
        print(d)
        if not d:
            return Response(Panel.objects.values())
        return Response(Panel.objects.filter(_id=d['_id']).values())
    def post(self, request):
        print(request.data)
        mCard = request.data['card']
        print(request.data['status'], 'clean')
        print(request.data['status']=='clean')
        if request.data['status'] == 'start':
            m[mCard] = Monitor(mCard,self.flows)
            m[mCard].start()
        elif request.data['status'] == 'clean':
            p = Panel.objects.get(pk=mCard[1])
            p._fail = 0
            p._pass = 0
            p.save()
            return Response({'fail':p._fail,'pass':p._pass,'log':'','card':mCard,'status':'clean','flow':'Waiting','nflow':p.next_test})
        elif request.data['status'] == 'restore':
            p = Panel.objects.get(pk=mCard[1])
            return Response({'fail':p._fail,'pass':p._pass,'log':'','card':mCard,'status':p._status,'flow':p.cur_test,'nflow':p.next_test})
        # print(m[mCard].log)
        # context={'log':m[mCard].log,'card':m[mCard].card,'status':m[mCard].status,'flow':m[mCard].f,'nflow':m[mCard].nf}
        if m[mCard].card._status == 'pass':
            # success.append(request.data['mac'])
            pass
        context={'fail':m[mCard].card._fail,'pass':m[mCard].card._pass,'log':m[mCard].card.content,'card':'c'+str(m[mCard].card.pk),'status':m[mCard].card._status,'flow':m[mCard].card.cur_test,'nflow':m[mCard].card.next_test}
        return Response(context)

def iface_ip_get_mac(ip):
    for i in list(conf.ifaces.__dict__['data'].values()):
        if conf.ifaces.dev_from_name(i).ip == ip: return (conf.ifaces.dev_from_name(i).mac, conf.ifaces.dev_from_name(i).name)
    raise Exception('Interface Get Mac Error!!')

#'98:fa:9b:44:c2:a2', 192.168.100.10,'乙太網路'
def arpGetMac(mac,ip,iface):
    sniff = AsyncSniffer(iface=iface,filter="arp",lfilter=lambda d: d.dst == mac)
    sniff.start()
    sendp(Ether(src=mac, dst='ff:ff:ff:ff:ff:ff')/ARP(hwsrc=mac, psrc=ip, pdst='192.168.100.1'), iface=iface, verbose = False)
    time.sleep(0.05)
    sniff.stop()
    return [i.hwsrc for i in sniff.results[ARP]]

#curl -X POST -H "Content-Type: application/json" -d '{"auto" : True}' "http://127.0.0.1:8000/api/arp/"

class Arp(APIView):
    def __init__(self):
        self.ip = '192.168.100.10'
        self.mac, self.iface = iface_ip_get_mac(self.ip)
        self.arp = []
        self.auto = False
    def get(self , request):
        success = []
        return Response({'auto':self.auto})
    def post(self, request):
        self.auto = request.data['auto']
        self.arp = arpGetMac(self.mac,self.ip,self.iface)
        arp = list(set([''.join(i.split(':')) for i in list(self.arp)])-set(success))
        print(success,self.arp)
        print(arp)
        return Response({'auto':self.auto,'arp':arp})

class dload(threading.Thread):
    def __init__(self, p, file):
        threading.Thread.__init__(self)
        self.p = p
        self.t = time.time()
        self.f = file
    def run(self):
        if not self.p.percent:
            s = requests.get('http://172.25.70.190:8000/api/v1/repos/nick/{}/'.format(self.f))
            defaultbranch = json.loads(s.content.decode('utf-8'))['default_branch']
            r = requests.get('http://172.25.70.190:8000/api/v1/repos/nick/{}/archive/{}.zip'.format(self.f,defaultbranch), stream=True)
            path = '{}.zip'.format(defaultbranch)
            l = 0
            with open(path, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in r.iter_content(chunk_size=8192):
                    l += len(chunk)
                    if time.time() - self.t > 1:
                        self.t = time.time()
                        if self.p.percent != round(l/total_length,2)*100:
                            self.p.percent = round(l/total_length,2)*100
                            self.p.save()
                            print ( round(l/total_length,2)*100, '%' )
                    if chunk:
                        f.write(chunk)
                        f.flush()
                if self.p.percent != round(l/total_length,2)*100:
                    self.p.percent = round(l/total_length,2)*100
                    self.p.save()
                    print ( round(l/total_length,2)*100, '%' )
            time.sleep(3)
            with zipfile.ZipFile(path,"r") as zip_ref:
                zip_ref.extractall("./localtest/testlibs/")

class GiteaDownload(APIView):
    def __init__(self):
        self.mydload = object()
        self.percent = 0
        self.p = Percent.objects.get()
        self.fname = ''
    def get(self, request):
        return Response({'name':self.fname,'percent':int(self.p.percent),'script':self.p._script})
    def post(self, request):
        self.fname = request.data['repo'].split('/')[-1]
        if self.p.percent==100:
            self.p.percent = 0
            self.p._script = request.data['repo']
            self.p.save()
            self.mydload = dload(self.p,self.fname)
            self.mydload.start()
        return Response({'name':'{}.zip'.format(self.fname),'percent':self.p.percent,'script':self.p._script})

def iface_ip_get_mac(ip):
    for i in list(conf.ifaces.__dict__['data'].values()):
        if conf.ifaces.dev_from_name(i).ip == ip: return (conf.ifaces.dev_from_name(i).mac, conf.ifaces.dev_from_name(i).name)
    return False

class AFI:
    def __init__(self,src):
        self.imac, self.iname = iface_ip_get_mac(src)
        self.CCU = {}
        t = AsyncSniffer(iface=self.iname, prn=lambda x: x.show())
        t.start()
        sendp(eval("Ether(src='{}', dst='ff:ff:ff:ff:ff:ff', type=4660)/Raw(load='info')".format(self.imac)), iface=self.iname)
        time.sleep(0.5)
        sendp(eval("Ether(src='{}', dst='ff:ff:ff:ff:ff:ff', type=4660)/Raw(load='info')".format(self.imac)), iface=self.iname)
        t.stop()
        d = [i.load.decode('utf-8').split('CCU\tinfo\t')[-1] for i in t.results if 'CCU' in i.load.decode('utf-8')]
        for s in d:
            _id, _mac = int(s.split(' ')[0]), s.split(' ')[1]
            self.CCU.update({_id:_mac})
    def sccu(self, idx, cmd):
        t = AsyncSniffer(iface="Ethernet5", prn=lambda x: x.show())
        t.start()
        sendp(eval("Ether(src='{}', dst='{}', type=4660)/Raw(load='CCU\t{}')".format(self.imac,self.CCU[idx],cmd)), iface=self.iname)
        time.sleep(0.5)
        sendp(eval("Ether(src='{}', dst='{}', type=4660)/Raw(load='CCU\t{}')".format(self.imac,self.CCU[idx],cmd)), iface=self.iname)
        t.stop()
        r = [i.load.decode('utf-8') for i in t.results if 'OK' in i.load.decode('utf-8')][0]
        return r[0]

# s = AFI('192.168.84.10')
# s.sccu(0,"ip 192.168.84.100  255.255.255.0 192.168.100.20 255.255.255.0")
# s.sccu(0,"prelay 69 eth0 69 192.168.84.10 1")
# for v_ in range(1,8):
#   for p_ in range(1,5):
#       s.sccu(0,"prelay 30%s%s vlan%s%s 23 192.168.100.1 23"%(v_,p_,v_,p_))
    
