# IPSec VTI with VRF instances



This project demonstrates a site-to-site VPN setup using **IPSec Virtual Tunnel Interfaces (VTI)** combined with **VRF Lite (Virtual Routing and Forwarding)** to segregate customer traffic. Each customer is provisioned with their own VRF instance and an IPSec VTI, ensuring isolated and secure routing domains per customer.

The enables customer sites to securely connect to a central site while maintaining traffic separation through VRF.



## Topology Description

The network topology includes:

- A central site router R1
- Multiple customer site routers (VRF-A and VRF-B)
- IPSec VTI tunnels between the central site and each VRFs
- VRF instances assigned per VRF on both R1 and spooke routers
- OSPF routing is used as routing protocol

VRF-A traffic is separate from VRF-B traffic.


![Topology](/Network/Topology.PNG)



## IPsec VTI 

The topology uses IPsec VTI as a tunnel configuration method; in conjuction with IPsec.
The following are steps to configure IPsec VTI with VRF:

### Define the VRFs:

```bash
!
ip vrf VRF-A
!
ip vrf VRF-B
!
ip vrf VRF-C
!
```

### Define the Cryptography algorithms:

```bash
crypto isakmp policy 100
 encr aes 256
 hash sha256
 authentication pre-share
 group 14
 lifetime 7200
crypto isakmp key strongkey! address 0.0.0.0
!
!
crypto ipsec transform-set crypt-ts esp-aes 256 esp-sha256-hmac
 mode tunnel
!
crypto ipsec profile crypt-profile
 set transform-set crypt-ts
 set pfs group14
!
```
### Configure Tunnels:

```bash
!
interface Tunnel0
 ip vrf forwarding VRF-A
 description CONNECTING TO VRF-A
 ip address 172.16.0.1 255.255.255.252
 ip ospf network point-to-point
 ip ospf 1 area 0
 tunnel source Ethernet0/0
 tunnel mode ipsec ipv4
 tunnel destination 32.19.86.10
 tunnel key 10
 tunnel protection ipsec profile crypt-profile
!
interface Tunnel1
 description CONNECTING TO VRF-B
 ip vrf forwarding VRF-B
 ip address 172.17.0.1 255.255.255.252
 ip ospf network point-to-point
 ip ospf 2 area 0
 tunnel source Ethernet0/0
 tunnel mode ipsec ipv4
 tunnel destination 32.19.86.20
 tunnel key 20
 tunnel protection ipsec profile crypt-profile
!
interface Tunnel10
 description CONNECTING TO VRF-A
 ip vrf forwarding VRF-A
 ip address 172.16.0.5 255.255.255.252
 ip ospf network point-to-point
 ip ospf 1 area 0
 tunnel source Ethernet0/1
 tunnel mode ipsec ipv4
 tunnel destination 44.67.28.10
 tunnel key 10
 tunnel protection ipsec profile crypt-profile
!
interface Tunnel11
 description CONNECTING TO VRF-B
 ip vrf forwarding VRF-B
 ip address 172.17.0.5 255.255.255.252
 ip ospf network point-to-point
 ip ospf 2 area 0
 tunnel source Ethernet0/1
 tunnel mode ipsec ipv4
 tunnel destination 44.67.28.20
 tunnel key 20
 tunnel protection ipsec profile crypt-profile
```



## GNS3 Images used:
* Routers : [i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin](https://www.gns3.com/marketplace/appliances/cisco-iou-l3)