import Pyro4
import threading
req = 0

class MyBlock:
    def __init__(self,transaction):
        self.transaction = transaction
        self.next = None

@Pyro4.expose
class MyBlockChain:
    def __init__(self,chainname):
        self.head = None
        self.chainname = chainname
        #self.lock = threading.Lock()
        # Registering and Daemon Loop
        daemon = Pyro4.Daemon()
        Pyro4.locateNS().register(chainname, daemon.register(self))
        print(str(chainname) + " Server is ready . . .")
        daemon.requestLoop()

    def createAccount(self,amount):
        # If Chain is empty, inserts to head
        if self.head is None:
            id_of_account = 1
            block = MyBlock(("CREATEACCOUNT",(id_of_account,amount)))
            self.head = block
            return id_of_account

        traverser = self.head
        maxi = 0 
        # Finds maximum account id by traversing the list 
        while traverser is not None:
            if traverser.transaction[1][0] > maxi:
                maxi = traverser.transaction[1][0]
            traverser = traverser.next
        id_of_account = maxi + 1 
        # Creates the block that will be inserted 
        block = MyBlock(("CREATEACCOUNT",(id_of_account,amount)))



        # If Chain is not empty, inserts end of the Chain
        last = self.head
        while last.next:
            last = last.next
        last.next = block
        return id_of_account

            
    def printChain(self):
        printer = self.head
        while printer is not None:
            print(printer.transaction)
            printer = printer.next

    def calculateBalance(self,accId):
        #print(self.chainname)
        traverser = self.head
        total = 0 
        if traverser is None:
            return -1
        found = 0
        while traverser is not None:
            if traverser.transaction[0] == "CREATEACCOUNT" and traverser.transaction[1][0] == accId:
                found = 1
                total += traverser.transaction[1][1]
            if traverser.transaction[0] == "TRANSFER" and traverser.transaction[1][0] == accId:
                if traverser.transaction[1][2] > 0:
                    total = total - traverser.transaction[1][2]
                else:
                    total = total + (traverser.transaction[1][2])*-1
            if traverser.transaction[0] == "TRANSFER" and traverser.transaction[1][1] == accId:
                if traverser.transaction[1][2] > 0:
                    total = total + traverser.transaction[1][2]
                else:
                    total = total - (traverser.transaction[1][2])*-1
            # Exchange will come
            if traverser.transaction[0] == "EXCHANGE" and traverser.transaction[1][0] == accId:
                if traverser.transaction[1][3] > 0:
                    total = total - traverser.transaction[1][3]
                else:
                    total = total + (traverser.transaction[1][3])*-1
            # if traverser.transaction[0] == "EXCHANGE" and traverser.transaction[1][1] == accId:
            #     if traverser.transaction[1][3] > 0:
            #         total = total + traverser.transaction[1][3]
            #     else:
            #         total = total - (traverser.transaction[1][3])*-1
            traverser = traverser.next
        if found == 0:
            return -1
        return total
                           
    def transfer(self,fromAcc,toAcc,amount):
        # if fromAcc != toAcc:
            if amount >= 0:
                fromBalance = self.calculateBalance(fromAcc)
                toBalance = self.calculateBalance(toAcc)
                if fromBalance != -1 and toBalance != -1:
                    if fromBalance >= amount:
                        block = MyBlock(("TRANSFER",(fromAcc,toAcc,amount)))
                        # If Chain is empty, inserts to head
                        if self.head is None:
                            self.head = block
                            return 1

                        # If Chain is not empty, inserts end of the Chain
                        last = self.head
                        while last.next:
                            last = last.next
                        last.next = block
                        return 1
                    else:
                        return -1
                else:
                    return -1
            else:
                amount = amount*-1
                fromBalance = self.calculateBalance(fromAcc)
                toBalance = self.calculateBalance(toAcc)
                if fromBalance != -1 and toBalance != -1:
                    if toBalance >= amount:
                        block = MyBlock(("TRANSFER",(fromAcc,toAcc,amount*-1)))
                        # If Chain is empty, inserts to head
                        if self.head is None:
                            self.head = block
                            return 1

                        # If Chain is not empty, inserts end of the Chain
                        last = self.head
                        while last.next:
                            last = last.next
                        last.next = block
                        return 1
                    else:
                        return -1
                else:
                    return -1
        # else:
            # print("Cannot transfer from your own account to yourself!")
            # return -1
    
    def exchange(self,fromAcc,toAcc,toChain,amount):
        global req
        if req == 0:
            
            fromBalance = self.calculateBalance(fromAcc)
            # print(toChain)
            # print(type(toChain))
            toBalance = toChain.calculateBalance(toAcc)

            if amount >= 0:
                if fromBalance != -1 and toBalance != -1:
                    if fromBalance >= amount:

                        req = 1
                        # self_proxy = Pyro4.Proxy(self.getChain())
                        # print("SELF:",self_proxy)
                        toChain.exchange(toAcc,fromAcc,self,amount*-1)
                        req = 0

                        block = MyBlock(("EXCHANGE",(fromAcc,toAcc,toChain.getChain(),amount)))
                        # If Chain is empty, inserts to head
                        if self.head is None:
                            self.head = block
                            return 1

                        # If Chain is not empty, inserts end of the Chain
                        last = self.head
                        while last.next:
                            last = last.next
                        last.next = block

                        

                        return 1
                    else:
                        return -1
                else:
                    
                    return -1
            else:
                amount = amount*-1
                if fromBalance != -1 and toBalance != -1:
                    if toBalance >= amount:

                        req = 1
                        # self_proxy = Pyro4.Proxy(self.getChain())
                        toChain.exchange(toAcc,fromAcc,self,amount)
                        req = 0

                        block = MyBlock(("EXCHANGE",(fromAcc,toAcc,toChain.getChain(),amount*-1)))
                        # If Chain is empty, inserts to head
                        if self.head is None:
                            self.head = block
                            return 1

                        # If Chain is not empty, inserts end of the Chain
                        last = self.head
                        while last.next:
                            last = last.next
                        last.next = block
                        
                        return 1
                    else:
                        
                        return -1
                else:
                    return -1
            

    def getChain(self):
        return self.chainname





# BTC = MyBlockChain("BTC")
# BTC.createAccount(100)
# BTC.printChain()
# BTC.createAccount(500)
# print("\n")
# BTC.printChain()
# BTC.transfer(1,2,-50)
# print("\n")
# BTC.printChain()
# print(BTC.calculateBalance(1))
# print(BTC.calculateBalance(2))
# BTC.transfer(1,2,50)
# print("\n")
# BTC.printChain()
# print(BTC.calculateBalance(1))
# print(BTC.calculateBalance(2))

# BTC.transfer(2,1,50)
# BTC.printChain()
# print(BTC.calculateBalance(1))
# print(BTC.calculateBalance(2))

# BTC.transfer(2,1,-50)
# BTC.printChain()
# print(BTC.calculateBalance(1))
# print(BTC.calculateBalance(2))