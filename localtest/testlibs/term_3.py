import serial, time 
from binascii import unhexlify
import binascii
import sys,os,string,time,serial,subprocess,ctypes,telnetlib
from telnetlib import DO, DONT, WILL, WONT, theNULL, TTYPE, IAC, SB,SE, ECHO
import paramiko, socket
DEFAULT_LOG=0

def telnet_negotiation(sock, command, option):
    #
    # Here's a function I came up with to handle sub-negotiation.
    # During session negotiation, the server can ask a series of
    # "will you or won't you" questions of the client. One of
    # those questions happens to be:
    # "Will you tell me what terminal type you are?"
    # This question is the only one out of the possible list of
    # such questions that I respond with "Yes, I will." Then later
    # the function reports that the terminal type is a DEC VT-100.
    # If you don't do the sub-negotiation and the server demands
    # to know the terminal type, the Telnet function will report
    # that the terminal type is simply "network". No server will
    # recognize this, and some will refuse to even start a session
    # with you using some default terminal type.
    # A couple of good links--
    # http://www.cs.cf.ac.uk/Dave/Internet/node136.html
    # http://www.scit.wlv.ac.uk/rfc/rfc8xx/RFC854.html
    #
    negotiation_list=[
        ['BINARY',WONT,'WONT'],
        ['ECHO',WONT,'WONT'],
        ['RCP',WONT,'WONT'],
        ['SGA',WONT,'WONT'],
        ['NAMS',WONT,'WONT'],
        ['STATUS',WONT,'WONT'],
        ['TM',WONT,'WONT'],
        ['RCTE',WONT,'WONT'],
        ['NAOL',WONT,'WONT'],
        ['NAOP',WONT,'WONT'],
        ['NAOCRD',WONT,'WONT'],
        ['NAOHTS',WONT,'WONT'],
        ['NAOHTD',WONT,'WONT'],
        ['NAOFFD',WONT,'WONT'],
        ['NAOVTS',WONT,'WONT'],
        ['NAOVTD',WONT,'WONT'],
        ['NAOLFD',WONT,'WONT'],
        ['XASCII',WONT,'WONT'],
        ['LOGOUT',WONT,'WONT'],
        ['BM',WONT,'WONT'],
        ['DET',WONT,'WONT'],
        ['SUPDUP',WONT,'WONT'],
        ['SUPDUPOUTPUT',WONT,'WONT'],
        ['SNDLOC',WONT,'WONT'],
        ['TTYPE',WILL,'WILL'],
        ['EOR',WONT,'WONT'],
        ['TUID',WONT,'WONT'],
        ['OUTMRK',WONT,'WONT'],
        ['TTYLOC',WONT,'WONT'],
        ['VT3270REGIME',WONT,'WONT'],
        ['X3PAD',WONT,'WONT'],
        ['NAWS',WONT,'WONT'],
        ['TSPEED',WONT,'WONT'],
        ['LFLOW',WONT,'WONT'],
        ['LINEMODE',WONT,'WONT'],
        ['XDISPLOC',WONT,'WONT'],
        ['OLD_ENVIRON',WONT,'WONT'],
        ['AUTHENTICATION',WONT,'WONT'],
        ['ENCRYPT',WONT,'WONT'],
        ['NEW_ENVIRON',WONT,'WONT']
    ]
    if ord(option)<40:
        received_option=negotiation_list[ord(option)][0]
        response=negotiation_list[ord(option)][1]
        print_response=negotiation_list[ord(option)][2]
    else:
        received_option='unrecognised'
        response=WONT
        print_response='WONT'
    if command==DO:
        print("TELNET Debug: Received request to DO %s, sending %s" % \
            (received_option,print_response))
        sock.sendall("%s%s%s" % (IAC, response, option))
    elif command==DONT:
        print('TELNET Debug: Received the DONT command')
    elif command==WILL:
        print('TELNET Debug: Received the WILL command')
    elif command==WONT:
        print('TELNET Debug: Received the WONT command')
    elif command==theNULL:
        print('TELNET Debug: Received the NULL command')
    elif command==SB:
        print('TELNET Debug: Received the SB command')
        print(ord(option))
        print(self.conn.read_sb_data())
    elif command==SE:
        print('TELNET Debug: Received the SE command')
        print(repr(self.conn.read_sb_data()))
        sock.sendall("%s%s%s%sDEC-VT100%s%s" % \
            (IAC,SB,TTYPE,chr(0),IAC,SE))
        print('TELNET Debug: Sent all')
    else:
        print('TELNET Debug: Received something, don''t know what.', ord(option))
    return

class Controller(object):
    def get(self):
        return ""
    def set(self, value):
        pass
    def wait(self,timeout):
        return (False,"")
    def setWait(self,value,timeout):
        return (False,"")
    def isConnect(self):
        return True

class Terminal(Controller):
    LOST_CONNECT = "** Fail Connection **"
    def __init__(self,host,port):
        self.log = DEFAULT_LOG
        self.host = host
        self.cr = "\r"   # default Carriage Return
        self.buffer_size = 32768   # default waiting buffer size
        self.port = port
        self.tn = None
    def _init(self):
        pass
    def _get(self):
        pass
    def _set(self,value):
        pass
    def _close(self):
        self.tn.close()
    def init(self):
        self.close(0)
        try:
           self._init()
        except:
           self.tn = 0
    def isConnect(self):
        return self.tn
    def get(self):
        if self.tn == None:
            self.init()
        if self.tn == 0:
            print (self.LOST_CONNECT)
            return ""
        time.sleep(0.01)
        try:
            r = self._get()
        except:
            self.tn = 0
            print (self.LOST_CONNECT)
            return ""
        if self.log&2:
            print ("[GET]:",r)
        return r
    def set(self,value):
        if self.tn == None:
            self.init()
        if self.tn == 0:
            print (self.LOST_CONNECT)
            return 0
        if self.log&1:
            print ("[SET]:",value)
        try:
            r = self._set(value)
        except:
            self.tn = 0
            print (self.LOST_CONNECT)
            return 0
        return r
    def close(self,force=1):
        if self.tn:
            self._close()
            self.tn = None
            time.sleep(0.1)
        elif force:
            self.tn = None
    def wait(self,prompt,timeout):
        if self.tn == None:
            self.init()
        if self.tn == 0:
            print (self.LOST_CONNECT)
            return (False, "")
        prompt = str(prompt)
        timeout += time.time()+0.1
        response = ""
        count = 0 
        while time.time() < timeout and self.tn:
            count += 1
            if not (count&3):
                print (".",)
            if len(response)>self.buffer_size:
                response = response[-len(prompt):]
            d = self.get()
            response += d
            if not prompt:
                if not d:
                    return (False, response)
            else:
                if prompt in response:
                    if count >= 3:  print ()
                    return (False, response)
            time.sleep(0.1)
        if count >= 3: print ()
        if self.log&1:
            print ("Terminal: Timeout")
        return (True, response)
    def __del__(self):
        self.close()
    def getOption(self,optionName):
        return self.__dict__[optionName]
    def setOption(self,**options):
        for k in options.keys():
            self.__dict__[k] = options[k]
    def setWait(self,setData,prompt,timeout):
        if self.tn == 0:
            print (self.LOST_CONNECT)
            return (False,"")
        self.set(setData)
        return self.wait(prompt,timeout)
    def __repr__(self):
        return self.get()
    def __call__(self):
        return self.get()
    def __str__(self):
        return self.get()
    def __lshift__(self,data):
        return self.set(data)

#hex
class SerialTTY(Terminal):
    def __init__(self,host,port=115200):
        Terminal.__init__(self,host,port)
    def _init(self):
        try:
            self.tn = serial.Serial(self.host, self.port, timeout=0.5)
        except:
            self.tn = 0
    def _get(self):
        buf = ""
        while 1:
            count = self.tn.inWaiting()
            if not count:
                break
            buf += binascii.hexlify(self.tn.read(count)).decode()
        return buf
    def _set(self,value):
        self.tn.write(bytes.fromhex(value))
        return len(value)

class SerialTTY(Terminal):
    def __init__(self,host,port=115200):
        Terminal.__init__(self,host,port)
    def _init(self):
        try:
            self.tn = serial.Serial(self.host, self.port, timeout=0.5)
        except:
            self.tn = 0
    def _get(self):
        buf = ""
        while 1:
            count = self.tn.inWaiting()
            if not count:
                break
            buf += self.tn.read(count).decode()
        return buf
    def _set(self,value):
        self.tn.write(value.encode('ascii'))
        return len(value)

class SSH(Terminal):
    def __init__(self,host,name,pwd,port=22):
        Terminal.__init__(self,host,port)
        self.name = name
        self.pwd = pwd
        self.port = port
    def _init(self):
        # try:
        self.t = paramiko.Transport((self.host,self.port))
        self.t.connect(username=self.name,password=self.pwd)
        self.tn = self.t.open_session()
        self.tn.get_pty()
        self.tn.invoke_shell()
        # except:
            # self.tn = 0
    def _get(self):
        buf = ""
        time.sleep(1)
        while self.tn.recv_ready():
            buf += self.tn.recv(1).decode('ascii')
        return buf
    def _set(self,value):
        self.tn.send(value.encode('ascii'))
        return len(value)
    def wait(self,prompt,timeout):
        if self.tn == None:
            self.init()
        if self.tn == 0:
            return (False, "")
        prompt = str(prompt)
        timeout += time.time()+0.1
        response = ""
        count = 0 
        while time.time() < timeout and self.tn:
            count += 1
            if not (count&3):
                print(".",)
            # if len(response)>self.buffer_size:
            #     response = response[-len(prompt):]
            d = self.get()
            response += d
            # print "response <%s> prompt <%s>"%(response,prompt)
            if not prompt:
                if not d:
                    return (False, response)
            else:
                if prompt in response:
                    if count >= 3:  print
                    return (False, response)
            time.sleep(0.1)
        if count >= 3: print
        return (True, response)

class Telnet(Terminal):
    def __init__(self,host,port=23):
        Terminal.__init__(self,host,port)
    def _init(self):
        self.tn = telnetlib.Telnet()
        #self.tn.set_option_negotiation_callback(telnet_negotiation)
        self.tn.open(self.host,self.port)
        self.tn.get_socket().setblocking(0)
        #self.tn.debuglevel(2)
        time.sleep(0.5)
    def _get(self):
        return self.tn.read_very_eager().decode('ascii')
    def _set(self,value):
        self.tn.write((value+'\n').encode('ascii'))
        return len(value)

## multi-Telnet
class Telnet(Terminal):
    def __init__(self,host,src,keepalive = 0):
        Terminal.__init__(self,host,src)
        self.keepalive = int(keepalive)
        self.host = host
        self.src = src
    def _init(self):
        self.tn = telnetlib.Telnet()
        # self.tn.set_option_negotiation_callback(telnet_negotiation)
        self.tn.open(self.host,self.src)
        # self.tn.get_socket().setblocking(0)
        #self.tn.debuglevel(2)
        time.sleep(0.5)
        if self.keepalive:
           thread.start_new_thread(TCPKeepAlive,(self.tn,self.keepalive))
    def _get(self):
        return self.tn.read_very_eager().decode('utf-8')
    def _set(self,value):
        self.tn.write((value+'\n').encode('utf-8'))
        return len(value)

def lWaitCmdTerm(term,cmd,waitstr,sec,count=1):
    term << cmd
    data = ''
    for i in range(sec):
        time.sleep(1)
        d = term.get()
        if d: data += d
        if waitstr in data:
            return data
    raise Exception("failed: %s"%cmd)

'''
def lWaitCmdTerm(term,cmd,waitstr,sec,count=1):
    termport=term.host
    termdata=['']
    for i in range(count):
       term.get()
       term << "%s\n"%cmd
       termdata = term.wait("%s"%waitstr,sec)
       if termdata[0]:
           continue
       else:
           return termdata[1]
    raise Exception("%s port : %s  return : %s"%(cmd,termport,termdata[-1]))

def isPortConnect(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(3)
    result =1 
    try:
       s.connect((ip,int(port)))
    except Exception:
       result = 0
    s.close()
    return result
'''

# term=lLogin('192.168.100.1','root','iamgroot')

from scapy.all import *
import codecs

def decimalToHexadecimal(decimal,length=False):
    # Conversion table of remainders to
    # hexadecimal equivalent
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                        5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                        13: 'D', 14: 'E', 15: 'F'}
    hexadecimal = ''
    while(decimal > 0):
        remainder = decimal % 16
        hexadecimal = conversion_table[remainder] + hexadecimal
        decimal = decimal // 16
    if not hexadecimal: return '0'
    if len(hexadecimal) < length:
        difflen = length - len(hexadecimal)
        hexadecimal = '0'*difflen + hexadecimal
    return hexadecimal

def iface_ip_get_mac(ip):
    for i in list(conf.ifaces.__dict__['data'].values()):
        if conf.ifaces.dev_from_name(i).ip == ip: return (conf.ifaces.dev_from_name(i).mac, conf.ifaces.dev_from_name(i).name)
    return False

class TelnetLayer2:
    def __init__(self,srcmac,srcip,dstmac,dstip,iface):
        self.options = []
        self.iface = iface
        self.pkt = Ether(src=srcmac,dst=dstmac)/IP(src=srcip,dst=dstip,flags=0x2)/TCP(flags=0x2,options=self.options)
        self.pkt['IP'].id = random.randint(0,2**10-1)
        # pkt['IP'].id = 545
        self.pkt['IP'].ttl = 128
        self.pkt['TCP'].sport = random.randint(49152,65535)
        # pkt['TCP'].sport = 49837
        self.pkt['TCP'].dport = 23
        self.pkt['TCP'].window = 64240
        self.pkt['TCP'].seq = random.randint(0,2**32-1)
        self.ans, self.unans = 0, 0
        self.data = ''
        self.sniff = AsyncSniffer(iface=self.iface, prn=lambda x: self.parsing(x),filter="tcp",lfilter=lambda d: d.src == dstmac)
        self.sniff.start()
        time.sleep(0.5)
        self.spkt([('MSS', 1460), ('NOP', 0), ('WScale', 8), ('NOP', 0), ('NOP', 0), ('SAckOK', '' )],0x2)
        time.sleep(1)
    def parsing(self,p):
        self.pkt['TCP'].seq = p['TCP'].ack
        if not p['TCP'].payload:
            self.pkt['TCP'].ack = p['TCP'].seq + 1
        else:
            self.pkt['TCP'].ack = p['TCP'].seq + len(p['TCP'].load)
        self.pkt['IP'].ttl = 128
        self.pkt['TCP'].window = 256
        self.pkt['IP'].id += 1
        if 'Raw' in p and b'\\xff\\xfd\x01\\xff\\xfd!\\xff\\xfb\x01\\xff\\xfb\x03' not in p[Raw].load:
            if b'\xff\xfb\x03' in p[Raw].load:
                self.data += p[Raw].load.split(b'\xff\xfb\x03')[-1].decode()
            else:
                self.data += p[Raw].load.decode()
        if 'Raw' in p and b'\\xff\\xfd\x01\\xff\\xfd!\\xff\\xfb\x01\\xff\\xfb\x03' in p[Raw].load:
            self.spkt([],0x18,'fffb01fffc21fffd01fffd03')
        if p.dataofs==5 and 'Padding' in p:
            pass
        else:
            if 'SA' in p[TCP].flags and p.dataofs==8:
                self.spkt([],0x10)
            if 'DF' in p.flags:
                self.spkt([],0x10)
        if p[TCP].flags=='PA':
            self.spkt([],0x10)
        if 'FA' in p[TCP].flags:
            self.spkt([],0x14)
            # self.close()
    def _decorator(foo):
        def update(self, options, flags, payload=''):
            self.pkt['TCP'].options = options
            self.pkt['TCP'].flags = flags
            self.pkt['TCP'].payload = Raw(bytes.fromhex(''))
            if payload:
                self.pkt['TCP'].payload = Raw(bytes.fromhex(payload))
            # print(hexdump(self.pkt))
            self.pkt['IP'].len = len(self.pkt)-14
            foo(self,options, flags, payload)
            # self.options = []
            # self.pkt = Ether(src='98:fa:9b:44:c2:a2',dst='20:6a:94:57:6e:7b')/IP(src='192.168.100.10',dst='192.168.100.1',flags=0x2)/TCP(flags=0x2,options=self.options)
            '''
            if not self.unans:
                self.pkt['TCP'].seq = self.ans[0].answer['TCP'].ack
                if not self.ans[0].answer['TCP'].payload:
                    self.pkt['TCP'].ack = self.ans[0].answer['TCP'].seq + 1
                else:
                    self.pkt['TCP'].ack = self.ans[0].answer['TCP'].seq + len(self.ans[0].answer['TCP'].load)
                self.pkt['IP'].ttl = 128
                self.pkt['TCP'].window = 256
                self.pkt['IP'].id = self.ans[0].query['IP'].id + 1 
                self.pkt['TCP'].sport = self.ans[0].query['TCP'].sport
                self.pkt['TCP'].dport = self.ans[0].query['TCP'].dport
                if self.ans[0].answer.dataofs==5:
                    if b'\xff\xfb\x01\xff\xfb\x03' in self.ans[0].answer['TCP'].load:
                        d = self.ans[0].answer['TCP'].load.replace(b'\xff\xfb\x01\xff\xfb\x03',b'')
                    d = self.ans[0].answer['TCP'].load
                    self.data += d
            '''
        return update
    @_decorator
    def spkt(self,options,flags,payload=''):
        self.options = options
        self.flags = flags
        self.flags = payload
        # self.ans, self.unans = srp(self.pkt,iface='乙太網路',filter='tcp',timeout=1,verbose=False)
        sendp(self.pkt,iface=self.iface,verbose=False)
        time.sleep(0.02)
    def close(self):
        self.spkt([],0x14)
        self.sniff.stop()
        self.data=''
    def wait(self,prompt,sec):
        d = ''
        for i in range(sec):
            if self.data:
                d += self.data
            if prompt in d:
                return d
            time.sleep(1)
        raise Exception('Wait prompt fail')
    def get(self):
        d = self.data
        self.data = ''
        return d
    def __repr__(self):
        d = self.data
        self.data = ''
        return d
    def __call__(self):
        d = self.data
        self.data = ''
        return d
    def __str__(self):
        d = self.data
        self.data = ''
        return d
    def __lshift__(self,data):
        self.spkt([],0x18,codecs.encode("{}\r".format(data).encode(), "hex").decode())
    def __del__(self):
        try:
            self.sniff.stop()
        except: pass

# srp(Ether(src='98:fa:9b:44:c2:a2',dst='20:6a:94:57:6e:7b')/IP(src='192.168.100.10',dst='192.168.100.1')/ARP(),retry=3,iface='乙太網路',filter='tcp',timeout=1)
# srp(Ether(src='98:fa:9b:44:c2:a2',dst='00:50:F1:21:00:10')/IP(src='192.168.100.10',dst='192.168.100.1')/ARP(),retry=3,iface='乙太網路',filter='tcp',timeout=1)

# a = srp(Ether(src='98:fa:9b:44:c2:a2', dst='fa:1d:0f:b4:8d:d2')/ARP(hwsrc='98:fa:9b:44:c2:a2', hwdst='fa:1d:0f:b4:8d:d2', psrc='192.168.100.10', pdst='192.168.100.1'), iface='乙太網路', verbose = False)
# a[0][ARP].show()

# b = srp(Ether(src='98:fa:9b:44:c2:a2', dst='20:6a:94:57:6e:7b')/ARP(hwsrc='98:fa:9b:44:c2:a2', hwdst='20:6a:94:57:6e:7b', psrc='192.168.100.10', pdst='192.168.100.1'), iface='乙太網路', verbose = False)
# b[0][ARP].show()

# b = sendp(Ether(src='98:fa:9b:44:c2:a2', dst='ff:ff:ff:ff:ff:ff')/ARP(hwsrc='98:fa:9b:44:c2:a2', psrc='192.168.100.10', pdst='192.168.100.1'), iface='乙太網路', verbose = False)
# sniff = AsyncSniffer(iface='乙太網路', prn=lambda x: x.show(),filter="arp",lfilter=lambda d: d.dst == '98:fa:9b:44:c2:a2')
# sniff.start()

# ans, unans = srp(Ether(dst="20:6a:94:57:6e:7b")/ARP(pdst="192.168.100.1"),timeout=2)

# t = TelnetLayer2('98:fa:9b:44:c2:a2','192.168.100.10','20:6a:94:57:6e:7b','192.168.100.1','乙太網路')
# t1 = TelnetLayer2('98:fa:9b:44:c2:a2','192.168.100.10','fa:1d:0f:b4:8d:d2','192.168.100.1','乙太網路')

# def hello(p):
#     print(p.dataofs)
#     print(hexdump(p))

# sniff = AsyncSniffer(iface='乙太網路', prn=lambda x: hello(x),filter="tcp",lfilter=lambda d: d.src == '20:6a:94:57:6e:7b')
# sniff.start()

# t._init
# t.spkt([('MSS', 1460), ('NOP', 0), ('WScale', 8), ('NOP', 0), ('NOP', 0), ('SAckOK', '' )],0x2)
# t.spkt([],0x18,'fffb01fffc21fffd01fffd03')
# t.spkt([],0x10)
# t.spkt([],0x18,codecs.encode(b"mso\r", "hex").decode())
# t.spkt([],0x10)
# t.spkt([],0x18,codecs.encode(b"msopassword\r", "hex").decode())
# Raw(bytes.fromhex(a))

def arpGetMac(ip):
    sniff = AsyncSniffer(iface='乙太網路', prn=lambda x: x.show(),filter="arp",lfilter=lambda d: d.dst == '98:fa:9b:44:c2:a2')
    sniff.start()
    sendp(Ether(src='98:fa:9b:44:c2:a2', dst='ff:ff:ff:ff:ff:ff')/ARP(hwsrc='98:fa:9b:44:c2:a2', psrc='192.168.100.10', pdst='192.168.100.1'), iface='乙太網路', verbose = False)
    time.sleep(0.05)
    sniff.stop()
    return [i.hwsrc for i in sniff.results[ARP]]

