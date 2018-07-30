import json
import requests
import sys, os
from uuid import getnode as get_mac


interfaces = [ "eth0", "wlan0" ]
#interfaces = [ "wlan0", eth0" ]
confHostname = ""
linkInterface=""

ETC_HOSTS="/etc/hosts"
ETC_HOSTNAME="/etc/hostname"
DOMAIN_NAME = "conf" # must be written in lower-case

def getMac(interface):

  try:
    mac = open('/sys/class/net/' + interface + '/address').readline().upper()
  except:
    mac = "00:00:00:00:00:00"
  
  return mac[0:17]


def checkLink (interface):
  
  hostname="www.google.de"
  osCmd = 'ping -c1 -w1 -4 -I' + interface + ' ' + hostname + ' > /dev/null'
  
  #print (osCmd)
  rep = os.system (osCmd)

  if rep==0:
    #print (interface + " has link")
    return interface
  else:
    #print (interface + " is down")
    return ""

cwd = os.path.dirname(sys.argv[0])

while not linkInterface:
  linkInterface = checkLink(interfaces[0]) 
  if not linkInterface:
    linkInterface = checkLink(interfaces[1])
  
#print (linkInterface)
macString = getMac (linkInterface)
#print (macString)

#mac = get_mac()
#macString = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
#print ("MAC-Addr: " + macString)

with open(cwd + '/' + DOMAIN_NAME + '.json', 'r') as f:
    data = json.load(f)
    f.close()

    #print ("os.uname:" + os.uname()[1])
        
try:
    if os.uname()[1] != data[DOMAIN_NAME][macString]:
        #we need to set a new hostname
        confHostname = data[DOMAIN_NAME][macString]
except:
    print("Keine passende MAC-Adresse gefunden")

#url = 'https://your.domain.here/yourfile.json'

#r = requests.get(url)
#dataUrl = json.loads(r.content.decode())
#print (dataUrl["DOMAIN_NAME"][macString] + " > " + ETC_HOSTNAME )

#print ("confHostname " + confHostname)

if confHostname:
    with open(ETC_HOSTNAME, 'w') as f:
        f.write(confHostname + '\n')
        f.close()

    with open(ETC_HOSTS, 'r') as fp:
        lines = fp.read().split("\n")
        fp.close()

    with open(ETC_HOSTS, 'w') as fp:    
        for i in lines:
            if '127.0.1.1' in i and not 'localhost' in i:
                #print ('127.0.1.1\t' + confHostname)
                fp.write ('127.0.1.1\t' + confHostname+'\n')
            else:
                if i:
                    #print (i)        
                    fp.write (i+'\n')               
        fp.close()

###
#
# final commands to execute
#
###
        os.system('hostnamectl set-hostname ' + confHostname)
