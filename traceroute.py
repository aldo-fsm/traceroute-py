import socket
import sys
from random import randint
import time



def tracert(ip_addr, hops=30):
    port =  33435

    print('traceroute para {}, {} hops max, pacotes de 60 bytes'.format(ip_addr, hops))
    # print('ttl address time')

    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    receiver.bind(('', port))
    packet = bytes(60)
    for i in range(hops):
        ttl = i+1
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sender.sendto(packet, (ip_addr, port))
        start_time = time.time()
        _, addr = receiver.recvfrom(1024)
        elapsed_time = round((time.time()-start_time)*1000, 3)
        print('{} -> {} \t| {}ms'.format(ttl, addr[0], elapsed_time))

if __name__ == '__main__':
    # print(sys.argv[1:])
    tracert('8.8.8.8', 10)