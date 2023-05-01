import hashlib
import datetime

class Header:
    def __init__(self, miner, blockNumber,timestamp):
        self.miner = miner
        self.blockNumber = blockNumber
        self.timestamp = timestamp

    def __str__(self):
        return f'Miner: {self.miner}\nBlock Number: {self.blockNumber}\nTimestamp: {self.timestamp}'
    
    def getMiner(self):
        return self.miner
    
    def getBlockNumber(self):
        return self.blockNumber
    
    def getTimestamp(self):
        return self.timestamp
    
    def __eq__(self, other):
        return self.miner == other.miner and self.blockNumber == other.blockNumber and self.timestamp == other.timestamp
    
    
    

class Data:
    def __init__(self):
        self.data = list()

    def __str__(self):
        return f'Transactions: {self.data}'
    
    def addTransaction(self, transaction):
        if(len(self.data)==10):
            print("Block is full")
        else:
            self.data.append(transaction)

    def getTransaction(self, index):
        return self.data[index]
    
    def getTransactions(self):
        return self.data
    
    def __eq__(self, other):
        return self.data == other.data
    

    


class Footer:
    def __init__(self,hashPrevBlock, hashCurrentBlock):
        self.hashPrevBlock = hashPrevBlock
        self.hashCurrentBlock = hashCurrentBlock

    def __str__(self):
        return f'Previous Block Hash: {self.hashPrevBlock}\nCurrent Block Hash: {self.hashCurrentBlock}'
    
    def getHashPrevBlock(self):
        return self.hashPrevBlock
    
    def getHashCurrentBlock(self):
        return self.hashCurrentBlock
    
    def __eq__(self, other):
        return self.hashPrevBlock == other.hashPrevBlock and self.hashCurrentBlock == other.hashCurrentBlock

    

class Block:
    def __init__(self, header, data, footer):
        self.header = header
        self.data = data
        self.footer = footer
    
    def __str__(self):
        return f"Header: {self.header}\n Data: {self.data}\n Footer: {self.footer}"
    
    def getHeader(self):
        return self.header
    
    def getData(self):
        return self.data
    
    def getFooter(self):
        return self.footer
    
    def calculate_hash(self):
        return hashlib.sha256(str(self.data).encode() + str(self.footer.getHashPrevBlock()).encode()).hexdigest()
    def __eq__(self, other):
        return self.header == other.header and self.data == other.data and self.footer == other.footer

    