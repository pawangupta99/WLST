
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

# This example script:
# * connects WLST to the Admin Examples Server
# * starts an edit session
# * creates 10 managed servers.
# * It creates 2 clusters and assigns the servers to the respective clusters.

from java.util import *
from javax.management import *
import javax.management.Attribute

print 'starting the script ....'
username = 'weblogic'
password = 'welcome1'
url='t3://localhost:7001'

clusters = 'cluster1','cluster2'
ms1 = {'managed1':7701,'managed2':7702,'managed3':7703, 'managed4':7704, 'managed5':7705}
ms2 = {'managed6':7706,'managed7':7707,'managed8':7708, 'managed9':7709, 'managed10':7710}

connect(username,password,url)

clustHM = HashMap()
edit()
startEdit()

for c in clusters:
    print 'creating cluster '+c
    clu = create(c,'Cluster')
    clustHM.put(c,clu)

cd('..\..')

clus1 = clustHM.get(clusters[0])
clus2 = clustHM.get(clusters[1])

for m, lp in ms1.items():
    managedServer = create(m,'Server')
    print 'creating managed server '+m
    managedServer.setListenPort(lp)
    managedServer.setCluster(clus1)

for m1, lp1 in ms2.items():
    managedServer = create(m1,'Server')
    print 'creating managed server '+m1
    managedServer.setListenPort(lp1)
    managedServer.setCluster(clus2)

save()
activate(block="true")
disconnect()
print 'End of script ...'

