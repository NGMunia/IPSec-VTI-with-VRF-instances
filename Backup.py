
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from rich.prompt import Prompt
from Network.Devices import HUBS, Spokes


# RUNNING CONFIGS
rp('[bold cyan]----------Backing Up configurations---------[/bold cyan]')
filepath = Prompt.ask('[bright_magenta]Running-configs filepath [/]')
for devices in chain(HUBS.values(),Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host   = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show run')

    with open(f'{filepath}/{host}', 'w')as f:
        f.write(output)
    rp(f'The running configuration of {host} has been backed up!!')
