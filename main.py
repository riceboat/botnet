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
 def __init__(self,ip,uname,pwd):
  self.ip=ip
  self.uname=uname
  self.pwd=pwd
 def spawn(self):
  try:
   login=True
   self.session=pxssh.pxssh()
   self.session.login(self.ip,self.uname,self.pwd,port=cport)
   print("Logged into "+self.ip)
  except:
   login=False
   print("Login failed for "+self.ip+"!")
  return login

 def cmd(self,com,out=False):
  try:
   self.session.sendline(com)
   if out:
    self.session.prompt()
    print(self.session.before)
  except:
   print(com+" Failed on "+self.ip+"!")

 def logoff(self):
  self.session.logout()

def getmyip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])

def search(myip):
 print("My ip address is "+myip)
 suf=" "
 skip=[]
 domain=myip[:myip.rfind(".")]
 while suf != "":
  suf=str(raw_input("Please enter any ip suffixes you want to skip:"))
  if suf != "":
   suf2=domain+"."+suf
   skip.append(suf2)
 print("Scanning for hosts on "+domain+"...")
 scanner=nmap.PortScanner()
 res=""
 for a in skip:
  res=" "+res+a
 if res == "":
  scanner.scan(domain+".0/24",str(cport))
 else:
  scanner.scan(domain+".0/24",str(cport),"--exclude"+res)
 suffixes=scanner.all_hosts()
 print("Found "+str(len(suffixes))+" hosts with port "+str(cport)+" open")
 return suffixes

def sendall(bots,cmd,out=True):
 for b in bots:
  b.cmd(cmd,out)

def connect(ips,uname,pwd):
 bots=[]
 print("User account > "+uname)
 for ip in ips:
  tmp=bot(ip,uname,pwd)
  if tmp.spawn()==True:
   bots.append(tmp)
 return bots

def getcreds(key):
 creds=[]
 cfile=open("BotCreds.txt","r")
 for line in cfile:
  creds.append(decryptor(line.strip(),key))
 cfile.close()
 return creds[0],creds[1]

def encodecreds():
 cfile=open("BotCreds.txt","w+")
 key=str(raw_input("Please enter an encryption key: "))
 cfile.write(encryptor(str(raw_input("Username: ")),key)+"\n")
 cfile.write(encryptor(str(raw_input("Password: ")),key)+"\n")
 cfile.close()

if os.path.isfile("BotCreds.txt")==False:
 encodecreds()
uname,pwd=getcreds(str(raw_input("Enter credidential decryption key: ")))
bots=connect(search(getmyip("wlan0")),uname,pwd)
print(str(len(bots))+" active")

temp=""
if len(bots) > 0:
 print("Type exit to leave the interpreter")
while len(bots) > 0 :
  temp=str(raw_input(">>>"))
  if temp == "exit":
   break
  sendall(bots,temp)
for x in bots:
 print("Logging off "+x.ip+"...")
 x.logoff()
if len(bots) == 0:
 print("Incorrect credentials!")
elif temp=="exit":
 print("All bots logged off")
else:
 print("No bots available!")
