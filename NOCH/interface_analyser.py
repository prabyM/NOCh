import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="name of the show tech file")
args = parser.parse_args()
filelocation = args.filepath
f = open(filelocation,'r')
print ('File Opened')

interfaces = ['none']
for lines in f:
    if 'show interfaces' in lines.strip('\n'):
        print('Entering LOop')
        interface_config = 1
    if 'line protocol is' in lines and (interface_config==1):
        print (lines)
        interfaces = interfaces.append(lines.split(' ')[0])
        print ('item append')
    if 'show redundnacy' in lines:
         interface_config = 0
         

for items in interfaces:
    print items
