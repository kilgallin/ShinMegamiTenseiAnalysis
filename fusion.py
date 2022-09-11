#copyright 2012 Jonathan Kilgallin
#Using input Copyright 2010 Alexander Paul Kleinheider from gamefaqs.com
#Shin Megami Tensei: Devil Survivor Copyright 2009 Atlus Co.

import binascii, datetime, sys

def findDemon(name):
    for demon in demons:
        if demon["name"] == name:
            return demon

f = open("C:/python27/apps/shin megami tensei/fusion_list.htm")
raw = f.read()
f.close()
i = raw.find("| ")+2;
prev = -1
demons = []

while(i < len(raw)):
    if i <= prev:
        break
    prev = i
    
    lname = raw[i:raw.find(" :: ",i)]
    if lname[0] == ":":
        break
    i += len(lname) + 4    
    llevel = int(raw[i:raw.find(" ",i)])
    if raw.find(" :: ",i) > raw.find("\n",i):
        ldemon = {"name" : lname, "level" : llevel, "inputs" : []}
        line = raw[i:raw.find("\n",i)]
        i += len(line)+1
        line = raw[i:raw.find("\n",i)]
        i += len(line)+1
        while(True):
            line = raw[i:raw.find("\n",i)]
            if line[0] == ":":
                break
            linput1 = line[2:line.find(" + ")]
            linput2 = line[line.find(" + ")+3:line.find(" ",line.find(" + ")+3)]
            ldemon["inputs"].append((linput1,linput2))
            #print "linput1", linput1, "linput2", linput2, "rinput1", rinput1, "rinput2", rinput2
            i += len(line)+1
        #print ldemon
        demons.append(ldemon)
        i = raw.rfind("| ",0,raw.find(" :: ",i))+2
        continue
    i = raw.rfind("| ",0,raw.find(" :: ",i))+2
    rname = raw[i:raw.find(" :: ",i)]
    i += len(rname) + 4
    rlevel = int(raw[i:raw.find(" ",i)])
    #print "name", lname, rname, "level", llevel, rlevel
    ldemon = {"name" : lname, "level" : llevel, "inputs" : []}
    rdemon = {"name" : rname, "level" : rlevel, "inputs" : []}
    i = raw.find("\n",i)+1
    i = raw.find("\n",i)+1
    lend = False
    rend = False
    if i <= prev:
        break
    while(not lend or not rend):
        line = raw[i:raw.find("\n",i)]
        if line[0] == ":":
            lend = True
        if line[-1] == ":":
            rend = True
        #print "line", line
        if not lend:
            linput1 = line[2:line.find(" + ")]
            linput2 = line[line.find(" + ")+3:line.find("  ",line.find(" + ")+3)]
            ldemon["inputs"].append((linput1,linput2))
        if not rend:
            rinput1 = line[42:line.find(" + ",42)]
            rinput2 = line[line.find(" + ",42)+3:line.find("  ",line.find(" + ",42)+3)]
            rdemon["inputs"].append((rinput1,rinput2))
        #print "linput1", linput1, "linput2", linput2, "rinput1", rinput1, "rinput2", rinput2
        i += len(line)+1
    demons.append(ldemon)
    demons.append(rdemon)
    i = raw.rfind("| ",0,raw.find(" :: ",i))+2
    
print [demon for demon in demons]

if sys.argv[1] == "minlevel":
    demon = findDemon(sys.argv[2])
    print demon
    level = 100
    argmin = None
    for inputs in demon["inputs"]:
        linput = findDemon(inputs[0])
        #print "linput", linput["name"], inputs[0]
        rinput = findDemon(inputs[1])
        #print "rinput", inputs[1], rinput["name"]
        if linput["level"] < level and rinput["level"] < level:
            if linput["level"] < rinput["level"]:
                level = rinput["level"]
                argmin = rinput
            else:
                level = linput["level"]
                argmin = linput
    if demon["level"] > level:
        print level, argmin["name"]
        level = demon["level"]
        argmin = demon
    print "Governed by", level, argmin["name"]