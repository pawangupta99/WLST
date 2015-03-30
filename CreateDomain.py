
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport
    
import os



#=======================================================================================
# Open a domain template.
#=======================================================================================

beaHome="C:/Oracle/Middleware/Oracle_Home"
wlHome="C:/Oracle/Middleware/Oracle_Home/wlserver"
print "beaHome="+beaHome
print "wlHome="+wlHome

readTemplate(wlHome + "/common/templates/wls/wls.jar", "Compact" )

cd('Servers/AdminServer')
set('ListenAddress','')
set('ListenPort', 7001)

create('AdminServer','SSL')
cd('SSL/AdminServer')
set('Enabled', 'True')
set('ListenPort', 7002)

#=======================================================================================
# Define the user password for weblogic.
#=======================================================================================

cd('/')
cmo=cd('Security/base_domain/User/weblogic')
# Please set password here before using this script, e.g. cmo.setPassword('value')
cmo.setPassword('weblogic1')

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

setOption('OverwriteDomain', 'true')
writeDomain(beaHome + '/user_projects/domains/NextGenDomain')
closeTemplate()
print "script returns SUCCESS"   

#=======================================================================================
# Exit WLST.
#=======================================================================================

#startNodeManager(verbose='true',NodeManagerHome='C:\\Oracle\\Middleware\\Oracle_Home\\user_projects\\domains\\NextGenDomain\\nodemanager')
#nmConnect("weblogic","weblogic1","slc06xll.us.oracle.com",5556,"NextGenDomain",beaHome + '/user_projects/domains/NextGenDomain',"SSL")

#startServer("AdminServer", "NextGenDomain", "http://slc06xll.us.oracle.com:7001", "weblogic","weblogic1",beaHome + "\\user_projects\\domains\\NextGenDomain" )


exit()

