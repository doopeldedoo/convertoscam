import os
import socket

Clocation = ('/etc/CCcam.cfg')
Olocation = ('/etc/tuxbox/config/oscam-emu/oscam.server')

print("This converter takes a CCcam.cfg and converts it into a oscam.server.")
print("It also tries to check if a connection works to minimize potential bad servers.")
print("It does not validate the user/pass combination.")

print("removing oscam.server if it exist")
if os.path.isfile(Olocation):
	os.remove(Olocation)
	print("removed oscam.server")

print("parsing CCcam.cfg")

f = open(Clocation)
print("reading and writing a new oscam.server file")
for line in f:
	if "C:" in line:
	    domain = line.split(' ')[1]
	    port = line.split(' ')[2]
	    user = line.split(' ')[3]
	    password = line.split(' ')[4]
	    
	    print("trying to connect...")
	    s = socket.socket()
	    s.settimeout(5)
	    try:
		    print(domain)
		    print(port)
		    s.connect((domain,int(port)))
	    except:
		    print("Connection Problem, trying next one")		
	    else:
	    	server = open(Olocation,"a")
	   	server.write("[reader]\n")
	    	server.write("label="+domain+"\n")
	    	server.write("enable=1\n")
	    	server.write("protocol=cccam\n")
	    	server.write("device="+domain+","+port+"\n")
	    	server.write("user="+user+"\n")
	    	server.write("password="+password+"\n")
	    	server.write("cccversion=2.3.2\n")
	    	server.write("group=1,2,3\n")
	    	server.write("inactivitytimeout=0\n")
	    	server.write("reconnecttimeout=20\n")
	    	server.write("ccckeepalive=1\n")
	    	server.write("lb_weight=100\n")
	    	server.write("cccmaxhops=10\n")
	    	server.write("ccckeepalive=1\n")
	    	server.write("cccwantemu=0\n")
	    	server.write('\n')
	    	server.close()
	    	print "+1"
	    finally:
		    s.close()
print "Process Complete,restarting softcam"
os.system("/etc/init.d/softcam restart")
