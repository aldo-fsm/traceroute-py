#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import time

def formate(listaTuplas):
    retorno = ""
    addrPrev = ""
    for tupla in listaTuplas:
        addr, hostname, elapsed_time = tupla
        if hostname:
            addr = '{} ({})'.format(hostname, addr)
        if(addrPrev == ""):
            if(addr =="*"):
                retorno += "[*"  
            else:
                retorno += "[" + addr + " - " + elapsed_time
        else:
            if(addr =="*"):
                retorno += "] [*" 
            elif(addr == addrPrev):
                retorno += ", " + elapsed_time
            else:
                retorno += "] [" + addr + " - " + elapsed_time        
        addrPrev = addr
    retorno += "] "
    return retorno

def tracert(hostname, hops=30):
    ip_addr = socket.gethostbyname(hostname)
    hops = int(hops)
    port =  33435

    if hops > 255:
        print("max hops não pode ser maior que 255")
        return

    print('traceroute para {}, {} hops max, 3 pacotes de 60 bytes'
        .format(ip_addr if ip_addr == hostname else '{} ({})'.format(hostname, ip_addr) , hops))

    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    receiver.settimeout(1)
    receiver.bind(('', port))
    packet = bytes(60)

    def send_receive(ttl):
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sender.sendto(packet, (ip_addr, port))
        start_time = time.time()
        hostname = ''
        try:
            _, (addr, _) = receiver.recvfrom(1024)
            try:
                hostname = socket.gethostbyaddr(addr)[0]
            except:
                pass
        except:
            addr = '*'
        elapsed_time = round((time.time()-start_time)*1000, 3)
        
        return addr, hostname, str(elapsed_time) + "ms"

    for i in range(hops):
        ttl = i+1
        data = [send_receive(ttl) for _ in range(3)]
        data = sorted(data, key=lambda x:x[0])
        print('{} -> {}'.format(ttl, formate(data)))

        if ip_addr in list(zip(*data))[0]:
            break

if __name__ == '__main__':
    args = sys.argv[1:]
    ip_addr = args[0]
    args = args[1:]
    tracert(ip_addr,*args)