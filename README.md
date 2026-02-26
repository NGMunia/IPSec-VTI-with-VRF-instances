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

## Verifying Routing:

To verify OSPF routes on VRF-A

```bash
R1#sh ip route vrf VRF-A

! Output omitted for brevity

Gateway of last resort is not set

      172.16.0.0/16 is variably subnetted, 4 subnets, 2 masks
C        172.16.0.0/30 is directly connected, Tunnel0
L        172.16.0.1/32 is directly connected, Tunnel0
C        172.16.0.4/30 is directly connected, Tunnel10
L        172.16.0.5/32 is directly connected, Tunnel10
      192.168.10.0/32 is subnetted, 1 subnets
O        192.168.10.1 [110/65536] via 172.16.0.2, 02:19:36, Tunnel0
      192.168.110.0/32 is subnetted, 1 subnets
O        192.168.110.1 [110/65536] via 172.16.0.6, 02:19:59, Tunnel10

```

Verying OSPF routes on VRF-B

```bash
R1#sh ip route vrf VRF-A ospf

Routing Table: VRF-A
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      192.168.10.0/32 is subnetted, 1 subnets
O        192.168.10.1 [110/65536] via 172.16.0.2, 02:27:46, Tunnel0
      192.168.110.0/32 is subnetted, 1 subnets
O        192.168.110.1 [110/65536] via 172.16.0.6, 02:28:09, Tunnel10

```


## Verifying Cryptography:

### Verifying IKE phase 1: 
```bash
R1#sh crypto isakmp sa Vrf VRF-A
IPv4 Crypto ISAKMP SA
dst             src             state          conn-id status
44.67.28.1      44.67.28.10     QM_IDLE           1011 ACTIVE
32.19.86.1      32.19.86.10     QM_IDLE           1010 ACTIVE

IPv6 Crypto ISAKMP SA

R1#sh crypto isakmp sa Vrf VRF-B
IPv4 Crypto ISAKMP SA
dst             src             state          conn-id status
44.67.28.20     44.67.28.1      QM_IDLE           1009 ACTIVE
44.67.28.1      44.67.28.20     QM_IDLE           1008 ACTIVE
32.19.86.1      32.19.86.20     QM_IDLE           1007 ACTIVE

```

### Verifying IKE phase 2:
```bash
R1#sh crypto ipsec sa vrf VRF-A

interface: Tunnel0
    Crypto map tag: Tunnel0-head-0, local addr 32.19.86.1

   protected vrf: VRF-A
   local  ident (addr/mask/prot/port): (0.0.0.0/0.0.0.0/0/0)
   remote ident (addr/mask/prot/port): (0.0.0.0/0.0.0.0/0/0)
   current_peer 32.19.86.10 port 500
     PERMIT, flags={origin_is_acl,}
    #pkts encaps: 960, #pkts encrypt: 960, #pkts digest: 960
    #pkts decaps: 940, #pkts decrypt: 940, #pkts verify: 940
    #pkts compressed: 0, #pkts decompressed: 0
    #pkts not compressed: 0, #pkts compr. failed: 0
    #pkts not decompressed: 0, #pkts decompress failed: 0
    #send errors 0, #recv errors 0

     local crypto endpt.: 32.19.86.1, remote crypto endpt.: 32.19.86.10
     plaintext mtu 1438, path mtu 1500, ip mtu 1500, ip mtu idb Ethernet0/0
     current outbound spi: 0x735EA5CD(1935582669)
     PFS (Y/N): Y, DH group: group14

```