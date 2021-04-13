"""
-------------------------------------------------------
[Node.py]
-------------------------------------------------------
Author:  Arshnoor Singh Bhinder, Avin Lad
ID:      183169310, 180647870
Email:   Bhin9310@mylaurier.ca, ladx7870@mylaurier.ca
__updated__ = "2021-04-13"
-------------------------------------------------------
"""

from common import *


class Node:

    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES        
        self.distanceTable = [[999 for i in range(num)] for j in range(num)]
        self.routes = [0 for i in range(num)]

        # you implement the rest of constructor
        # sets values in distance table to their initial cost
        for i in range(num):
            self.distanceTable[ID][i] = costs[i]

        # set the diagonal values of distance table to 0
        for i in range(num):
           self.distanceTable[i][i] = 0

        # sets the values for the routes to the initial distance values
        for i in range(len(self.distanceTable[self.myID])):
            self.routes[i] = self.distanceTable[self.myID][i]


    def recvUpdate(self, pkt):
        self.distanceTable[pkt.sourceid] = pkt.mincosts
        # you implement the rest of it 
        

        # sends the packet back to layer 2
        self.ns.tolayer2(pkt)

              
        return 
    
    def printdt(self):
        print("   D" + str(self.myID) + " |  ", end="")
        for i in range(self.ns.NUM_NODES):
            print("{:3d}   ".format(i), end="")
        print()
        print("  ----|-", end="")
        for i in range(self.ns.NUM_NODES): 
            print("------", end="")
        print()    
        for i in range(self.ns.NUM_NODES):
            print("     {}|  ".format(i), end="")
            
            for j in range(self.ns.NUM_NODES):
                print("{:3d}   ".format(self.distanceTable[i][j]), end="")
            print()            
        print()
        
