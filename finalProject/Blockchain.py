import hashlib
import datetime
from Block import *
from Node import Node
import sched, time
import pickle

class Blockchain:
    def __init__(self, nodeID):
        self.chain = [self.create_genesis_block(nodeID)]

    def create_genesis_block(self, nodeID):
        header = Header(nodeID, 0,datetime.datetime.now())
        data = Data()
        footer = Footer(0, hashlib.sha256(str(data).encode() + str(0).encode()).hexdigest())
        return Block(header, data, footer)

    def add_block(self, new_block):
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.footer.getHashCurrentBlock() != current_block.calculate_hash():
                return False
            if current_block.footer.getHashPrevBlock() != previous_block.calculate_hash():
                return False
            
        return True
    
    def getSize(self):
        return len(self.chain)
    
    def getBlock(self, index):
        if index >= self.getSize():
            return None
        return self.chain[index]
    
    def __eq__(self, other):
        return self.chain == other.chain

class DelegatedProofOfStake:
    def __init__(self):
        print('Initializing Delegated Proof of Stake...')
        self.nodes = []
        self.currentMiners = []
        
    def add_node(self, node):
        print(f'Adding node {node.getNodeID()}...')
        self.nodes.append(node)

    async def Delegation(self):
        print('\nStarting new delegation...')

        miners = sorted(self.nodes, key = lambda x: x.getNodeID())
        #init votes
        votes = {}
        for i in range(0, len(self.nodes)):
            votes[i] = 0

        #getting votes
        for node in self.nodes:
            votes[node.getVote()] += node.getReputation()

        #sorting votes
        votes = sorted(votes.items(), key = lambda x: x[1], reverse = True)

        #selecting proposer
        self.currentMiners = []
        self.currentRep = []
        for vote in votes[:5]:
            l, r = vote
            self.currentMiners+=[l]
            self.currentRep+=[r]

        print(f'Current miners: {", ".join([str(x) for x in self.currentMiners])}') 
        print(f'Votes gathered: {", ".join([str(x) for x in self.currentRep])}') 


        self.currentMiners = [miners[i] for i in self.currentMiners]

        print('Starting mining...')
        #starting the  mining process
        self.StartMining()

        print('Applying consensus...')
        #consensus
        self.Consensus()

        print('Saving state...')
        #saving state
        self.saveState()

        #scheduling the next delegation
        time.sleep(10)
        await self.Delegation()


    def Consensus(self):
        
        #getting the longest chain
        longestChain = self.currentMiners[0].getBlockChain()
        for miner in self.currentMiners:
            if (miner.getBlockChain().getSize() > longestChain.getSize() ) and miner.getBlockChain().is_valid():
                longestChain = miner.getBlockChain()

            if (miner.getBlockChain().is_valid() == False):
                miner.setReputationBalance(miner.getReputation() - 5)
                print(f'!!! Node {miner.getNodeID()} has been penalized for having an invalid blockchain !!!')

        print(f'Updating longest chain...')
        #updating the chain
        self.updateChain(longestChain)

    def updateChain(self, longestChain):
        for miner in self.currentMiners:
            miner.setBlockChain(longestChain)

        with open(r'D:\VS Code\Class\Blockchain\finalProject\blockChain.pickle', 'wb') as f:
            pickle.dump(longestChain, f)


    def getCurrentMiners(self):
        return self.currentMiners
    
    def StartMining(self):
        s1 = sched.scheduler(time.time, time.sleep)
        delay = 0

        for miner in self.currentMiners:
            s1.enter(delay:=delay+10,1,miner.Mine)

        s1.run()
        
    def saveState(self):
        with open(r'D:\VS Code\Class\Blockchain\finalProject\blockState.pickle', 'wb') as f:
            pickle.dump(self, f)


class BlockchainWithDPoS:
    def __init__(self):
        self.blockchain = Blockchain()
        self.dpos = DelegatedProofOfStake()

    def add_node(self, node):
        self.dpos.add_node(node)

    def create_block(self, data):
        block_data = {'data': data, 'proposer': self.dpos.current_proposer}
        new_block = Block(datetime.datetime.now(), block_data, '')
        self.dpos.select_proposer()
        if self.dpos.verify_proposer(new_block):
            self.blockchain.add_block(new_block)

    def is_valid(self):
        return self.blockchain.is_valid()

