'This module parses the interface level debugs to identify possible issues'
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="name of the show tech file")
args = parser.parse_args()
filelocation = args.filepath
f = open(filelocation,'r')


interface_load = re.compile("\d{3}")

interfaces = []
interface_load_values=[]
interface_load_numbers=[]
interface_error=[]

for lines in f:

    lines = lines.strip('\n')

    if 'show interfaces' in lines:
        interface_config = 1

    if 'line protocol is' in lines and (interface_config == 1):
        interfaces.append(lines.split(' ')[0])
        
    if 'reliability' in lines:
        
        interface_load_values = re.findall(r"\d{1,3}/\d{1,3}", lines)

        reliability = int(interface_load_values[0].split('/')[0])
        txload = int(interface_load_values[1].split('/')[0])
        rxload = int(interface_load_values[2].split('/')[0])

        if txload > 175:

            interface_error.append('Transmission on one or more interfaces are utilizing an increased percentage of BW.'
                                   'Make sure that you have sufficient available bandwidth for the interface.')

        if rxload > 175: 
            interface_error.append('Reception on One or more interfaces are utilizing an increased percentage of bandwidth.'
                                   'Make sure that you have sufficent available bandwith for the interface.')
            
        if reliability<255:
            interface_error.append('One or more interaces have reduced reliability. '
                                   'There are chances that the interface has gone faulty. '
                                   'If the issue persist, change the hardware.')
            
    if 'CRC' in lines:

        CRC = (re.findall("\d{1,9} CRC,", lines))
        if CRC:
            if int(CRC[0].split(' ')[0])>0:
                interface_error.append('CRC Errors found on one or more interfaces.'
                      'These kind of errors occur when there is an issue with the cabling or the hardware of the NIC.')

    if 'show redundancy' in lines:
        interface_config = 0
             
print("Errors found while checking interfaces\n\n")
for errors in set(interface_error):
    print(errors)
