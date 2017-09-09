import json
import requests
import sys, os
from uuid import getnode as get_mac

ETC_HOSTS="/etc/hosts"
ETC_HOSTNAME="/etc/hostname"
DOMAIN_NAME = "conf" # must be written in lower-case
confHostname = ""

cwd = os.path.dirname(sys.argv[0])

mac = get_mac()
macString = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

with open(cwd + '/' + DOMAIN_NAME + '.json', 'r') as f:
    data = json.load(f)
    f.close()
        
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

if confHostname:
    with open(ETC_HOSTNAME, 'w') as f:
        f.write(confHostname + '\n')
        f.close()

    with open(ETC_HOSTS, 'r') as fp:
        lines = fp.read().split("\n")
        fp.close()

    with open(ETC_HOSTS, 'w') as fp:    
        for i in lines:
            if '127.0.1.1' in i and DOMAIN_NAME in i:
                #print ('127.0.1.1\t' + confHostname)
                fp.write ('127.0.1.1\t' + confHostname+'\n')
            else:
                if i:
                    #print (i)        
                    fp.write (i+'\n')               
        fp.close()
        #os.system('sudo shutdown -r now')
        os.system('hostnamectl set-hostname ' + confHostname)
