import csv
import math
import datetime
from operator import itemgetter, attrgetter
from classes import *

#load the address into an addresses variable using the csv module
addresses = list(csv.reader(open('addresses.csv', encoding='utf-8-sig')))

#load the distance into a distances variable using the csv module
distances = list(csv.reader(open("distance_data.csv", encoding='utf-8-sig')))

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
    print(address)

#Create new instance of package hash table from the class, and load objects into it
packageHashTable = HashTable()
loadPackageData('package.csv')

#create truck 1 and 2 objects from the truck class
truckOne = Truck(datetime.timedelta(hours=8), "HUB", 0.0, 0)
truckTwo = Truck(datetime.timedelta(hours=8), "HUB", 0.0, 0)
truckThree = Truck(datetime.timedelta(hours=9 minutes=10), "HUB", 0.0, 0)

# Packages that must be delivered on truck 2 plus 12 other packages.
#listTruckTwoPackages = [3,18,15,36,38] + list(range(11,14)) + list(range(19,24))
listTruckTwoPackages = [3,18,15,36,38] + list(range(11,24))
truckTwo.packages = [packageHashTable.search(i) for i in listTruckTwoPackages]

ignore = listTruckTwoPackages + [5,17,24,27,32,35]
listTruckOnePackages = [i for i in range(1,33) if i not in ignore]  # list of 16 packages satisfying the above
ignore_2 = listTruckTwoPackages + listTruckOnePackages

listTruckThreePackages = [i for i in range(1,41) if i not in ignore_2]

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
  
# call load function to load the packages from listTruckOnePackages and sort them by delivery deadline
truckOne.packages = sorted(truckOneLoad(listTruckOnePackages), key=attrgetter('zip'))

truckTwo.packages = sorted(truckTwoLoad(listTruckTwoPackages), key=attrgetter('zip'))

truckThree.packages = sorted(truckThreeLoad(listTruckThreePackages), key=attrgetter('zip'))

def distanceBetweenTruckPackages(packageID, truckAddress):

  if distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)] == "":
    return(float(distances[addressInd(truckAddress)][addressInd(packageHashTable.search(packageID).address)]))

  else:
    return float(distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)])


print("Truck One's packages")
print("")
for package in truckOne.packages:
  truckOne.mileage += distanceBetweenTruckPackages(package.ID, truckOne.address)
  truckOne.address = package.address
  package.delivery_time = truckOne.time + datetime.timedelta(hours=float(truckOne.mileage/18))
  print(package.ID, truckOne.mileage)
  
ui_time = datetime.timedelta(hours=9)
for package in truckOne.packages:
  if ui_time < truckOne.time:
    package.delivery_status = "Loaded"

  elif package.delivery_time > ui_time:
    package.delivery_status = "En Route"

  else:
    package.delivery_status = "Delivered"
  
  print("Package", package.ID, "is ", package.delivery_status, "at", package.delivery_time, "with deadline", package.delivery_deadline)
print("Truck one mileage is", truckOne.mileage)
#Truck two packages
print("")
print("Truck Two's packages")
print("")
for package in truckTwo.packages:
  truckTwo.mileage += distanceBetweenTruckPackages(package.ID, truckOne.address)
  truckTwo.address = package.address
  package.delivery_time = datetime.timedelta(hours=8) + datetime.timedelta(hours=float(truckTwo.mileage/18))
  print(package.ID, truckTwo.mileage)
  if ui_time < truckTwo.time:
    package.delivery_status = "Loaded"

  elif package.delivery_time > ui_time:
    package.delivery_status = "En Route"

  else:
    package.delivery_status = "Delivered"
    print("Package", package.ID, "is ", package.delivery_status, "at", package.delivery_time, "with deadline", package.delivery_deadline)
print("Truck two mileage is", truckTwo.mileage)



print("")
print("Truck Three's packages")
print("")

for package in truckThree.packages:
  truckThree.mileage += distanceBetweenTruckPackages(package.ID, truckOne.address)
  truckThree.address = package.address
  package.delivery_time = datetime.timedelta(hours=8) + datetime.timedelta(hours=float(truckThree.mileage/18))
  print(package.ID, truckThree.mileage)
  if ui_time < truckThree.time:
    package.delivery_status = "Loaded"

  elif package.delivery_time > ui_time:
    package.delivery_status = "En Route"

  else:
    package.delivery_status = "Delivered"
  
  print("Package", package.ID, "is ", package.delivery_status, "at", package.delivery_time, "with deadline", package.delivery_deadline)
  #print("Package", package.ID, "was delivered at ", package.delivery_time)
print("Truck three mileage is", truckThree.mileage)


print("Total mileage is ", truckOne.mileage + truckTwo.mileage + truckThree.mileage)
#print(package.delivery_time)

#ui_time = datetime.timedelta(hours=int(input("Hours")), minutes=int(input("mins")))








