
#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport
    

from java.util import *
from java.io import FileInputStream
from javax.management import *
import javax.management.Attribute
import sys
from wlstModule import *#@UnusedWildImpor

print 'starting the script ....'
username = 'weblogic'
password = 'weblogic1'
url='t3://localhost:7001'

connect('weblogic','weblogic1','t3://slc06xll.us.oracle.com:7001')



def createMachine():
        global machine
        
        print("Creating a new machine named "+machineName)
        try:
            #Return to the domain edit position
            cd('/')
            #Turn edit mode back on
            
            
            
            machine=create(machineName, 'Machine')
            #cd('/Machines/' + machineName+'/NodeManager/'+machineName)
            #cmo.setListenAddress(machineName)
            
            #save and activate the changes
            return machine
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
        
        machineName ="slc07ehb.us.oracle.com"
        machine="none"
        try:
            print("Checking for existing machine named "+machineName)
            cd("Machines/"+machineName)
            ls()
            machine="true" 
            return machine
            
            
        except:
                dumpStack()
                print("\nINFO: There is no existing machine named: "+machineName+".")
        else:
                print("Found machine named "+machineName)
                print("\nWARNING: Using existing machine instead of creating it.")
                #machine="Exist"
        if(machine == "none"):
                createMachine()
        #End function handleMachine()
    
    #Function to create a new managed server
print "tryiing to creating a new machine"    



try:
    edit()
    startEdit()
    ms = create("hello",'Server')
    machine
    ms.setmachine(machine)
    
    activate(block="true")
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to save and/or activate!!!"
    dumpStack()
    raise 
    
