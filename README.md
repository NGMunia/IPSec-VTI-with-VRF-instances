# IPSec VTI with VRF instances



This project demonstrates a site-to-site VPN setup using **IPSec Virtual Tunnel Interfaces (VTI)** combined with **VRF Lite (Virtual Routing and Forwarding)** to segregate customer traffic. Each customer is provisioned with their own VRF instance and an IPSec VTI, ensuring isolated and secure routing domains per customer.

The enables customer sites to securely connect to a central site while maintaining traffic separation through VRF.



## Topology Description

The network topology includes:

- A central site router (Hub)
- Multiple customer site routers 
- IPSec VTI tunnels between the central site and each customer site
- VRF instances assigned per customer on both hub and spoke routers
- EIGRP routing is used as routing protocol



![Topology](/Network/Topology.PNG)



## Example Configuration Snippets


``` bash
interface Tunnel10
 vrf forwarding CUSTOMER-A
 ip address 172.16.0.1 255.255.255.252
 tunnel source Ethernet0/3
 tunnel mode ipsec ipv4
 tunnel destination 44.67.28.128
 tunnel protection ipsec profile crypt-profile
!
interface Tunnel11
 vrf forwarding CUSTOMER-B
 ip address 172.16.1.1 255.255.255.252
 tunnel source Ethernet0/3
 tunnel mode ipsec ipv4
 tunnel destination 44.67.28.129
 tunnel protection ipsec profile crypt-profile
!
interface Tunnel12
 vrf forwarding CUSTOMER-C
 ip address 172.16.2.1 255.255.255.0
 tunnel source Ethernet0/3
 tunnel mode ipsec ipv4
 tunnel destination 44.67.28.130
tunnel protection ipsec profile crypt-profile
!

          
```


## GNS3 Images used:
* Routers : [i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin](https://www.gns3.com/marketplace/appliances/cisco-iou-l3)