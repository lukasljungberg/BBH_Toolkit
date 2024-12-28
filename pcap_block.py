import pyshark

def extract_ip_addresses(pcap_file):
    ip_addresses = set()

    # Open the pcap file with pyshark
    cap = pyshark.FileCapture(pcap_file)

    # Iterate through each packet
    for packet in cap:
        # Check if the packet has IP layer (IPv4 or IPv6)
        if 'IP' in packet:
            # Extract source and destination IP addresses
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            ip_addresses.add(src_ip)
            ip_addresses.add(dst_ip)

    return ip_addresses

pcap_file = 'mal_packets.pcap'  # Replace with your pcap file path
ip_addresses = extract_ip_addresses(pcap_file)
for addr in ip_addresses:
    with open('/etc/pf.conf', 'a') as f:
        f.write('block drop from ' + addr + ' to any\n')
        f.write('block drop from any to ' + addr + '\n')
