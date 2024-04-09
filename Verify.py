


from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from Network.Devices import Spokes, HUBS





# VERIFYING EIGRP ROUTES:
rp('\n[bold cyan]----------Verifying EIGRP ROUTES ON HUB AND SPOKE ROUTERS---------[/bold cyan]')
for devices in chain(Spokes.values(), HUBS.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip route eigrp')
    rp(host,output, sep='\n')


print('\n\n')


# VERIFYING EIGRP NEIGHBORSHIP :
rp('\n[bold cyan]----------Verifying EIGRP NEIGHBORSHIP ON HUB AND SPOKE ROUTERS---------[/bold cyan]')
for devices in chain(Spokes.values(), HUBS.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip eigrp neighbors')
    rp(host,output, sep='\n')



print('\n\n')


# VERIFYING DMVPN registration:
rp('\n[bold cyan]----------Verifying DMVPN REGISTRATION AND CRYPTOGRAPHY ON ROUTERS---------[/bold cyan]')
for devices in chain(Spokes.values(), HUBS.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show dmvpn detail')
    rp(host,output, sep='\n')

