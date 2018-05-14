import socket
import sys



if __name__ == '__main__':
    # print(sys.argv[1:])
    port = 33435
    hops = 10
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    receiver.bind(('', port))
    for i in range(hops):
        ttl = i+1
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sender.sendto(b'', ('8.8.8.8', port))
        _, addr = receiver.recvfrom(1024)
        print(ttl, addr[0])
