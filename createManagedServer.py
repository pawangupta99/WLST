
#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

print 'starting the script ....'
username = 'weblogic'
password = 'weblogic1'
url='t3://slc06xll.us.oracle.com:7001'

connect(username,password,url)


edit()
startEdit()


    
 
 
#Set the managed server and machine variables
createNewManagedServer = True
createNewMachine = True
machineName = "slc06xll.us.oracle.com"
targetServerName = "IM1"
machine = None
target = None
     
    #--------------------------------------------------------------------------------------
    #Function definitions for creating a managed server
    #--------------------------------------------------------------------------------------
     
    #Function to create a new machine
def createMachine():
    global machine
         
    print("Creating a new machine named "+machineName)
    try: 
        cd('/')
        edit()
        startEdit()
        machine = cmo.createMachine(machineName)
        cd('/Machines/' + machineName+'/NodeManager/'+machineName)
        cmo.setListenAddress(machineName)
        save()
    except:
        dumpStack()
        print("\n\nERROR: Could not create a new machine named "+machineName)
        stopEdit("y")
        disconnect()
        raise Exception
    else:
        try:
            activate(block="true")
            print("Done creating a new machine named "+machineName)
        except:
            dumpStack()
            print("\n\nERROR: Could not activate the changes from creating a new machine named "+machineName)
            print("\tUndoing changes")
            undo("true", "y")
            stopEdit("y")
            disconnect()
            raise Exception
        #End function createMachine()
     
    #Function to determine whether to create a new machine or use the existing one
    def handleMachine():
        global machineName
        global machine
         
             
    if createNewMachine:
            #Check for an existing machine with the same name first
        try:
            print("Checking for existing machine named "+machineName)
            cd("Machines/"+machineName)
            machine=cmo
        except:
                dumpStack()
                print("\nINFO: There is no existing machine named: "+machineName+".")
        else:
                print("Found machine named "+machineName)
                print("\nWARNING: Using existing machine instead of creating it.")
     
            #If we couldn't find an existing machine, continue to create the new one
        if(machine == None):
                createMachine()
        else:
            try:
                print("Searching for machine named "+machineName)
                cd("Machines/"+machineName)
                machine=cmo
            except:
                dumpStack()
                print("\nWARNING: Could not find existing machine named: "+machineName+".")
                createMachine()
            else:
                print("Found machine named "+machineName)
        #End function handleMachine()
     
    #Function to create a new managed server
    def createManagedServer():
        global target
         
        print("Creating a new managed server named "+targetServerName)
         
        try:
            #Return to the domain edit position
            cd('/')
            #Turn edit mode back on
            edit()
            startEdit()
             
            target = cmo.createServer(targetServerName)
            target.setListenAddress(machineName)
            target.setListenPortEnabled(True)
            target.setListenPort(8226)
             
            #argsProperties = os.path.join(instancePath, "serverStartArguments.properties")
            #argsFile = open(argsProperties, "r")
             
            #allLines = argsFile.readlines()
            #argsFile.close()
             
            #newArgs = ""
            #for line in allLines:
                #newArgs = newArgs + " " + line
             
            #target.getServerStart().setArguments(newArgs)
             
            #binDirectory = os.path.join("C:\\Oracle\\Knowledge\\IMss", "bin")
             
            #classpathProperties = os.path.join(binDirectory, "serverStartClasspath.properties")
            #classpathFile = open(classpathProperties, "r")
             
            #allLines2 = classpathFile.readlines()
            #classpathFile.close()
             
            #classpath = ""
            #for line in allLines2:
               # classpath = classpath + line + ";"
             
            #target.getServerStart().setClassPath(classpath)
             
            target.setMachine(machine)
             
            #save and activate the changes
            save()
        except:
            dumpStack()
            print("\n\nERROR: Could not create a new managed server named "+targetServerName)
            stopEdit("y")
            disconnect()
            raise Exception
        else:
            try:
                activate(block="true")
                print("Done creating a new managed server named "+targetServerName)
            except:
                dumpStack()
                print("\n\nERROR: Could not activate the changes from creating a new managed server named "+targetServerName)
                print("\tUndoing changes")
                undo("true", "y")
                stopEdit("y")
                disconnect()
                raise Exception
        #End function createManagedServer
 
    #--------------------------------------------------------------------------------------
    #Set the target Managed Server
    #--------------------------------------------------------------------------------------
     
    if createNewManagedServer:
         
        try:
            print("Checking for existing managed server named "+targetServerName)
             
            cd("Servers/"+targetServerName)
            target=cmo
        except:
            dumpStack()
            print("\nINFO: Could not find existing managed server named: "+targetServerName+".")
        else:
            print("Found managed server named "+targetServerName)
            print("\nWARNING: Using existing managed server instead of creating it.")
         
        #If we couldn't find an existing managed server, continue to create the new one
        if target == None:
            #Make sure the machine exists before we create the server
            handleMachine()
            createManagedServer()
    else:
        try:
            print("Searching for managed server named "+targetServerName)
             
            cd("Servers/"+targetServerName)
            target=cmo
        except:
            dumpStack()
            print("\nWARNING: Could not find existing managed server named: "+targetServerName+".")
             
            #If we couldn't find the existing managed server, attempt to create it
            #Make sure the machine exists before we create the server
            handleMachine()
            createManagedServer()
        else:
            print("Found managed server named "+targetServerName)   
 



try:
    save()
    activate(block="true")
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to save and/or activate!!!"
    dumpStack()
    raise 
    
