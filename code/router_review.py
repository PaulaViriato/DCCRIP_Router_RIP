from datetime import datetime
from random import uniform
import sys
import os.path
import time
import json
import socket
import _thread

# Inicio da classe Device:
class Device:
    def __init__ (self, destiny, weight, source):
        self.destiny = destiny
        self.weight  = weight
        self.source  = source
        self.timer   = time.clock()

    def setDestiny (self, destiny):
        self.destiny = destiny

    def setWeight (self, weight):
        self.weight = weight

    def setSource (self, source):
        self.source = source

    def updateTimer (self):
        self.timer = time.clock()

    def getDestiny (self):
        return self.destiny

    def getWeight (self):
        return self.weight

    def getSource (self):
        return self.source

    def getTimer (self):
        return self.timer
# Fim da classe Device.

# Inicio da classe Route:
class Route:
    def __init__ (self):
        self.list = None
        
    def exists (self, destiny, source):
        if (self.list != None):
            if (source != None):
                for lst in self.list:
                    if ((lst.getDestiny() == destiny)and
                        (lst.getSource() == source)):
                        return lst
            else:
                for lst in self.list:
                    if (lst.getDestiny() == destiny):
                        return lst
        return False

    def add (self, destiny, weight, source):
        if (self.list != None):
            exis = self.exists (destiny, source)
            if (exis == False):
                devi = Device (destiny, weight, source)
                self.list.append (devi)
                printLog ("add "+destiny+" "+str(weight)+" "+source)
            else:
                exis.setWeight (weight)
                exis.updateTimer ()
                printLog ("update-timer "+destiny+" "+source)
        else:
            self.list = []
            devi = Device (destiny, weight, source)
            self.list.append (devi)
            printLog ("add "+destiny+" "+str(weight)+" "+source)
    
    def delt (self, destiny, source):
        exis = self.exists (destiny, source)
        if (exis != False):
            if (len(self.list) > 1): self.list.remove (exis)
            else: self.list = None
            printLog ("del "+destiny+" "+source)

    def getDestinies (self, source):
        rtrn = None
        
        lstroutes = self.getRoutes()
        if (lstroutes != None):
            if (source == None):
                for lst in self.getRoutes():
                    if (rtrn != None):
                        rtrn.append (lst.getDestiny())
                    else:
                        rtrn = []
                        rtrn.append (lst.getDestiny())
            else:
                for lst in self.getRoutes():
                    if (source == lst.getSource()):
                        if (rtrn != None):
                            rtrn.append (lst.getDestiny())
                        else:
                            rtrn = []
                            rtrn.append (lst.getDestiny())
        return rtrn
        
    def getRoutes (self):
        rtrn = None
        
        if (self.list != None):
            for lst in self.list:
                exis = 0
                if (rtrn != None):
                    for ret in rtrn:
                        if (lst.getDestiny() == ret.getDestiny()):
                            exis = 1
                            break
                    if (exis == 0):
                        less = (self.getLessRoute (lst.getDestiny()))[0]
                        rtrn.append (less)
                else:
                    rtrn = []
                    less = (self.getLessRoute (lst.getDestiny()))[0]
                    rtrn.append (less)
        return rtrn
    
    def getLessRoute (self, destiny):
        w    = 999999
        rtrn = None
        
        if (self.list != None):
            for lst in self.list:
                if (lst.getDestiny() == destiny):
                    if (lst.getWeight() < w):
                        w = lst.getWeight()
                        rtrn = []
                        rtrn.append (lst)
                    else:
                        if (lst.getWeight() == w):
                            rtrn.append (lst)
        return rtrn
    
    def getList (self):
        return self.list
# Fim da classe Route.

exit = False
stop = False
paus = False

receiv = []
server = ""
port   = 55151
mszudp = 65507
sock   = None

route  = Route()
pi     = 0

def cfnumber (number):
    if (number < 10): return "0"+str(number)
    else: return str(number)

def printLog (message):
    global server
    global paus
    
    while (paus == True):
        time.sleep(uniform(0,0.2))

    paus = True
    a_server = server.replace(".","")
    archive  = "log_"+a_server+".txt"
    archlog  = None
    
    datetim  = datetime.now()
    newmess  = "["+cfnumber(datetim.day)
    newmess += "-"+cfnumber(datetim.month)
    newmess += "-"+str(datetim.year)
    newmess += " "+cfnumber(datetim.hour)
    newmess += ":"+cfnumber(datetim.minute)
    newmess += ":"+cfnumber(datetim.second)
    newmess += "] "+message+"\n"
    
    content = []
    if (os.path.exists(archive)):
        archlog = open(archive, 'r')
        content = archlog.readlines()
        archlog.close()

    content.append (newmess)
    archlog = open(archive, 'w')
    archlog.writelines(content)
    archlog.close()
    paus = False

def packageSending (package):
    global server
    global route
    global port
    global sock

    while (sock == None):
        time.sleep(uniform(0,0.2))
        
    destiny = package["destination"]
    alterna = route.getLessRoute (destiny)
    main_ip = ""

    if (alterna != None):
        if (len(alterna) == 1):
            routeip = alterna[0]
            if (routeip.getSource() == server):
                main_ip = routeip.getDestiny()
            else: main_ip = routeip.getSource()
        else:
            value = len(alterna)
            while (value == len(alterna)):
                probabi = uniform(0,1)
                value = int(value*probabi)
            routeip = alterna[value]
            if (routeip.getSource() == server):
                main_ip = routeip.getDestiny()
            else: main_ip = routeip.getSource()
        
        message = json.dumps(package)
        encodes = bytes (message, "ascii")
        sock.sendto(encodes, (main_ip, port))
        printLog ("send-"+package["type"]+" "+main_ip)
    else: printLog ("invalid-sending-"+package["type"]+" "+destiny)

def packageReceiving ():
    global exit
    global stop
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server, port))

    while (exit == False):
        if (stop == False):
            package, recip = sock.recvfrom(mszudp)
            message = str(package)
            message = message[2:(len(message)-1)]
            printLog ("receive "+str(recip))
            receiv.append (message)
    
    sock.close()
    sock = None
    _thread.exit ()

def updateReceiv ():
    global receiv
    
    objlist = receiv
    size = len(objlist)
    if (size > 1):
        i = 0
        while (i < (size-1)):
            objlist[i] = objlist[i+1]
            i += 1
        objlist.remove(objlist[size-1])
    else: objlist = []
    receiv = objlist

def updateRoutes ():
    global route
    global server

    rtrn  = {}
    
    destinies = route.getDestinies(server)
    if (destinies != None):
        for destiny in destinies:
            update = {}
            update["type"]        = "update"
            update["source"]      = server
            update["destination"] = destiny

            distances = {}
            distances[server] = 0
            for lst in route.getRoutes():
                if ((lst.getDestiny() != destiny)and
                    (lst.getSource() != destiny)):
                    distances[lst.getDestiny()] = lst.getWeight()
            update["distances"]   = distances

            if (destiny != server): packageSending (update)
            else: rtrn = update

    return json.dumps(rtrn, indent=4)

def traceRoutes (destiny):
    trace = {}
    trace["type"]        = "trace"
    trace["source"]      = server
    trace["destination"] = destiny
    trace["hops"]        = []
    trace["hops"].append (server)
    packageSending (trace)

def updateLoads (received):
    global server
    global route
    
    source   = received["source"]
    less_dis = route.getLessRoute (source)
    
    if (less_dis != None):
        init_dis = less_dis[0].getWeight()
        distance = received["distances"]

        for dest in distance:
            if (dest != server):
                route.add (dest, (init_dis+distance[dest]), source)

def dataLoads (received):
    rec_txt = received["payload"]
    try:
        rec_loa = json.loads(rec_txt)
        message = json.dumps(rec_loa, indent=4)
        print (message)
    except Exception:
        print (rec_txt)

def traceLoads (received):
    global server
    rectrac = received
    rectrac["hops"].append(server)
    message = json.dumps(rectrac)
    
    dattrac = {}
    dattrac["type"]        = "data"
    dattrac["source"]      = server
    dattrac["destination"] = rectrac["source"]
    dattrac["payload"]     = message
    packageSending (dattrac)

def designator ():
    global server
    global receiv
    global route
    global exit
    global stop

    while (exit == False):
        if ((len(receiv) > 0)and(stop == False)):
            received = json.loads(receiv[0].replace("\\\\", "\\"))
            if (received["destination"] == server):
                if (received["type"] == "update"): updateLoads (received)
                if (received["type"] == "data"): dataLoads (received)
                if (received["type"] == "trace"): traceLoads (received)
            else:
                destination = received["destination"]
                destiny     = route.exists (destination, None)

                if (destiny == False):
                    daterro = {}
                    daterro["type"]        = "data"
                    daterro["source"]      = server
                    daterro["destination"] = received["source"]
                    daterro["payload"]     = "ERRO: Nao existe rota ate o "
                    daterro["payload"]    += "destino! Parada em: "+server
                    daterro["payload"]    += " - Destino: "+destination
                    packageSending (daterro)
                else:
                    retransm = received
                    if (retransm["type"] == "trace"):
                        retransm["hops"].append(server)                
                    packageSending (retransm)
            updateReceiv ()
    _thread.exit ()

def updateTimer (pi):
    global route
    global exit
    global stop

    initTime = time.clock()
    while (exit == False):
        current = time.clock()
        if (((current - initTime) >= pi)and(stop == False)):
            list_route = route.getList()
            if (list_route != None):
                for lst in list_route:
                    if ((current - lst.getTimer()) >= float(4*pi)):
                        route.delt (lst.getDestiny(), lst.getSource())
                updateRoutes ()
                initTime = current

    _thread.exit ()

def modifyAddr (newserver):
    global server
    global stop
    
    stop = True
    time.sleep(1.05)
    a_server = server.replace(".","")
    archive  = "log_"+a_server+".txt"

    content = []
    if (os.path.exists(archive)):
        archant = open(archive, 'r')
        content = archant.readlines()
        archant.close()
        os.remove(archive)

    list_route = route.getList()
    if (list_route != None):
        for lst in list_route:
            if (lst.getDestiny() == server):
                lst.setDestiny(newserver)
            if (lst.getSource() == server):
                lst.setSource(newserver)

    a_server = newserver.replace(".","")
    archive  = "log_"+a_server+".txt"
    if (os.path.exists(archive)): os.remove(archive)
    archnew  = open(archive, 'w')
    archnew.writelines(content)
    archnew.close()

    server = str(newserver)
    stop   = False
    printLog ("--modify-addr "+newserver)
    
def execCommands (command):
    global server
    global route
    global port
    global pi

    act = command.replace("\n","")
    act = act.split(" ")
    if (act[0] == "add"):
        if (len(act) == 3): route.add (act[1], int(act[2]), server)
        else: route.add (act[1], int(act[2]), act[3])
    elif (act[0] == "del"):
        if (len(act) == 2): route.delt (act[1], server)
        else: route.delt (act[1], act[2])
    elif (act[0] == "trace"):
        printLog ("trace "+str(act[1]))
        traceRoutes (str(act[1]))
    elif (act[0] == "--startup-commands"):
        archive = str(act[1])
        arch    = open(archive, 'r')
        archtxt = arch.readlines()

        printLog ("--startup-commands "+archive)
        for line in archtxt:
            execCommands (line)
        arch.close()
    elif (act[0] == "--update-period"):
        pi = float(act[1])
        printLog ("--update-period "+str(act[1]))
    elif (act[0] == "--update-port"):
        port = int(act[1])
        printLog ("--update-port "+str(act[1]))
    elif (act[0] == "--addr"):
        if (server == ""):
            server = str(act[1])
            printLog ("--addr "+str(act[1]))
        else: modifyAddr (act[1])
    elif ((act[0] == "quit")or(act[0] == "^C")):
        updtRoute = updateRoutes ()
        printLog ("quit")
        exit = True
    else: print ("Invalid command!")

# Inicio da funcao principal (main):
if __name__ == "__main__":
    global exit
    global pi

    execCommands ("--addr "+sys.argv[1])
    execCommands ("--update-period "+sys.argv[2])
    _thread.start_new_thread(packageReceiving, tuple([]))
    _thread.start_new_thread(designator, tuple([]))
    _thread.start_new_thread(updateTimer, tuple([pi]))
    try:
        execCommands ("--startup-commands "+str(sys.argv[3]))
    except Exception: exit = False

    while (exit == False):
        command = str(input())
        execCommands (command)
# Fim da funcao principal (main).
