from Blockchain import *
from Node import *
import asyncio
import random

async def main():
    blockchainSystem = DelegatedProofOfStake()
    
    #create nodes
    nodes = []
    for i in range(0, 100):
        nodes.append(Node(i,random.randint(0,100), Blockchain(i)))
        blockchainSystem.add_node(nodes[i])

    #start delegations
    await blockchainSystem.Delegation()

if __name__ == "__main__":
    asyncio.run(main())