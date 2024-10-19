from scapy.all import sniff, get_if_list
import logging
import random
import time

# Set up logging
logging.basicConfig(filename='packets.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def packet_callback(packet):
    # Extract relevant information from the packet
    try:
        packet_info = f"Time: {packet.time:.3f}, Source: {packet[IP].src}, " \
         f"Destination: {packet[IP].dst}, Summary: {packet.summary()}"
    except Exception as e:
        packet_info = f"Could not extract packet details: {e}"

    print(packet_info)
    logging.info(packet_info)

def start_packet_capture(interface=None):
    print("Starting packet capture... Press Ctrl+C")
