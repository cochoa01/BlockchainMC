import random
import sched,time
from Block import *

class Node:
    def __init__(self, nodeID, reputationBalance, blockChain):

        self.nodeID = nodeID
        self.reputationBalance = reputationBalance
        self.blockChain = blockChain
        self.isMining = False

    def getNodeID(self):
        return self.nodeID
    
    def getReputation(self):
        return self.reputationBalance
    
    def getBlockChain(self):
        return self.blockChain
    
    def setReputationBalance(self, reputationBalance):
        self.reputationBalance = reputationBalance

    def getVote(self):
        vote = random.randint(0,99)
        while(vote<=self.reputationBalance):
            if(random.randint(0,1)==1):
                return vote
            vote = random.randint(0,99)

        return vote
        

    def setBlockChain(self, blockChain):
        self.blockChain = blockChain

    
    def Mine(self):
        print(f'Node {self.nodeID} is mining...')
        self.isMining = True
        currTime = time.time()
        speed = random.randint(1,3)
        devious = False
        if (random.randint(0,100)<=15):
            devious = True
        
        totalItems = speed*60
        
        print(f'Node {self.nodeID} accessing mempool...')
        mempool = self.getMempool()

        DataBlocks = []
        for i in range(0, int(totalItems/10)):
            dataBlock = Data()
            for j in range(0, 10):
                selection = random.randint(0, len(mempool)-1)
                
                dataBlock.addTransaction(self.makeTransaction(mempool[selection]))
                                         
                del(mempool[selection])

            DataBlocks.append(dataBlock)

        self.setMempool(mempool)

        for dataBlock in DataBlocks:

            header = Header(self.nodeID, self.blockChain.getSize(), datetime.datetime.now())
            dataHash = str(dataBlock)+str(self.blockChain.getBlock(-1).getFooter().getHashCurrentBlock())
            if devious:
                dataHash = str(dataBlock)
            footer = Footer(self.blockChain.getBlock(self.blockChain.getSize()-1).getFooter().getHashCurrentBlock(),self.calculate_hash(dataHash))
            newBlock = Block(header, dataBlock, footer)
            self.blockChain.add_block(newBlock)
        
        while (time.time() - currTime < 10):
            continue
        
        oldRep = self.getReputation()
        self.setReputationBalance(self.getReputation() + speed*2)
        self.isMining = False
        print(f'Node {self.nodeID} finished mining {int(totalItems/10)} blocks... Reputation Balance: {oldRep} --> {self.getReputation()}')

    def makeTransaction(self, transaction):
        return hash(transaction)
    
    def calculate_hash(self, data):
        return hashlib.sha256(data.encode()).hexdigest()
    
    def getMempool(self): 
        with open(r'D:\VS Code\Class\Blockchain\finalProject\mempool.txt', 'r') as file:
            data = file.readlines()
            data = [line.strip() for line in data]

        return data
    
    def setMempool(self, mempool):
        with open(r'D:\VS Code\Class\Blockchain\finalProject\mempool.txt', 'w') as file:
            for transaction in mempool:
                file.write(transaction+'\n')


            
            

            

            


    
    def __str__(self):
        return f'Node ID: {self.nodeID}\nReputation Balance: {self.reputationBalance}\nBlock Chain: {self.blockChain}'

    