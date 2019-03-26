from pexpect import pxssh
import os,nmap,socket,struct,fcntl
cport=8022

def decryptor(stri,key):
 res=""
 key=key*100
 for x in range(len(stri)):
  res=res+chr((ord(stri[x])-96)-(ord(key[x])-96)+96)
 return res

def encryptor(stri,key):
 res=""
 key=key*100
 for x in range(len(stri)):
  res=res+chr((ord(stri[x])-96)+(ord(key[x])-96)+96)
 return res

class bot:
 def __init__(self,ip):
  self.ip=ip

 def spawn(self):
  try:
   login=True
   self.session=pxssh.pxssh()
   self.session.login(self.ip,"u0_a213","raspberry",port=cport)
   print("Logged into "+self.ip)
  except:
   login=False
   print("Login failed for "+self.ip)
  return login

 def cmd(self,com,out=False):
  try:
   self.session.sendline(com)
   if out:
    self.session.prompt()
    print(self.session.before)
  except:
   print(com+" Failed on "+self.ip)

def getmyip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])

def search(myip):
 print("My ip address is "+myip)
 suf=""
 skip=[]
 domain=myip[:myip.rfind(".")]
 while suf != "":
  suf=str(raw_input("Please enter any ip suffixes you want to skip:"))
  skip.append(suf)
 print("Scanning for bots on "+domain)
 scanner=nmap.PortScanner()
 scanner.scan(domain+".0/24",str(cport))
 suffixes=scanner.all_hosts()
 print("Found "+str(len(suffixes))+" hosts with "+str(cport)+" open!")
 return suffixes

def sendall(bots,cmd,out=True):
 for b in bots:
  b.cmd(cmd,out)

def connect(ips):
 bots=[]
 for ip in ips:
  tmp=bot(ip)
  if tmp.spawn()==True:
   bots.append(tmp)
 return bots

bots=connect(search(getmyip("wlan0")))
print(str(len(bots))+" active")
while len(bots) >0:
  sendall(bots,str(raw_input(">>>")))
print("All bots offline")
