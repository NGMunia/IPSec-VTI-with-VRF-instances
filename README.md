# IPSec VTI with VRF instances



This project demonstrates a site-to-site VPN architecture using IPSec Virtual Tunnel Interfaces (VTI) combined with VRF-Lite (Virtual Routing and Forwarding) to provide traffic segmentation and secure connectivity for multiple customers over shared infrastructure.

Each customer is assigned:

- A dedicated VRF instance
- A dedicated IPSec VTI tunnel
- An independent routing domain


This design ensures:
- Traffic isolation between customers
- Encrypted communication between sites
- Overlapping IP address support (if required)
- Logical multi-tenancy on a single physical router



## Architectural Concept

### IPsec VTI

An IPSec VTI creates a routed tunnel interface that:
- Uses IPSec for encryption
- Behaves like a normal Layer 3 interface
- Supports dynamic routing protocols (e.g., OSPF)

Unlike crypto map–based IPSec (legacy site-to-site IPsec), VTI allows routing protocols to run directly over the tunnel, simplifying configuration and scalability.


### VRF-Lite

VRF-Lite enables multiple independent routing tables on the same router. Each VRF:

- Has its own routing table
- Maintains separate forwarding decisions
- Prevents traffic leakage between customers


VRFs are locally significant, meaning they only exist on R1. Customer routers do not need to be VRF-aware unless specifically designed to do so.



## Topology Description

The topology consists of:
- R1 – Central site router (hub)
- Multiple customer site routers (e.g., VRF-A and VRF-B)
- Dedicated IPSec VTI tunnels between R1 and each customer site
- Separate VRF instances for each customer


### Logical Structure

VRF-A → Tunnel-A → Customer A

VRF-B → Tunnel-B → Customer B

Each tunnel interface is bound to its respective VRF, ensuring complete routing separation.


![Topology](/Network/Topology.PNG)




## Routing Design

The deployment uses OSPF (Open Shortest Path First) as the routing protocol over each VTI tunnel.

### Key characteristics:

- OSPF runs independently inside each VRF.
- Routing adjacencies form over the IPSec VTI.
- Routes learned in VRF-A are not visible in VRF-B.
- Each customer maintains an isolated routing domain.


This design ensures that:
- Customer A traffic cannot reach Customer B.
- Routing tables remain fully segmented.
- Encryption and routing operate transparently together.



### Traffic Isolation Model

Traffic separation is achieved through:
- VRF-based routing table isolation
- Dedicated VTI interfaces per customer
- Independent OSPF processes within each VRF

Even though all tunnels terminate on the same physical router (R1), customer traffic remains logically separated.

## Configuration:

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


