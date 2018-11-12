#!/usr/local/bin/python3.5

import boto3
import sys
import csv
import readline

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if len(sys.argv) == 1:
        action = input("%sWhat action do you want to perform? (register/deregister): %s" % (bcolors.OKBLUE,bcolors.ENDC))
        fname = input("%sFile with InstanceIDs(Absolute path): %s"%(bcolors.OKBLUE,bcolors.ENDC))
        elbname = input("%sElbName: %s"%(bcolors.OKBLUE,bcolors.ENDC))
elif len(sys.argv) == 4:
        elbname =  sys.argv[1]
        action =  sys.argv[2]
        fname =  sys.argv[3]
else:
        print("""%sAtleast three arguments required
        Usage: ./adcheck.py <Elbname> <action> <File Name>")
        Eg:
                ./adcheck.py testelb register instids.txt %s """ % (bcolors.FAIL,bcolors.ENDC))
        exit(2)

elb = boto3.client("elb")
flist1 = []
with open(fname) as file:
        reader = csv.reader(file, delimiter='\n')
        for row in reader:
                flist1.append(row[0])

lbinst = []
for inst in flist1:
        instdic = {}
        instdic['InstanceId'] = inst
        lbinst.append(instdic)

#print(lbinst)
if action.lower() == "register" :
        print("\nRegistering....\n \n")
        response = elb.register_instances_with_load_balancer(LoadBalancerName=elbname,Instances=lbinst)
        print("%sInstanceIds in %s are \n " % (bcolors.OKBLUE, elbname))
        for instids in response['Instances']:
                print("%s " % (instids['InstanceId']))
        print("%s Total instances in %s now: %s %s %s" % (bcolors.HEADER, elbname, bcolors.BOLD, bcolors.ENDC, len(response['Instances'])))
elif action.lower() == "deregister":
        print("\nDeregistering.... \n \n")
        response = elb.deregister_instances_from_load_balancer(LoadBalancerName=elbname,Instances=lbinst)
        print("%sInstanceIds in %s are \n " % (bcolors.OKBLUE, elbname))
        for instids in response['Instances']:
                print("%s" % (instids['InstanceId']))
        print("%s Total instances in %s now: %s %s %s" % (bcolors.HEADER, elbname, bcolors.BOLD, bcolors.ENDC, len(response['Instances'])))
else:
        print("Action should only be 'register' or 'deregister'")
