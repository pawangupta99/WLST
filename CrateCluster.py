

from java.util import *
from java.io import FileInputStream
from javax.management import *
import javax.management.Attribute
import sys
from wlstModule import *#@UnusedWildImport
 
envproperty="config.properties"




 
propInputStream=FileInputStream(envproperty)
configProps=Properties()
configProps.load(propInputStream)
 
def getp(x):
    return configProps.get(x)
  
 
def logLevel(ms, k):
    lg = ms.getLog()
    lg.setFileName(''+domainHome+'/logs/bea/ms'+str(k)+'_'+domainName+'.log')
    lg.setLogFileSeverity('Info')
    lg.setRotationType('byTime')
    lg.setRotationTime("23:59")
    lg.setFileTimeSpan(24)
    lg.setDomainLogBroadcastSeverity('Error')
    lg.setMemoryBufferSeverity('Error')
    lg.setRedirectStdoutToServerLogEnabled(true)
    lg.setRedirectStderrToServerLogEnabled(true)
    lg.setStdoutSeverity('Error')
  
def setDiagnostics(ms, k):
    svrdiag = ms.getServerDiagnosticConfig()
    svrdiag.setDiagnosticContextEnabled(false)
    svrdiag.setDiagnosticStoreDir(''+domainHome+'/logs/store/diagnostics/ms'+str(k)+'_'+domainName+'/')
    defFileStore = ms.getDefaultFileStore()
    defFileStore.setDirectory(''+domainHome+'/logs/store/default/ms'+str(k)+'_'+domainName+'/')
    hvDataRetire = svrdiag.createWLDFDataRetirementByAge("HarvestDataRetirePolicy")
    hvDataRetire.setArchiveName(""+getp("ms_harvesarchivename")) 
    hvDataRetire.setEnabled(bool(getp("ms_harvesenabled")))
    hvDataRetire.setRetirementAge(int(getp("ms_harvesretireage")))
    hvDataRetire.setRetirementPeriod(int(getp("ms_harvesretireperiod")))
    hvDataRetire.setRetirementTime(int(getp("ms_harvesretiretime")))
 
    eventDataRetire = svrdiag.createWLDFDataRetirementByAge("EventDataRetirePolicy")
    eventDataRetire.setArchiveName(""+getp("ms_evtarchivename"))
    eventDataRetire.setEnabled(bool(getp("ms_evtenabled")))
    eventDataRetire.setRetirementAge(int(getp("ms_evtretireage")))
    eventDataRetire.setRetirementPeriod(int(getp("ms_evtretireperiod")))
    eventDataRetire.setRetirementTime(int(getp("ms_evtretiretime")))
 
def webserver_log(ms, k):
    wbsvr = ms.getWebServer()
    wbsvr.setPostTimeoutSecs(30)
    wbsvrlog = wbsvr.getWebServerLog()
    wbsvrlog.setFileName(''+domainHome+'/logs/ms'+str(k)+'_'+domainName+'_access.log')
    wbsvrlog.setLoggingEnabled(bool(getp("ms_accesslogenabled")))
    wbsvrlog.setLogFileFormat(""+getp("ms_accesslogformat"))
    wbsvrlog.setELFFields(""+getp("ms_extlogfomart"))
    wbsvrlog.setRotationType('byTime')
    wbsvrlog.setRotationTime("23:59")
    wbsvrlog.setFileTimeSpan(24)
 
 


def setServerStartArugments(ms):
        argsProperties ="serverStartArguments.properties"
        argsFile = open(argsProperties, "r")
        allLines = argsFile.readlines()
        argsFile.close()
        newArgs = ""
        for line in allLines:
            newArgs = newArgs + " " + line
        ms.getServerStart().setArguments(newArgs)
            
 
def setServerClassPath(ms):
        classpathProperties = "serverStartClasspath.properties"
        classpathFile = open(classpathProperties, "r")
        allLines2 = classpathFile.readlines()
        classpathFile.close()
        classpath = ""
        for line in allLines2:
            classpath = classpath + line + ";"
        ms.getServerStart().setClassPath(classpath)
           




#################Creating machine configurationss##############################

def createMachine(hostName,ms):
    
    machineName=hostName
    try: 
        cd('/')
        #edit()
        #startEdit()
        machine=create(machineName, 'Machine')
        print "***************************************************************************"
        #machine.getNodeManager().setNMType('plain')
        machine.getNodeManager().setListenAddress(hostName)
        ms.setMachine(machine)
        return machine
        
    except:
        dumpStack()
        print("\n\nERROR: Could not create a new machine named "+machineName)
        #stopEdit("y")
        disconnect()
        raise Exception
    else:
        try:
            #activate(block="true")
            print("Done creating a new machine named "+machineName)
            return machine
        except:
            dumpStack()
            print("\n\nERROR: Could not activate the changes from creating a new machine named "+machineName)
            print("\tUndoing changes")
            #undo("true", "y")
            #stopEdit("y")
            disconnect()
            raise Exception

def handleMachine(hostName,ms):
        #global machineName
        #global machine
        
        machineName=hostName
        alreadyExistingMachine="false"
        try:
            print("Checking for existing machine named "+machineName)
            cd("Machines/"+machineName)
            
            machine=cmo
            ms.setMachine(machine)
            alreadyExistingMachine="true"
            return machine
        except:
                dumpStack()
                print("\nINFO: There is no existing machine named: "+machineName+".")
        else:
                print("Found machine named "+machineName)
                print("\nWARNING: Using existing machine instead of creating it.")
                #machine="Exist"
        if(alreadyExistingMachine == "false"):
                createMachine(hostName,ms)

####End machine handling code




 
#####################################################################################
#  MANAGED SERVER CONFIGURATIONS
###################################################################################
 
def create_ms(k,hostName):
    cd('/')
    ms = create(""+getp("man"+str(k)),'Server')
    ms.setListenAddress(""+getp("ms_listenaddress"+str(k)))
    ms.setListenPort(int(getp("ms_listenport"+str(k))))
    ms.setWeblogicPluginEnabled(bool(getp("ms_defaultwlplugin")))
    ms.setMaxOpenSockCount(int(getp("ms_maxopensockcount")))
    ms.setNativeIOEnabled(bool(getp("ms_nativeioenabled")))
    ms.setStuckThreadMaxTime(int(getp("ms_stuckthreadmaxtime")))
    ms.setStuckThreadTimerInterval(int(getp("ms_stuckthreadtimerinterval")))
    ms.setLowMemoryGCThreshold(int(getp("ms_lowmemorygcthreshold")))
    ms.setLowMemorySampleSize(int(getp("ms_lowmemorysamplesize")))
    ms.setLowMemoryTimeInterval(int(getp("ms_lowmemorytimeinterval")))
    ms.setStagingMode(""+getp("ms_stagingmode"))
    ms.setAcceptBacklog(int(getp("ms_acceptbacklog")))
    ms.setLoginTimeoutMillis(int(getp("ms_logintimeoutmillis")))
    ms.setManagedServerIndependenceEnabled(bool(getp("ms_managedserverindependenceenabled")))
    ms.setTransactionLogFilePrefix(""+getp("ms_transactionlogfileprefix"))
    machine=handleMachine(hostName,ms)
    #assign('Server', ms,'Machine',machine)
#     ms.setMachine(machine)
    ####Setting server arguments for each of the manage servers
    setServerStartArugments(ms)
    setServerClassPath(ms)
    print ' ******* SETTTING MANAGED SERVER ATTRIBUTES for *********** '+getp("man"+str(k))
    ms.setReplicationGroup('Rep'+str(k))
    ms.setPreferredSecondaryGroup('Rep'+str(int(k)+1))
    
    logLevel(ms, k)
    setDiagnostics(ms, k)
    webserver_log(ms, k)
    ms.setCluster(clusTgt)
    return ms
    
  
################ main program ####################################################
domainName=getp("domainName")
adminServerListenaddr=getp("adminServerListenaddr")
admin_listerport=getp("admlistenport")
adminURL="t3://"+adminServerListenaddr+":"+str(admin_listerport)
domainHome=getp("domainHome")
 
adminUser=getp("adminUser")
adminPassword=getp("adminPassword")
userConfigFile=""+domainHome+"/bin/userconfigfile.secure"
userKeyFile=""+domainHome+"/bin/userkeyfile.secure"
 
adminServerName=getp("adminServerName")
clusterName=getp("clusterName")
numMS=getp("total_mansrvr")
 

#####################################################################################
#  CLUSTER CONFIGURATIONS
#####################################################################################
print ' ******* CREATING CLUSTER *********** '
connect(adminUser,adminPassword,adminURL)
edit()
startEdit()

cd('/')
print "clusname ******" + str(clusterName)

#clu = cmo.createCluster(""+clusterName
clu = create(clusterName,'Cluster')
isMulticastTrue=getp("isMulticastTrue")
if (isMulticastTrue == "true"):
    clu.setMulticastAddress(getp("multi_address"))
    clu.setMulticastPort(getp("multi_port"))
else:
    clu.setClusterMessagingMode('unicast')
 
clu.setWeblogicPluginEnabled(true)
clu.setClusterAddress(getp("ms_listenaddress1")+":"+getp("ms_listenport1")+","+getp("ms_listenaddress2")+":"+getp("ms_listenport2")+","+getp("ms_listenaddress3")+":"+getp("ms_listenport3"))
cd('/Clusters/'+clusterName)
clusTgt = clu
print "clusterName ****" +str(clusterName)+ "*******"+str(clusTgt)
cd('/')
for k in range(1, int(numMS)+1): 
    print getp("man"+str(k))
    hostName=getp("ms_listenaddress"+str(k))
    print "hostnaamme****************"+hostName
    #machine=handleMachine(hostName)
    create_ms(k,hostName)
    
    
     






cd('/')



try:
    save()
    activate(block="true")
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to save and/or activate!!!"
    dumpStack()
    raise 
    
