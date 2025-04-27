class BusBooking:
    def __init__(self) -> None:
        self.EmptyAisle = [-1]*20
        self.EmptyWindow = [-1]*20
        self.IntialBooking = 1
        self.WaitingList = []
        self.FinalList = []
        self.IDname =[]
        return
    def bookingID(self):
        p = self.IntialBooking
        self.IntialBooking += 1
        return p
    def addaisle(self,name):
        m = self.bookingID()
        i = self.EmptyAisle.index(-1)
        self.EmptyAisle = self.EmptyAisle[:i]+[m]+self.EmptyAisle[i+1:]
        self.FinalList.append((m,"".join(map(str,["A",i+1]))))
        self.IDname.append((m,name))
        return (m,"".join(map(str,["A",i+1])))
    def addwindow(self,name):
        m = self.bookingID()
        i = self.EmptyWindow.index(-1)
        self.EmptyWindow = self.EmptyWindow[:i]+[m]+self.EmptyWindow[i+1:]
        self.FinalList.append((m,"".join(map(str,["W",i+1]))))
        self.IDname.append((m,name))
        return (m,"".join(map(str,["W",i+1])))
    def addwaiting(self,name,preference):
        m = self.bookingID()
        self.WaitingList.append([m,"".join(map(str,["WL-",1+len(self.WaitingList)]))])
        self.FinalList.append((self.WaitingList[-1][0],self.WaitingList[-1][1]))
        self.IDname.append((m,name))
        return (self.WaitingList[-1][0],self.WaitingList[-1][1])
    def book(self,name,preference="W"):
        if preference is None:
            preference = "No preference"
        if preference.lower() in ["a","aisle"]:
            if -1 in self.EmptyAisle:
                return self.addaisle(name)
            elif -1 in self.EmptyWindow:
                return self.addwindow(name)
            else:
                return self.addwaiting(name,preference)
        elif preference.lower() in ["w","window"]:
            if -1 in self.EmptyWindow:
                return self.addwindow(name)
            elif -1 in self.EmptyAisle:
                return self.addaisle(name)
            else:
                return self.addwaiting(name,preference)
        else:
            if -1 in self.EmptyAisle:
                return self.addaisle(name)
            elif -1 in self.EmptyWindow:
                return self.addwindow(name)
            else:
                return self.addwaiting(name,preference)    
    def cancel(self,booking_id):
        for i in range(len(self.FinalList)):
            if booking_id in self.FinalList[i]:
                if i<40:
                    c = self.FinalList[i][1]
                    if len(self.WaitingList)>0:
                        v = self.WaitingList[0][0]
                        self.WaitingList = self.WaitingList[1:]
                        for g in range(len(self.WaitingList)):
                            t = list(self.WaitingList[g])
                            t = [t[0],"".join(map(str,["WL-",g+1]))]
                            self.WaitingList = self.WaitingList[:g]+[tuple(t)]+self.WaitingList[g+1:]
                        self.FinalList = self.FinalList[:i]+[(v,c)]+self.FinalList[i+1:40]+self.WaitingList
                        return True
                    else:
                        self.FinalList = self.FinalList[:i]+self.FinalList[i+1:]
                    return True
                else:
                    self.WaitingList = self.WaitingList[:i-40]+self.WaitingList[i-39:]
                    for g in range(len(self.WaitingList)):
                        t = list(self.WaitingList[g])
                        t = [t[0],"".join(map(str,["WL-",g+1]))]
                        self.WaitingList = self.WaitingList[:g]+[tuple(t)]+self.WaitingList[g+1:]
                    self.FinalList = self.FinalList[:i]+self.WaitingList[i-40:]
                    return True
        return False
    def status(self,booking_id):
        for i in self.FinalList:
            if booking_id in i:
                return (self.IDname[booking_id-1][1],i[1])
    def __str__(self) -> str:
        BId_N_CS = []
        for i in self.FinalList:
            name = ""
            for j in self.IDname:
                if j[0] == i[0]:
                    name = j[1]
                    break
            BId_N_CS.append([i[0],name,i[1]])
        BId_N_CS.sort()
        return " ".join(map(str, BId_N_CS))