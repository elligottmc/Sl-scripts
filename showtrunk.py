# Show Trunk Ports
import SoftLayer
import os, random, string
import string
from itertools import chain
import json
import SoftLayer.API
from pprint import pprint as pp

## Input ID and API Key Below

username = ""
apiKey =""

## Input Fully Qualified Hostname Below

fullyQualifiedDomainName = ""

##Call the API and start doing stuff

client = SoftLayer.Client(
    username= username,
    api_key = apiKey,
    )


###############################################################
# GET SERVER DETAILS                                          #
###############################################################



# Lookup Hostname

hardwarelist = client['Account'].getHardware()

#print [hardwarelist];

for hardware in hardwarelist:
    if hardware['fullyQualifiedDomainName'] == fullyQualifiedDomainName:
        hardwareid=hardware['id']
        continue    

#hardwareid = '399220'

mask_object="backendRouters,networkVlans,uplinkNetworkComponents"
hardware = client['Hardware'].getObject(mask=mask_object, id = hardwareid)
backendRouter = hardware['backendRouters'][0]['fullyQualifiedDomainName']

# Get Trunked VLAN details

try:
    # FIND uplink network Index Number
    index=0
    for uplink in hardware['uplinkNetworkComponents']:
        if uplink['name'] == "eth" and 'primaryIpAddress' in uplink.keys():
                uplinkid=uplink['id']
                continue

    # Get Network Component ID for Uplink
    network = client['Network_Component'].getObject(mask='uplinkComponent', id=uplinkid)
    networkcomponentid=network['id']
    uplinkcomponentid=network['uplinkComponent']['id']

    # Get VLAN Trunks for network_compondent ID
    trunks = client['Network_Component'].getNetworkVlanTrunks(mask='networkVlan', id=uplinkcomponentid)
    
    trunkindex=0
    
    if trunks:
       print ("Trunks/Tags Found");
    else:
       print ("No Trunks/Tags Found");
   
    for trunk in trunks:
        trunkindex=trunkindex+1
        print ("VLAN Trunk #%s: %s (%s)" % (trunkindex, trunk['networkVlan'],trunk['networkVlan']['vlanNumber'])           );
        
           

    
except SoftLayer.SoftLayerAPIError as e:
    print("Error: %s, %s" % (e.faultCode, e.faultString))
