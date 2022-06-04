import csv
import math
import datetime
from operator import itemgetter, attrgetter
from classes import *

#load the address into an addresses variable using the csv module
addresses = list(csv.reader(open('addresses.csv', encoding='utf-8-sig')))

#load the distance into a distances variable using the csv module
distances = list(csv.reader(open("distance_data.csv", encoding='utf-8-sig')))
# function to return distance between package 1's address and the hub and vice versa
#print(distances[addressInd(packageHashTable.search(1).address)][addressInd(truckOne.address)])

# function to load all the data from the package.csv file into the package hash table object
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

#create function to return the index of each address.
def addressInd(address):
    for item in addresses:
        # print(item, address)
        if address in item[1]:
            return int(item[0])

#Create new instance of package hash table from the class, and load objects into it
packageHashTable = HashTable()
loadPackageData('package.csv')

#create truck 1 and 2 objects from the truck class
truckOne = Truck(datetime.timedelta(hours=8), "HUB", 0.0, 0)
truckTwo = Truck(datetime.timedelta(hours=8), "HUB", 0.0, 0)

# packages that must be delivered on truck 2 plus 12 other packages
listTruckTwoPackages = [3,18,36,38] + list(range(10,17)) + list(range(19,24))
truckTwo.packages = [packageHashTable.search(i) for i in listTruckTwoPackages]

# packages that must be delivered on truck 2 plus 12 other packages
listTruckTwoPackages = [3,18,36,38] + list(range(10,17)) + list(range(19,24))
truckTwo.packages = [packageHashTable.search(i) for i in listTruckTwoPackages]
#print(truckTwo.packages)

ignore = listTruckTwoPackages + [6, 25, 28, 29]  #don't include delayed packages or those loaded into truck two
listTruckOnePackages = [i for i in range(1,35) if i not in ignore]  # list of 16 packages satisfying the above

#define functions to load each truck
#load function for truck one:
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
  
# call load function to load the packages from listTruckOnePackages and sort them by delivery deadline
truckOne.packages = sorted(truckOneLoad(listTruckOnePackages), key=attrgetter('delivery_deadline'))

truckTwo.packages = sorted(truckTwoLoad(listTruckTwoPackages), key=attrgetter('delivery_deadline'))




