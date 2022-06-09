import csv
import math
import datetime
def loadPackageData(fileName):
    with open(fileName) as package:
        packageData = csv.reader(package, delimiter=',')
        next(packageData)  # skip header
        for package in packageData:
            packageID = int(package[0])
            packageAddress = package[1]
            packageCity = package[2]
            packageState = package[3]
            packageZip = package[4]
            packageDeliveryDeadline = package[5]
            packageWeight = package[6]
            packageStatus = "Loaded"
            packageDeliveryTime = datetime.timedelta(hours=8)
            # create a package object from the package class
            packageInfo = Package(packageID, packageAddress, packageCity, packageState, packageZip,
                                  packageDeliveryDeadline, packageWeight, packageStatus, packageDeliveryTime)
            # insert it into the hash table
            packageHashTable.insert(packageID, packageInfo)

def addressInd(address):
    for item in addresses:
        # print(item, address)
        if address in item[1]:
            return int(item[0])
    print(address)

def truckOneLoad(listOfPackages):
    truckPackages = []
    for packageId in listOfPackages:
        truckPackages.append(packageHashTable.search(packageId))
    return truckPackages

# load function for truck 2
def truckTwoLoad(listOfPackages):
    truckPackages = []
    for packageId in listOfPackages:
        truckPackages.append(packageHashTable.search(packageId))
    return truckPackages

def truckThreeLoad(listOfPackages):
    truckPackages = []
    for packageId in listOfPackages:
        truckPackages.append(packageHashTable.search(packageId))
    return truckPackages


def distanceBetweenTruckPackages(packageID, truckAddress):

  if distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)] == "":
    return(float(distances[addressInd(truckAddress)][addressInd(packageHashTable.search(packageID).address)]))

  else:
    return float(distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)])