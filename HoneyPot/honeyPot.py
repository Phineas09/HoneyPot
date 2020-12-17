import pyshark
import mysql.connector
import sys
import re
import json
import argparse
from simpleMySql import SimpleMysql
from urllib.request import urlopen
from IPy import IP

class PacketDigest:

    packetStack = None
    packetCount = 0
    database = None
    filteredPackets = 0

    def __init__(self):
        self.packetCount = 0
        self.packetStack = []
        self.filteredPackets = 0
        self.database = SimpleMysql(
                host=MACRO.DB_HOST,
                port=3306,
                user=MACRO.DB_USERNAME,
                passwd=MACRO.DB_PASSWORD,
                db=MACRO.DB_NAME,
                keep_alive=True # try and reconnect timedout mysql connections?
            )


    def findIpLocation(self, ipAddr):
        if(ipAddr == ''):
            return 'Unknown/Local'

        ip = IP(ipAddr)

        if(ip.iptype() == "PUBLIC"):
            url = 'https://ipinfo.io/' + ipAddr + '/json'
        
        if(ip.iptype() == "PRIVATE"):
            url = 'https://ipinfo.io/json'

        res = urlopen(url)
        data = json.load(res)
        city = data['city']
        country=data['country']
        return city + "/" + country


    def registerPacketToDatabase(self, packet):
        database = self.database
        if(database != None):
            #gather all info from packet
            database.insert("packets", {
                "Source_Ip": str(packet.layers[1].get_field('host')),
                "Dest_Ip": str(packet.layers[1].get_field('dst')),
                "Source_MAC": str(packet.layers[0].get_field("src_resolved")), #eth layer
                "Method" : str(packet.layers[-1].get_field('request_method')), #http layer
                "Port" : str(packet.layers[2].get_field('dstport')),
                "Path" : str(packet.layers[-1].get_field('request_uri')), #http layer
                "Origin" : str(self.findIpLocation(str(packet.layers[1].get_field('host')))) 
            })

            #commit to database
            database.commit()
            print("Packet saved!")
        else:
            print("Packet was not saved!")

    def processPackets(self, packet):
        
        self.packetCount = self.packetCount + 1

        if(packet.layers[-1].layer_name == "http" or packet.layers[-1].layer_name == "data-text-lines"): #catch automated requests
            if(packet.layers[-1].layer_name == "data-text-lines"):
                packet.layers.pop()
            print(f"Http packet from {packet.layers[1].get_field('host')}\t to  {packet.layers[1].get_field('dst')}")
            if(packet.layers[1].get_field('host') not in MACRO.IGNORE_IP ): #ip address of the site
                self.registerPacketToDatabase(packet)
                self.packetStack.append(packet)
                self.filteredPackets = self.filteredPackets + 1


    def printStats(self):
        print(f"Intercepted Packets {self.packetCount}\nPackets of interest {self.filteredPackets}")


def startCapture(customPacket):
    capture = pyshark.LiveCapture(interface='ens33', bpf_filter='tcp')
    capture.apply_on_packets(customPacket.processPackets)

if __name__ == '__main__':

    CONSTANTS_PATH = "./config.json"

    with open(CONSTANTS_PATH) as f:
        data = json.load(f)

    MACRO = argparse.Namespace(**data)
    customPacket = PacketDigest()
    try:
        startCapture(customPacket)
    except KeyboardInterrupt:
        print('\nInterrupted\n')
        customPacket.printStats()
        sys.exit(0)
