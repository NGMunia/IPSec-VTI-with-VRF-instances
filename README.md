# IPv4-VPN-over-IPv6



The following employs IPv4-VPN mGRE overlay with IPv6 as the underlay (Transport network).

This can be implemented in scenarios where ISPs are transitioning and rolling out IPv6 in their infrastructure.

The IPv6 network serves as the underlay network while IPv4 serves as the overlay network.

The VPN configuration allows communications between spokes within a region and the central network while restricting inter-regional communication.

This is achieved through route filtering.


![Topology](/Network/Topology.png)





## GNS3 Images used:
* Routers : [i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin](https://www.gns3.com/marketplace/appliances/cisco-iou-l3)
* Switches: i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
* Server: [Windows_Server_2016_Datacenter_EVAL_en-us_14393_refresh](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2016)
* IDS: [Ostinato Wireshark](https://gns3.com/marketplace/appliances/ostinato-wireshark)
* Admin-PC: Windows 8.1 ISO VM
* End-user PCs: [Webterm Docker](https://gns3.com/marketplace/appliances/webterm)
