# Copyright (c) 2002, 2012 Oracle and/or its affiliates. All rights reserved.
# Oracle and Java are registered trademarks of Oracle and/or its affiliates. Other names may be trademarks of their respective owners.
# 
# This software and related documentation are provided under a license agreement containing restrictions 
# on use and disclosure and are protected by intellectual property laws. Except as expressly permitted 
# in your license agreement or allowed by law, you may not use, copy, reproduce, translate, broadcast, modify, 
# license, transmit, distribute, exhibit, perform, publish or display any part, in any form, or by any means. 
# Reverse engineering, disassembly, or decompilation of this software, unless required by law for interoperability, is prohibited.
# 
# The information contained herein is subject to change without notice and is not warranted to be error-free. If you find any errors, please report them to us in writing.
# 
# If this is software or related documentation that is delivered to the U.S. Government or anyone licensing it on behalf of the U.S. Government, the following notice is applicable:
# 
# U.S. GOVERNMENT END USERS: Oracle programs, including any operating system, integrated software, 
# any programs installed on the hardware, and/or documentation, delivered to U.S. Government end users are "commercial computer software" 
# pursuant to the applicable Federal Acquisition Regulation and agency-specific supplemental regulations. As such, use, duplication, 
# disclosure, modification, and adaptation of the programs, including any operating system, integrated software, any programs installed 
# on the hardware, and/or documentation, shall be subject to license terms and license restrictions applicable to the programs. No other rights are granted to the U.S. Government.
# 
# This software or hardware is developed for general use in a variety of information management applications. It is 
# not developed or intended for use in any inherently dangerous applications, including applications that may create a risk of 
# personal injury. If you use this software or hardware in dangerous applications, then you shall be responsible to take all 
# appropriate fail- safe, backup, redundancy, and other measures to ensure its safe use. Oracle Corporation and its affiliates 
# disclaim any liability for any damages caused by use of this software or hardware in dangerous applications.
# 
# This software or hardware and documentation may provide access to or information on content, products and services from third parties. 
# Oracle Corporation and its affiliates are not responsible for and expressly disclaim all warranties of any kind with respect to 
# third-party content, products, and services. Oracle Corporation and its affiliates will not be responsible for any loss, costs, 
# or damages incurred due to your access to or use of third-party content, products, or services. 

#---------------------------------------------------------------------------------------------
#Oracle Knowledge 8.6.0.0 - deployIMApps.py
#
#This script will deploy the Oracle Knowledge Applications to the specified Web Logic Domain
#
#---------------------------------------------------------------------------------------------

import os, shutil
from java.lang import System
from wlstModule import *#@UnusedWildImport

#set the exit code to zero to indicate a success
exitCode=0

wlsOutputFile = None
logFile = None

try:
    instanceName = "InfoManager"
    instancePath = "C:\\Oracle\\Knowledge\\IM\\instances\\InfoManager"
    
    #Create the log files
    wlsOutput = os.path.join("C:\\Oracle\\Knowledge\\IM\\InfoManager\\logs", "deployIMApps.out")
    log = os.path.join("C:\\Oracle\\Knowledge\\IM\\InfoManager\\logs", "deployIMApps.log")

    wlsOutputFile = open(wlsOutput, "w+")
    logFile = open(log, "w+")
    
    def printLog(message):
        print(message)
        logFile.write("\n"+message)
        return
    

    #--------------------------------------------------------------------------------------
    #Decrypt the admin server and managed server credentials
    #--------------------------------------------------------------------------------------
    encryptedAdminUser = "74w1eL8hPM4NnGKeyCKdBDySEnmxynJOeuWNGh614VI\="
    encryptedAdminPassword = "x3lfFHb4KiHmK0xZTQ6EnVP+M7h1uxn0Hz7wC836Es4\="
    
    encryptedMgdServerUser = "/N9rsTtmXnFkjbETnmDSGWQnPQSt2lzJH3jd4KiKx4M\="
    encryptedMgdServerPassword = "Wfa4myWfVjggDfYgi8eRThpK4soJkevvUqa/WWYNKqQ\="
    
    
    #--------------------------------------------------------------------------------------
    #Connect to the Domain - Allow the user to provide the credentials via command line
    #--------------------------------------------------------------------------------------

    redirect(wlsOutput, "true")

    printLog("Oracle Knowledge will deploy the applications to the following WebLogic Domain:")
    printLog("\tC:\\Oracle\\Middleware\\Oracle_Home\\user_projects\\domains\\base_domain\n\n")

    adminURL = "t3://slc06xll:7001"
    
    try:
        connect("weblogic", "weblogic1", adminURL)
    except:
        dumpStack()
        printLog("\n\nERROR: Failed to connect to the WebLogic Domain Server.")
        printLog("\tPlease make sure your Server is running before running this script.")
        raise Exception
    
    try:
        #Turn on edit mode
        edit()
    except:
        dumpStack()
        printLog("\n\nERROR: Could not edit the domain")
        disconnect()
        raise Exception
    
    
    
        #End function createMachine()
    
    
    #--------------------------------------------------------------------------------------
    #Create the Boot Identity file
    #--------------------------------------------------------------------------------------
    printLog("Creating a Boot Identity file at: C:\\Oracle\\Knowledge\\IM\\instances\\InfoManager\\boot.properties")
    bootIdentity = "C:\\Oracle\\Knowledge\\IM\\instances\\InfoManager\\boot.properties"
    
    bootIdentityFile = open(bootIdentity, "w+")
    bootIdentityFile.write("username="+encryptedMgdServerUser+"\n")
    bootIdentityFile.write("password="+encryptedMgdServerPassword+"\n")
    bootIdentityFile.close()
    
    printLog("Done creating Boot Identity file.")
    

    #--------------------------------------------------------------------------------------
    #Defining the application deployment function
    #--------------------------------------------------------------------------------------
    def deployApplication(applicationName, fullApplicationNameForLog):
        printLog("Deploying " + fullApplicationNameForLog)

        try:
            rootPath = os.path.join(instancePath, "webapps", applicationName)
            appPath = os.path.join(rootPath, "app")
            planPathXML = os.path.join(rootPath, "plan", "plan.xml")
            deploy(applicationName, appPath, targets="IM_Cluster", stageMode="nostage", planPath=planPathXML)
        except:
            dumpStack()
            printLog("\n\nERROR: Could not deploy " + fullApplicationNameForLog)
            disconnect()
            raise Exception
        else:
            printLog("Done deploying " + fullApplicationNameForLog)

    
    #--------------------------------------------------------------------------------------
    #Deploy InfoManager
    #--------------------------------------------------------------------------------------
    installInfoManager = 'Yes'
    if installInfoManager == 'Yes':
        deployApplication("InfoManager", "the Oracle Knowledge Management Console")
        
        
    #--------------------------------------------------------------------------------------
    #Deploy IMWS
    #--------------------------------------------------------------------------------------
    installIMWS = False
    if installIMWS:
        deployApplication("imws", "the Oracle Knowledge Web Services")


    #--------------------------------------------------------------------------------------
    #Deploy InfoCenter
    #--------------------------------------------------------------------------------------
    installInfoCenter = 'No'
    if installInfoCenter == 'Yes':
        deployApplication("infocenter", "InfoCenter")
        
    #--------------------------------------------------------------------------------------
    #Deploy iConnect
    #--------------------------------------------------------------------------------------
    installIConnect = 'No'
    if installIConnect == 'Yes':
        deployApplication("iconnect", "iConnect")
    
    
    #--------------------------------------------------------------------------------------
    #Deploy SSP
    #--------------------------------------------------------------------------------------
    installSSP = 'No'
    if installSSP == 'Yes':
        deployApplication("ssp", "SSP")
    
    
    #--------------------------------------------------------------------------------------
    #Deploy Content Resource Mount Point
    #--------------------------------------------------------------------------------------
#     installOKResourcesApp = False
#     if installOKResourcesApp:
#         appName = "OKResources"
#         
#         printLog("Checking for existing app: "+appName)
#         #Return to the domain edit position
#         cd('/')
#         #Turn edit mode back on
#         try:
#             edit()
#             startEdit()
#         except:
#             stopEdit("y")
#             disconnect()
#             raise Exception
#         else:            
#             try:
#                 cd("AppDeployments/"+appName)
#             except:
#                 stopEdit("y")
#                 deployApplication(appName, appName)
#             else:
#                 #Distribute the existing app onto this server
#                 existingApp = cmo
#                 targetServers = existingApp.getTargets()
#                 alreadyTargetedToThisServer = False
#                 for server in targetServers:
#                     if server.getName() == targetServerName:
#                         alreadyTargetedToThisServer = True
#                         break
#                 
#                 if alreadyTargetedToThisServer == False:
#                     printLog("Distributing existing app '"+appName+"' to "+targetServerName)
#                     existingApp.addTarget(target)
#                     
#                     try:
#                         #save and activate the changes
#                         save()
#                     except:
#                         dumpStack()
#                         printLog("\n\nERROR: Could not distribute existing app '"+appName+"' to "+targetServerName)
#                         stopEdit("y")
#                         disconnect()
#                         raise Exception
#                     else:
#                         try:
#                             activate(block="true")
#                             printLog("Done distributing existing app '"+appName+"' to "+targetServerName)
#                         except:
#                             dumpStack()
#                             printLog("\n\nERROR: Could not activate the changes from distributing existing app '"+appName+"' to "+targetServerName)
#                             printLog("\tUndoing changes")
#                             undo("true", "y")
#                             stopEdit("y")
#                             disconnect()
#                             raise Exception
#                 else:
#                     stopEdit("y")    
    
    #--------------------------------------------------------------------------------------
    #Disconnect from the Domain
    #--------------------------------------------------------------------------------------
    try:
        edit()
        startEdit()
        activate()
        disconnect()
    except:
        printLog("\n\nERROR: Could not disconnect from the WebLogic Domain")
        disconnect()
        raise Exception

    printLog("SUCCESS: Oracle Knowledge Applications successfully deployed")

except:
    print("FAILED: Oracle Knowledge Applications could be not successfully deployed")
    
    #close the log files
    if wlsOutputFile is not None:
        wlsOutputFile.close()
        
    if logFile is not None:
        logFile.write("\nFAILED: Oracle Knowledge Applications could be not successfully deployed")
        logFile.close()
        
    #Set the exit code to one to indicate a failure
    exitCode=1
else:
    #close the log files
    wlsOutputFile.close()
    logFile.close()
    
System.exit(exitCode)
#--------------------------------------------------------------------------------------
#
#End Script
#
#-------------------------------------------------------------------------------------
