#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import re, sys, os
'''
Created on 25 apr 2016

@author: Thomas Bergqvist
''' 
maxlenght = 0
class Check_tmpl_and_prop(): 
    
    def __init__(self, fileo):
        self.__autogl = []
        self.__keyl = set()
        self.__prop = []
        self.__file = ""
        self.__fileo = fileo 
        try:            
            self.__file = [line.strip() for line in open(fileo, 'r')]                     
        except:
            print("Hittar inte " + fileo)
            sys.exit(1)
                                
    def get_prop(self):
        return self.__prop    
    def get_gv(self):
        return self.__autogl
    def get_kl(self):
        return self.__keyl
                           
    def set_prop(self):
        for line in self.__file:
            tmp = line.strip()
            if "=" in tmp and not tmp.startswith("#"):
                tmp = tmp.replace(" ", "")                            
                self.__prop.append(tmp[0:tmp.find("=")])
                                      
    def set_gv_and_kl(self):  
        for line in self.__file:
            tmp = line.strip()           
            if "@" not in tmp and "[" not in tmp and not tmp.startswith("#"):
                if tmp:
                    i1 = tmp.replace(" ", "").find("=")
                    self.__autogl.append(tmp[0:i1])           
            if "=" in tmp and "@" in tmp and not tmp.startswith("#"):
                tmp2 = str(re.findall(r'(@.*@)', tmp))
                keys = tmp.count("@")                                       
                if keys == 2:
                    i1 = tmp2.find("@")    
                    i2 = tmp2.find("@", i1 + 1 )
                    self.__keyl.add(tmp2[i1 + 1 : i2])                                         
                elif keys == 4:
                    i1 = tmp2.find("@")    
                    i2 = tmp2.find("@", i1 + 1 )
                    self.__keyl.add(tmp2[i1 + 1 : i2])
                    i3 = tmp2.find("@", i2 + 1)
                    i4 = tmp2.find("@", i3 + 1 )
                    self.__keyl.add(tmp2[i3 + 1 : i4])               
                else:
                    print("utesluter " + line )   
            
    def check_duplicates(self, lista):
        lista.sort()
        for i in range(0,len(lista)-1):
            if lista[i] == lista[i+1]:
                print(str(lista[i]).ljust(maxlenght) + " Ar en dubblett i " + self.__fileo)
        print("")
         
def getlongeststring(lenght):
    global maxlenght
    if len(lenght) > maxlenght:
        maxlenght = len(lenght)
                              
def main():  
    p = os.popen("echo $WAS_PROFILE")
    tmpprofile =  str((p.readline())) 
    profile = "/domains/was001/" + tmpprofile[tmpprofile.rfind("/") + 1:len(tmpprofile)]
    
    var1 = Check_tmpl_and_prop(profile.strip("\n") + "/xmlaccess/exp/local_configuration.tmpl")
    var1.set_gv_and_kl() 
    automatgenereradevarden_from_tmpl = var1.get_gv() #LIST
    map(getlongeststring, automatgenereradevarden_from_tmpl)
    nycklar_from_templ = var1.get_kl() #SET 
    var1.check_duplicates(automatgenereradevarden_from_tmpl)
     
    var2 = Check_tmpl_and_prop(profile.strip("\n") + "/config/exp/local_config.properties" )
    var2.set_prop()
    properties_from_local_prop = var2.get_prop()
    map(getlongeststring, properties_from_local_prop)
    var2.check_duplicates(properties_from_local_prop)    
    
    # Testa att värden som ska automatgenereras inte finns i properties
    for i in list(filter((lambda i: i in properties_from_local_prop), automatgenereradevarden_from_tmpl)):
        print(i.ljust(maxlenght) + " Kommer automatgenereras och behovs inte i " + profile.strip("\n") +"/config/exp/local_config.properties")
    print("")
    # Testa att alla nycklar från template finns i properties
    for j in list(filter((lambda j: j not in properties_from_local_prop), nycklar_from_templ)):
            print(j.ljust(maxlenght) + " Saknas i " + profile.strip("\n") +"/config/exp/local_config.properties")
    print("")
    #testa om det finns egendefinierade nycklar i properties som inte har någon kopplingg till template
    for k in list(filter((lambda k: k in properties_from_local_prop), automatgenereradevarden_from_tmpl)):
        properties_from_local_prop.remove(k)       
    for l in list(filter((lambda l: l not in nycklar_from_templ), properties_from_local_prop)):
        print(l.ljust(maxlenght)  + " Har ingen motsvarighet i " + profile.strip("\n") + "/xmlaccess/exp/local_configuration.tmpl")
    print("")
if __name__ == '__main__':
    main()
