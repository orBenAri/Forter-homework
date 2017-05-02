
import csv
from fuzzywuzzy import fuzz
import unittest

def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    count = 1
    accuracy = 89
    realBillFirstName = billFirstName.split(" ")[0]                                # get rids of middle names
    realShipFirstName = shipFirstName.split(" ")[0]                                # get rids of middle names
    x= billNameOnCard.split(" ")
    firstNameOnCard = x[0].lower()                                                 # splits name on card
    lastNameOnCard = x[1].lower()

    if not checkNames(realBillFirstName, billLastName.lower(), realShipFirstName, shipLastName.lower(), accuracy):
        count += 1
    if not checkNames(realBillFirstName, billLastName.lower(), firstNameOnCard, lastNameOnCard, accuracy) \
            and not checkNames(realShipFirstName, shipLastName.lower(), firstNameOnCard, lastNameOnCard, accuracy):
        count += 1
    return count

def checkNames(name1FirstName, name1LastName, name2FirstName, name2LastName, accuracy):
    csvFile = open("nicknames.csv")
    name1Options = [name1FirstName]
    name2Options = [name2FirstName]
    dictNickNames = csv.DictReader(csvFile)
    for row in dictNickNames:                                                     # finds all possible names for a nickname
        if fuzz.token_sort_ratio(row["nickname"], name1FirstName) >= accuracy:
            name1Options.append(row["name"])
        if fuzz.token_sort_ratio(row["nickname"], name2FirstName) >= accuracy:
            name2Options.append(row["name"])
    csvFile.close()
    for name1 in name1Options:                                                    # checks all options
        for name2 in name2Options:
         nameA = name1 + " " + name1LastName
         nameB = name2 + " " + name2LastName
         if fuzz.token_sort_ratio(nameA, nameB) >= accuracy:
            return True
    return False


class testing(unittest.TestCase):

    def testOne(self):
        self.failUnless(1==countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli"))

    def testTwo(self):
        self.failUnless(1==countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli"))

    def testThree(self):
        self.failUnless(1==countUniqueNames("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli"))

    def testFour(self):
        self.failUnless(1==countUniqueNames("Deborah", "Egli", "Deborah S", "Egli", "Egli Deborah"))

    def testFive(self):
        self.failUnless(2==countUniqueNames("Michele","Egli","Deborah","Egli","Michele Egli"))


if __name__ == "__main__":
    unittest.main()

