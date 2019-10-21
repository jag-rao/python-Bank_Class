# Python Bank project
# Author: Jagadish Rao, Oct 2019


from pathlib import Path
import fileinput

filcount = 0
filhibal = fillowbal = filsumchk = filsumsav = filnumchkacc = filnumsavacc = filnumrecs = mergedcount = 0
filcusthibal = filcustlowbal = ""

path = Path("c:\pyproj\ABC_Bank\data")
mergedfil = "c:\\pyproj\\ABC_Bank\\data\\append.txt"


def drawline():
    print()
    print("-" * 45)


def write_merged_file(infil, inrec):
    fil = open(infil, "a")
    fil.write(inrec)
    fil.close()


def getMergedCount():
    return mergedcount


class Bank:

    def __init__ (self):
        self.bankcusthibal = ""
        self.bankcustlowbal = ""
        self.banktotchkacc = 0
        self.banktotsavacc = 0
        self.banktotchkamt = 0
        self.banktotsavamt = 0
        self.bankhibal = 0
        self.banklowbal = 0


    def updateNumChkAccts(self, count):
        self.banktotchkacc += count

    def updateNumSavAccts(self, count):
        self.banktotsavacc += count

    def updateChkAmt(self, sum):
        self.banktotchkamt += sum

    def updateSavAmt(self, sum):
        self.banktotsavamt += sum

    def setCustHiBal(self, name):
        self.bankcusthibal = name

    def setCustLoBal(self, name):
        self.bankcustlowbal = name

    def setLoBal(self, amt):
        self.banklowbal = amt

    def setHiBal(self, amt):
        self.bankhibal = amt

    def getHiBal(self):
        return self.bankhibal

    def getLoBal(self):
        return self.banklowbal

    def getCustHiBal(self):
        return self.bankcusthibal

    def getCustLoBal(self):
        return self.bankcustlowbal

    def getTotChkAccts(self):
        return self.banktotchkacc

    def getTotChkAmt(self):
        return self.banktotchkamt

    def getTotSavAccts(self):
        return self.banktotsavacc

    def getTotSavAmt(self):
        return self.banktotsavamt




class BankDataFile:

    def __init__ (self, infil):
        self.infil = infil
        self.custhibal = ""
        self.custlowbal = ""
        self.lowbal = 999999999999
        self.hibal = 0
        self.sumchk = 0
        self.sumsav = 0
        self.numchkacc = 0
        self.numsavacc = 0
        self.numrecs = 0


    def displayResults(self):
        print(self.infil)
        print("Data records: " + str(self.numrecs))
        print("Max balance: " + self.custhibal + ", $" + str(self.hibal))
        print("Min balance: " + self.custlowbal + ", $" + str(self.lowbal))
        print("Num of Checking Accts: " + str(self.numchkacc))
        print("Num of Saving Accts: " + str(self.numsavacc))


    def getResults(self):
            return self.custhibal, self.hibal, self.custlowbal, self.lowbal, self.sumchk, self.sumsav, self.numchkacc, self.numsavacc, self.numrecs


    def processFileRecords(self):

        for line in fileinput.input(self.infil):
            fline = line.split(",")

            if "ID" in fline[0].upper():
                if getMergedCount() == 0:
                    write_merged_file(mergedfil, line)      # write the header into the merged file, only the first time
                continue

            bal = float(fline[-2])
            customer = fline[1] + " " + fline[2]

            if "CHECKING" in fline[-1].upper():             # track the number of checking accounts, total amount
                self.sumchk += bal
                self.numchkacc += 1
            else:
                if "SAVING" in fline[-1].upper():           # track the number of savings accounts, total amount
                    self.sumsav += bal
                    self.numsavacc += 1

            if bal > self.hibal:                             # set the highest, lowest customer
                self.hibal = bal
                self.custhibal = customer
            else:
                if bal < self.lowbal:
                    self.lowbal = bal
                    self.custlowbal = customer

            self.numrecs += 1

            write_merged_file(mergedfil, line)              # write the input record into the merged file




### Main program

NaperBank = Bank()


for fhandle in path.glob("*.csv"):          # loop over the input files

    bankfile = BankDataFile(fhandle)
    bankfile.processFileRecords()
    bankret = bankfile.getResults()

    filcusthibal, filhibal, filcustlowbal, fillowbal, filsumchk, filsumsav, filnumchkacc, filnumsavacc, filnumrecs  = bankret     # return values from each file


    NaperBank.updateNumChkAccts(filnumchkacc)
    NaperBank.updateNumSavAccts(filnumsavacc)
    NaperBank.updateChkAmt(filsumchk)
    NaperBank.updateSavAmt(filsumsav)


    if filcount == 0:
        NaperBank.setCustHiBal(filcusthibal)
        NaperBank.setHiBal(filhibal)
        NaperBank.setCustLoBal(filcustlowbal)
        NaperBank.setLoBal(fillowbal)
    else:
        if filhibal > NaperBank.getHiBal():
            NaperBank.setCustHiBal(filcusthibal)
            NaperBank.setHiBal(filhibal)
        if fillowbal < NaperBank.getLoBal():
            NaperBank.setCustLoBal(filcustlowbal)
            NaperBank.setLoBal(fillowbal)


    drawline()

    print("File: " + str(filcount + 1) + "\n")
    bankfile.displayResults()

    filcount += 1
    mergedcount += filnumrecs



drawline()
print("Summary: \n")
print("Total number of files: " + str(filcount))
print("Highest balance: " + NaperBank.getCustHiBal() + ", $" + str(NaperBank.getHiBal()))
print("Lowest balance : " + NaperBank.getCustLoBal() + ", $" + str(NaperBank.getLoBal()))
print("Checking accounts: " + str(NaperBank.getTotChkAccts()) + ", Amount: $" + str(NaperBank.getTotChkAmt()))
print("Savings accounts : " + str(NaperBank.getTotSavAccts()) + ", Amount: $" + str(NaperBank.getTotSavAmt()))
drawline()

#############################################################################################################


