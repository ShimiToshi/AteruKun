import dpkt
import binascii


with open("sample.pcap", 'rb') as file:
    pcr = dpkt.pcap.Reader(file)
    packet_count = 0
    for ts, buf in pcr:
        # print("time sent", ts)
        # print(buf)
        packet_count += 1
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            continue
        ip = eth.data
        tcp = ip.data
        # if tcp.dport == 80 and len(tcp.data) > 0:
        #     http = dpkt.http.Request(tcp.data)
            # print(http)
        print(tcp)
        for i, b in enumerate(bytes(tcp)):
            print(i, chr(b))

        print("@@@@@")

