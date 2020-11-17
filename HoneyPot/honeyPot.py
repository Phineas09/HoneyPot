import pyshark
import mysql.connector
from simpleMySql import SimpleMysql


class CustomPacket:

    packetStack = None
    packetCount = 0

    def __init__(self):
        self.packetCount = 0
        self.packetStack = []

    def processPackets(self, packet):
        self.packetCount = self.packetCount + 1
        
        if(packet.layers[-1].layer_name == "http"):
            print(f"Http packet from {packet.layers[1].get_field('host')}\t to  {packet.layers[1].get_field('dst')}")
            self.packetStack.append(packet)
            #print(packet.layers[1].field_names)
            #print(packet.layers[-1].field_names)
            #I want only the attacker packets
            if(packet.layers[1].get_field('dst') == "192.168.1.191"): #ip address of the site
                print(packet.layers[-1].get_field('request_uri'))
                print(packet.layers[-1].get_field('request_full_uri'))
                print(packet.layers[-1].get_field('request_method'))
                print("Delim---------------------------------------")

            



capture = pyshark.LiveCapture(interface='ens33', bpf_filter='tcp')
customPacket = CustomPacket()

capture.apply_on_packets(customPacket.processPackets)

'''
db = SimpleMysql(
    host="192.168.1.235",
    port=3306,
    user="honeyMonitor",
    passwd="Claudiu147!$&",
    db="honeyData",
	keep_alive=True # try and reconnect timedout mysql connections?
)

book = db.getAll("test", ["name"])

db.update("test",
	{"a": 250},
	("id=%s AND b=%s", (12, 4))
)

db.commit()
print(book)
book = db.getAll("test", ["name"])
print(book)

'''