

from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from rich.prompt import Prompt
from Network.Devices import Spokes, HUBS



rp('[cyan]----------Configuring MOTD banner---------[/cyan]')
for devices in chain(Spokes.values(),HUBS.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    commands = [
                'banner login @',
               f'{"*"*50}',
               f'{" "*13}{host}',
               f'{" "*5}Configured using CLI and Python',
               f'{" "}Unauthorized access is strictly forbidden',
               f'{"*"*50}',
               '@']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()


