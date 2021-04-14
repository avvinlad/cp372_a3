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
        self.num = self.ns.NUM_NODES        
        self.distanceTable = [[999 for i in range(self.num)] for j in range(self.num)]
        self.routes = [0 for i in range(self.num)]

        # add id to route list for next hop
        self.routes[self.myID] = self.myID

        # sets values in distance table to their initial cost
        for i in range(self.num):
            self.distanceTable[ID][i] = costs[i]

        # set the diagonal values of distance table to 0
        for j in range(self.num):
           self.distanceTable[j][j] = 0
           
        # send a new packet with updated distance table
        for k in range(self.num):
            if (self.routes[k] != 999) and (k != self.myID):
                self.ns.tolayer2(RTPacket(self.myID, k, self.distanceTable[self.myID]))



    def recvUpdate(self, pkt):
        # sets the mincosts to the distance table
        self.distanceTable[pkt.sourceid] = pkt.mincosts

        for i in range(self.num):
            if (pkt.mincosts[i] < self.distanceTable[pkt.sourceid][i]):
                self.distanceTable[pkt.sourceid][i] = pkt.mincosts[i]

        # check for updated values in the distance table
        updated = False

        # bellman ford algorithm
        for row in range(self.num):
            for col in range(self.num):
                if row != col:
                    if self.bellman_ford_algo(pkt, row, col):
                        updated = True

        # make sure the diagonal values remain 0 if not that means the values have updated
        for diagonal in range(self.num):
            if self.distanceTable[diagonal][diagonal] != 0:
                self.distanceTable[diagonal][diagonal] = 0

             
        if updated:
            self.update_route()
            # sends the packet back to layer 2
            for i in range(self.num):
                if self.routes[i] != 999 and i != self.myID:
                    self.ns.tolayer2(RTPacket(self.myID, i, self.distanceTable[self.myID]))
              
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
        

    def bellman_ford_algo(self, pkt, source, destination):
        updated = False
        weight = []

        # loop through adding the weights of neighbours
        for i in range(self.num):
            weight.append(self.distanceTable[source][i] + self.distanceTable[i][destination])

        # check if minimum is less than what is in distance table and replace if true
        if (min(weight) < self.distanceTable[source][destination]):
            self.distanceTable[source][destination] = min(weight)
            self.routes[pkt.sourceid] = weight.index(min(weight))
            updated = True        
        
        return updated


    def update_route(self):        

        self.routes[self.myID] = self.myID

        return 
    