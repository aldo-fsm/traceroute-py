import socket
import sys
from random import randint
import time



def tracert(ip_addr, hops=30):
    port =  33435

    print('traceroute para {}, {} hops max, 3 pacotes de 60 bytes'.format(ip_addr, hops))
    # print('ttl address time')

    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    receiver.settimeout(1)
    receiver.bind(('', port))
    packet = bytes(60)

    def send_receive(ttl):
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sender.sendto(packet, (ip_addr, port))
        start_time = time.time()
        try:
            _, (addr, _) = receiver.recvfrom(1024)
        except:
            addr = '*'
        elapsed_time = round((time.time()-start_time)*1000, 3)
        
        return addr, elapsed_time

    for i in range(hops):
        ttl = i+1
        data = [send_receive(ttl) for _ in range(3)]
        data = sorted(data, key=lambda x:x[0])
        print(data)
        # print('{} -> {} \t| {}ms'.format(ttl, str.join(' ',data[0]), 'a'))
        # addr1, elapsed_time1 = send_receive(ttl)
        # addr2, elapsed_time2 = send_receive(ttl)
        # addr3, elapsed_time3 = send_receive(ttl)
        # print('{} -> {} \t| {}ms'.format(ttl, addr1, elapsed_time1))

if __name__ == '__main__':
    # print(sys.argv[1:])
    tracert('8.8.8.8', 10)