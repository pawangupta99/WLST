
#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport






#############################################################################
#
# @author Copyright (c) 2010 - 2011 by Middleware Magic, All Rights Reserved.
#
#############################################################################
from java.io import FileInputStream
import java.lang
import os
import string

propInputStream = FileInputStream("domains.properties")
configProps = Properties()
configProps.load(propInputStream)

Username = configProps.get("username")
Password = configProps.get("password")
Host = configProps.get("host")
nmPort = configProps.get("nm.port")
domainName = configProps.get("domain.name")
domainDir = configProps.get("domain.dir")
nmType = configProps.get("nm.type")

startNodeManager()
print ''
print '============================================='
print ' NODE MANAGER started Successfully...!!!'
print '============================================='
print ''
nmConnect(Username,Password,Host,nmPort,domainName,domainDir,nmType)
print ''
print '============================================='
print 'Connected to NODE MANAGER Successfully...!!!'
print '============================================='
print ''

serverName = configProps.get("server.name")
print '###### serverName = ', serverName
#nmStart(serverName)
serverName = configProps.get("server.name")
print ''
print '============================================='
print '===> Successfully started ', serverName, '  <==='
print '============================================='
print ''


















try:
    save()
    activate(block="true")
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to save and/or activate!!!"
    dumpStack()
    raise 
    
