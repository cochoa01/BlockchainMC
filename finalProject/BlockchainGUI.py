from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Blockchain import *
from Node import *
import random
import pickle

class BlockchainGUI():

    def __init__(self):
        self.refreshBlockchain()
        self.window = Tk()
        self.window.title("Blockchain")
        self.window.geometry("600x300")
        
        self.TopFrame = Frame(self.window)
        self.TopFrame.pack(fill=X, anchor='n')

        self.MiddleFrame = Frame(self.window)
        self.MiddleFrame.pack(fill=X)

        self.BottomFrame = Frame(self.window)
        self.BottomFrame.pack(fill=X)

        self.ButtonFrame = Frame(self.window)
        self.ButtonFrame.pack(fill=X, anchor='s')

        self.radio_var = IntVar()
        self.radio_var.set(0)
        self.rb1 = Radiobutton(self.TopFrame, text="View Blockchain", variable=self.radio_var, value=1, command= self.blockchainView)
        self.rb2 = Radiobutton(self.TopFrame, text="View Block", variable=self.radio_var, value=2, command=self.blockView)
        self.rb3 = Radiobutton(self.TopFrame, text="View Nodes", variable=self.radio_var, value=3, command=self.nodeView)
        self.rb4 = Radiobutton(self.TopFrame, text="Quit", variable=self.radio_var, value=4, command=self.window.destroy)

        self.rb1.pack(side=LEFT)
        self.rb2.pack(side=LEFT)
        self.rb3.pack(side=LEFT)
        self.rb4.pack(side=LEFT)

        self.refresh = Button(self.ButtonFrame, text="Refresh", command=self.refresh)
        self.refresh.pack()


        mainloop()

    

    def blockchainView(self):
        self.refreshBlockchain()
        self.clearMiddle()
        self.label = Label(self.MiddleFrame, text="Blockchain Info:")
        self.label.pack(side=LEFT)

        self.clearBottom()
        self.blockNum = IntVar()
        self.blockNum.set(self.blockChain.getSize())
        self.label = Label(self.BottomFrame, text="Total Blocks Mined: ")
        self.label.pack(side=LEFT)
        self.label = Label(self.BottomFrame, textvariable=self.blockNum)
        self.label.pack(side=LEFT)

    def refreshBlockchain(self):
        with open(r'D:\VS Code\Class\Blockchain\finalProject\blockState.pickle', 'rb') as f:
            self.blockState = pickle.load(f)

        with open(r'D:\VS Code\Class\Blockchain\finalProject\blockChain.pickle', 'rb') as f:
            self.blockChain = pickle.load(f)

    def refresh(self):
        self.refreshBlockchain()
        if self.radio_var.get() == 1:
            self.blockchainView()
        elif self.radio_var.get() == 2:
            self.blockView()
        elif self.radio_var.get() == 3:
            self.nodeView()

    def blockView(self):
        self.refreshBlockchain()
        self.clearMiddle()
        self.label = Label(self.MiddleFrame, text="Block Info:")
        self.label.pack(side=LEFT)

        self.clearBottom()
        s = StringVar()
        self.entry = Entry(self.BottomFrame, textvariable=s)
        self.entry.pack(side=LEFT)
        self.button = Button(self.BottomFrame, text="Submit", command=lambda: self.blockViewHelper(s.get()))
        self.button.pack(side=LEFT)

    async def Delegate(self):
        await self.blockState.Delegation()

    def blockViewHelper(self, blockNum):
        try:
            blockNum = int(blockNum)
            if blockNum < 0:
                raise ValueError
            elif blockNum >= self.blockChain.getSize():
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid Block Number")
        

        self.clearBottom()
        s = StringVar()
        self.entry = Entry(self.BottomFrame, textvariable=s)
        self.entry.pack(side=LEFT)
        self.button = Button(self.BottomFrame, text="Submit", command=lambda: self.blockViewHelper(s.get()))
        self.button.pack(side=LEFT)

        self.label = Label(self.BottomFrame, text="Block Number: ")
        self.label.pack()
        self.label = Label(self.BottomFrame, text=blockNum)
        self.label.pack()


        self.label = Label(self.BottomFrame, text="Mined By: ")
        self.label.pack()
        self.label = Label(self.BottomFrame, text=self.blockChain.getBlock(blockNum).getHeader().getMiner())
        self.label.pack()


        self.label = Label(self.BottomFrame, text="Mined At: ")
        self.label.pack()
        self.label = Label(self.BottomFrame, text=self.blockChain.getBlock(blockNum).getHeader().getTimestamp())
        self.label.pack()


        self.label = Label(self.BottomFrame, text="Block Hash: ")
        self.label.pack()
        self.label = Label(self.BottomFrame, text=self.blockChain.getBlock(blockNum).getFooter().getHashCurrentBlock())
        self.label.pack()


    def nodeView(self):
        self.refreshBlockchain()
        self.clearMiddle()
        self.label = Label(self.MiddleFrame, text="Node Info:")
        self.label.pack(side=LEFT)

        self.clearBottom()
        self.nodeNum = StringVar()
        self.label = Label(self.BottomFrame, text="Node Number: ")
        self.label.pack(side=LEFT)
        self.entry = Entry(self.BottomFrame, textvariable=self.nodeNum)
        self.entry.pack(side=LEFT)
        self.button = Button(self.BottomFrame, text="Submit", command=lambda: self.nodeViewHelper(self.nodeNum.get()))
        self.button.pack(side=LEFT)

    def nodeViewHelper(self, nodeNum):
        try:
            nodeNum = int(nodeNum)
            if nodeNum < 0:
                raise ValueError
            elif nodeNum > len(self.blockState.nodes):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid Node Number")

        self.clearBottom()
        self.nodeNum = StringVar()
        self.label = Label(self.BottomFrame, text="Node Number: ")
        self.label.pack(side=LEFT)
        self.entry = Entry(self.BottomFrame, textvariable=self.nodeNum)
        self.entry.pack(side=LEFT)
        self.button = Button(self.BottomFrame, text="Submit", command=lambda: self.nodeViewHelper(self.nodeNum.get()))
        self.button.pack(side=LEFT)

        self.label = Label(self.BottomFrame, text="Reputation Balance: ")
        self.label.pack()
        self.label = Label(self.BottomFrame, text=self.blockState.nodes[nodeNum].getReputation())
        self.label.pack()

        self.label = Label(self.BottomFrame, text="Is Mining: ")
        self.label.pack()
        if(self.blockState.nodes[nodeNum].isMining):
            self.label = Label(self.BottomFrame, text="True")
        else:
            self.label = Label(self.BottomFrame, text="False")
        self.label.pack()



    def clearMiddle(self):
        self.MiddleFrame.destroy()
        self.MiddleFrame = Frame(self.window)
        self.MiddleFrame.pack(fill=X)

    def clearBottom(self):
        self.BottomFrame.destroy()
        self.BottomFrame = Frame(self.window)
        self.BottomFrame.pack(fill=X)

    

if __name__ == "__main__":
    x = BlockchainGUI()