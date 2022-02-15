import os,string,time,socket,select
import telnetlib,serial,bz2
import subprocess,sys
import errno

"""
snmp://<v3 user>:<v3 password>@<host>:<port>/<community>/<MIB File>/<MIB object>/<type>
ftp://<user>:<password>@<host>:<port>/<path>
http://<user>:<password>@<host>:<port>/<url-path>
tftp://<user>:<password>@<host>:<port>/<url-path>
udp://<host>:<port>
htxpy://<host>:<port>

tcp://<host>:<port>
term://<user>:<password>@<host>:<baud rate>/<com N>
telnet://<user>:<password>@<host>:<port>
"""
tool_dir = "C:/Net-SNMP/bin"
log = 0

def LogResult(name,direct,data):
    if log:
        if not data: data = ""
        open(name+".log","a").write(direct+data)
    return data


def InitXurl(path):
    global tool_dir
    if os.path.isfile(path+"/snmpget.exe") and \
       os.path.isfile(path+"/hrping.exe") and \
       os.path.isfile(path+"/process.exe") and \
       os.path.isfile(path+"/wget.exe") and \
       os.path.isfile(path+"/wput.exe"):
        tool_dir = path
        return 0
    print "Missing some tools(snmpget,hrping,process,wget,wput)"
    return 1



def parser(urls):
    protocol = user = passwd = host = port = ""
    url_str = urls.strip()
    protocol,url = url_str.split("://")
    url = url.split("/")
    at = url[0].find('@')
    if at > 0:
        user,passwd = url[0][:at].split(':')
    host = url[0][at+1:].split(':')
    if len(host)==1:
        host = host[0]
    else:
        host, port = host
    return (urls,protocol,user,passwd,host,port,url[1:])



class HTX_snmp:
    def __init__(self,all,user,passwd,host,port,*path):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        path = path[0]
        if len(path) < 4:
            raise "Missing snmp parameters!!"
        self.community = path[0]
        self.mibfile = path[1]
        self.mibobj = path[2]
        self.type = path[3]

    def get(self):
        if self.mibfile == "*":
            mibf = ""
        else:
            mibf = "-m "+self.mibfile
        data = os.popen(tool_dir+"/snmpget %s -r 1 -t 3 -O 0U -c %s -v 2c %s %s"%\
                        (mibf,self.community,self.host,self.mibobj)).read()
        index = data.find(self.mibobj)
        if index>=0:
            index = data.find(": ")
            if index >=0:
                result = data[index+2:].strip()
                if data.find("INTEGER: ")>=0:
                    if "(" in result:
                        result = result[result.find("(")+1:result.find(")")]
                elif len(result)==17 and len(result.split(':'))==6:
                    result = "".join(result.split(':')).upper()
                if result and result[0] == '"':
                    return LogResult("HTX_snmp",">>>",result[1:-1])
                else:
                    return LogResult("HTX_snmp",">>>",result)
        return None

    def set(self,value):
        value = str(value)
        if self.type == "s" : value='"'+value+'"'
        data = os.popen(tool_dir+'/snmpset -r 0 -m %s -c %s -v 2c %s %s %s %s'%\
                       (self.mibfile,self.community,self.host,self.mibobj,self.type,value)).read()
        LogResult("HTX_snmp","<<<",value)
        return data

    def close(self):
        pass

    def wait(self,value,timeout):
        current = time.time()
        timeout += current
        count = 0
        while current < timeout:
            count += 1
            if count%10 == 0: print ".",
            result = self.get()
            if str(value) == result:
                if count >= 10: print
                return result
            time.sleep(0.1)
            current = time.time()
        if count >= 10: print "!"
        return ""

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        pass

    def __del__(self):
        self.close()



class HTX_telnet:
    def __init__(self,all,user,passwd,host,port,*path):
        path = path[0]
        self.user = user
        self.passwd = passwd
        self.host = host
        self.cr = "\n"   # default Carriage Return
        self.buffer_size = 32768   # default waiting buffer size
        if port:
            self.port = int(port)
        else:
            self.port = 23
        self.tn = telnetlib.Telnet(host,self.port)
        self.tn.get_socket().setblocking(0)
        if user and passwd:
            response = self.tn.read_until(":", 5)
            self.tn.write(user + self.cr)
            response = self.tn.read_until(":", 5)
            self.tn.write(passwd + self.cr)

    def get(self):
        return LogResult("HTX_telnet",">>>",self.tn.read_very_eager())

    def set(self,value):
        return LogResult("HTX_telnet","<<<",self.tn.write(value + self.cr))

    def close(self):
        if self.tn:
            self.tn.close()
            self.tn = None

    def wait(self,prompt,timeout):
        try:
            current = time.time()
            prompt = str(prompt)
            timeout += current
            response = ""
            count = 0 
            while current < timeout:
                count += 1
                if count == 30:
                    print ".",
                    count = 0 
                if len(response)>self.buffer_size:
                    response = response[-len(prompt):]
                response += self.get()
                if prompt in response:
                    if count >= 10:  print
                    return response
                time.sleep(0.1)
                current = time.time()
            if count >= 10: print "!"
            return ""
        except EOFError:
            print "Telnet EOFERROR!!"
            return ""

    def __del__(self):
        self.close()

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        for k in options.keys():
            self.__dict__[k] = options[k]



class HTX_term:
    def __init__(self,all,user,passwd,host,port,*path):
        path = path[0]
        self.user = user
        self.passwd = passwd
        self.host = host
        self.baud = int(port)
        self.com = path[0]
        self.console = serial.Serial(path[0], self.baud, timeout=1)
        self.cr = "\n\r"   # default Carriage Return
        self.buffer_size = 32768   # default waiting buffer size

    def get(self):
        buf = ""
        while 1:
            count = self.console.inWaiting()
            if not count:
                break
            buf += self.console.read(count)
        return LogResult("HTX_term","<<<",buf)

    def set(self,value):
        return LogResult("HTX_term",">>>",self.console.write(value + self.cr))

    def close(self):
        if self.console:
            self.console.close()
            self.console = None

    def wait(self,prompt,timeout):
        current = time.time()
        prompt = str(prompt)
        timeout += current
        response = ""
        count = 0 
        while current < timeout:
            count += 1
            if count == 30:
                print ".",
                count = 0 
            if len(response)>self.buffer_size:
                response = response[-len(prompt):]
            response += self.get()
            if prompt in response:
                if count >= 10:  print
                return response
            time.sleep(0.1)
            current = time.time()
        if count >= 10: print "!"
        return ""

    def __del__(self):
        self.close()

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        for k in options.keys():
            self.__dict__[k] = options[k]



class HTX_http:
    def __init__(self,all,user,passwd,host,port,*path):
        self.all = all

    def get(self):
        data = os.popen(tool_dir+"/wget %s -O %s"% \
                        (self.all,self.all.split('/')[-1])).read()
        i = data.rfind('(')
        if i >= 0:
            value,unit = data[i+1:].split()[:2]
            if unit[0] == 'M' :
                value = float(value)*1000000
            else:
                value = float(value)*1000

            return value
        return 0

    def set(self,value):
        return 0

    def close(self):
        pass

    def wait(self,value,timeout):
        pass

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        pass

    def __del__(self):
        self.close()


class HTX_ftp(HTX_http):
    def set(self,value):
        data = os.popen(tool_dir+"/wput -u %s %s"% \
                        (self.all.split('/')[-1],self.all)).read()
        i = data.find('`')
        if i >= 0:
            j = data.find('/')-1
            value = data[i+1:j]
            if data[j] == 'M' :
                value = float(value)*1000000
            else:
                value = float(value)*1000

            return value
        return 0



class HTX_udp:
    def __init__(self,all,user,passwd,host,port,*path):
        self.host = host
        if port:
            self.port = int(port)
        else:
            self.port = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0.1)
        self.bind = 0

    def get(self):
        # Accept UDP datagrams, on the given port, from any sender
        if not self.bind:
            self.socket.bind(("", self.port))
            self.bind = 1
        # print "waiting on port:", port
        try:
            data, addr = self.socket.recvfrom(65536)
        except socket.timeout:
            data = ""
        return data

    def set(self,value):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return s.sendto(value, (self.host, self.port))

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket =  None

    def wait(self,prompt,timeout):
        if not timeout:
            timeout = 1000000
        current = time.time()
        prompt = str(prompt)
        timeout += current
        response = ""
        count = 0
        while current < timeout:
            count += 1
            if count%10 == 0:  print ".",
            if len(response)>10000000:
                response = response[-len(prompt):]
            value = self.get()
            if value:
                response += value
                if prompt in response:
                    if count >= 10:  print
                    return response
            current = time.time()
        if count >= 10: print "!"
        return ""

    def __del__(self):
        self.close()

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        pass



class HTX_tcps:
    def __init__(self,all,user,passwd,host,port,*path):
        self.host = host
        if port:
            self.port = int(port)
        else:
            self.port = 23
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        self.socket.listen(1)
        self.channel_accept = None

    def get(self):
        if self.channel_accept:
            return self.channel_accept.recv(65536)
        return None

    def set(self,value):
        return self.channel_accept.send(value)

    def close(self):
        if self.channel_accept:
            self.channel_accept.close()
            self.channel_accept = None

    def wait(self,prompt,timeout):
        is_readable = [self.socket]
        is_writable = []
        is_error = []
        r, w, e = select.select(is_readable, is_writable, is_error, timeout)
        if r:
            self.channel_accept, info = self.socket.accept()
            print "connection from", info
            return True
        return False

    def __del__(self):
        self.close()
        if self.socket:
            self.socket.close()
            self.socket =  None

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        pass



class HTX_tcpc:
    def __init__(self,all,user,passwd,host,port,*path):
        self.host = host
        if port:
            self.port = int(port)
        else:
            self.port = 23
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))

    def get(self):
        return self.socket.recv(65536)

    def set(self,value):
        return self.socket.send(value)

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket =  None

    def wait(self,prompt,timeout):
        is_readable = [self.socket]
        is_writable = []
        is_error = []
        r, w, e = select.select(is_readable, is_writable, is_error, timeout)
        if r:
            return True
        return False

    def __del__(self):
        self.close()

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        pass



class HTX_htxpy(HTX_udp):
    def __init__(self,all,user,passwd,host,port,*path):
        HTX_udp.__init__(self,all,user,passwd,host,port,*path)
        self.host = host
        self.port = 6000
    def get(self):
        return bz2.decompress(HTX_udp.get(self))
    def set(self,value):
        return HTX_udp.set(self,bz2.compress(value))



if sys.platform == 'win32':
    from win32file import ReadFile, WriteFile
    from win32pipe import PeekNamedPipe
    import msvcrt



class HTX_shell(subprocess.Popen):
    """ Example:
    if __name__ == '__main__':
        if sys.platform == 'win32':
            shell, commands, tail = ('cmd', ('dir /w', 'echo HELLO WORLD'), '\r\n')
        else:
            shell, commands, tail = ('sh', ('ls', 'echo HELLO WORLD'), '\n')
        for i in range(1):
            a = Shell(shell)
            print a.get(),
            for cmd in commands:
                a.set(cmd)
                print a.get(),
            a.close('exit')
            print a.get()
    """
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {'stdin': subprocess.PIPE, 'stdout': subprocess.PIPE}
        subprocess.Popen.__init__(self, args[3], **kwargs)
        self._setup()
        self.cr = "\r\n"
        self.exit = "exit"
        self.closed = False
        self.buffer_size = 32768   # default waiting buffer size

    def __repr__(self):
        return self.get()
    def __call__(self):
        return self.get()
    def __str__(self):
        return self.get()
    def __lshift__(self,data):
        return self.set(data)

    def get(self):
        time.sleep(0.1)
        r = self._recv('stdout',maxsize=None)
        if r is None:
            raise Exception("Other end disconnected!")
        return r

    def wait(self,prompt,timeout):
        current = time.time()
        prompt = str(prompt)
        timeout += current
        response = ""
        count = 0
        while current < timeout:
            count += 1
            if count%10 == 0: print ".",
            if len(response)>self.buffer_size:
                response = response[-len(prompt):]
            response += self.Get()
            if prompt in response:
                if count >= 10:  print
                return response
            current = time.time()
        if count >= 10: print "!"
        return ""

    def set(self,data):
        if self.cr:
            data += self.cr
        while len(data):
            sent = self.send(data)
            if sent is None:
                raise Exception("Other end disconnected!")
            data = buffer(data, sent)
        return 0

    def close(self):
        if not self.closed:
            self.closed = True
            self.set(self.exit)
            subprocess.Popen.wait(self)

    def __del__(self):
        self.close()

    def recv_err(self, maxsize=None):
        return self._recv('stderr', maxsize)

    def send_recv(self, input='', maxsize=None):
        return self.send(input), self.recv(maxsize), self.recv_err(maxsize)

    def get_conn_maxsize(self, which, maxsize):
        if maxsize is None:
            maxsize = self.buffer_size
        elif maxsize < 1:
            maxsize = 1
        return getattr(self, which), maxsize

    def _close(self, which):
        getattr(self, which).close()
        setattr(self, which, None)

    if subprocess.mswindows:
        def _setup(self):
            pass

        def send(self, input):
            if not self.stdin:
                return None

            try:
                x = msvcrt.get_osfhandle(self.stdin.fileno())
                (errCode, written) = WriteFile(x, input)
            except ValueError:
                return self._close('stdin')
            except (subprocess.pywintypes.error, Exception), why:
                if why[0] in (109, errno.ESHUTDOWN):
                    return self._close('stdin')
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = self.get_conn_maxsize(which, maxsize)
            if conn is None:
                return None

            try:
                x = msvcrt.get_osfhandle(conn.fileno())
                (read, nAvail, nMessage) = PeekNamedPipe(x, 0)
                if maxsize < nAvail:
                    nAvail = maxsize
                if nAvail > 0:
                    (errCode, read) = ReadFile(x, nAvail, None)
            except ValueError:
                return self._close(which)
            except (subprocess.pywintypes.error, Exception), why:
                if why[0] in (109, errno.ESHUTDOWN):
                    return self._close(which)
                raise

            if self.universal_newlines:
                read = self._translate_newlines(read)
            return read

    else:
        def _setup(self):
            import fcntl
            for i in (self.stdin, self.stdout, self.stderr):
                flags = fcntl.fcntl(i, fcntl.F_GETFL)
                fcntl.fcntl(i, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        def send(self, input):
            if not self.stdin:
                return None

            if not select.select([], [self.stdin], [], 0)[1]:
                return 0

            try:
                written = os.write(self.stdin.fileno(), input)
            except OSError, why:
                if why[0] == errno.EPIPE: #broken pipe
                    self.stdin.close()
                    self.stdin = None
                    return None
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = get_conn_maxsize(which, maxsize)
            if conn is None:
                return None

            if not select.select([conn], [], [], 0)[0]:
                return ''

            r = conn.read(maxsize)
            if not r:
                conn.close()
                setattr(self, which, None)
                return None

            if self.universal_newlines:
                r = self._translate_newlines(r)
            return r

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        for k in options.keys():
            self.__dict__[k] = options[k]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       