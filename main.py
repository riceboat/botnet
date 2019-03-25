from pexpect import pxssh
import os,nmap
s=pxssh.pxssh()
cport=8022
suffixes=[]
done=False
def command(s,cmd):
 print("Excecuting>>> "+cmd)
 s.sendline(cmd)
prefix=str(raw_input("Please enter the first three letters of your ip address or press enter for last used: "))
comd=str(raw_input("Please enter the command(s) you want to run: "))
out=str(raw_input("Display command output? y/n: "))
if out=="y":
 output=True
else:
 output=False
if prefix=="":
 f=open("lastused.txt","r")
 prefix=f.readline().strip()
else:
 if os.path.isfile('lastused.txt'):
  os.system("rm lastused.txt")
 f=open("lastused.txt","w")
 f.write(prefix)
f.close()
print("scanning for bots on "+prefix)
scanner=nmap.PortScanner()
scanner.scan(prefix+".0/24",str(cport))
suffixes=scanner.all_hosts()
for ip in suffixes:
 s=pxssh.pxssh()
 try:
    print("Connecting to > "+ip+"              *")
    s.force_password=True
    s.login(ip,"root","raspberry",port=cport)
    print("Logged in to "+ip+"                 *")
    command(s,comd)
    s.prompt()
    if out:
     print(s.before)
    s.logout()
 except:
  print("Host is down^")
