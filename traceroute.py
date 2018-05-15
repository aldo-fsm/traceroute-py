import socket
import sys
from random import randint
import time

def formate(listaTuplas):
    retorno = ""
    addrPrev = ""
    for tupla in listaTuplas:
        addr, elapsed_time = tupla
        if(addrPrev == ""):
            if(addr =="*"):
                retorno += "(*"  
            else:
                retorno += "(" + addr + " - " + elapsed_time
        else:
            if(addr =="*"):
                retorno += ") (*" 
            elif(addr == addrPrev):
                retorno += ", " + elapsed_time
            else:
                retorno += ") (" + addr + " - " + elapsed_time        
        addrPrev = addr
    retorno += ") "
    return retorno

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
        
        return addr, str(elapsed_time) + "ms"

    for i in range(hops):
        ttl = i+1
        data = [send_receive(ttl) for _ in range(3)]
        data = sorted(data, key=lambda x:x[0])
        printado = str(ttl) + " " + formate(data)
        print(printado)

if __name__ == '__main__':
    # print(sys.argv[1:])
    tracert('8.8.8.8', 10)