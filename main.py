import csv
import math
import datetime
from operator import itemgetter, attrgetter
from classes import *

#load the addresses into a variable using the csv module
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
          
#Create new instance of package hash table from the class, and load the package into it.
packageHashTable = HashTable()
loadPackageData('package.csv')

#Function to return the index of an address to compute determine the packageID
def addressInd(address):
    for item in addresses:
        if address in item[1]:
            return int(item[0])
    print(address)


#Function to calculate the distance between a package address and the truck to determine the mileage and next location to deliver
def distanceBetweenTruckPackages(packageID, truckAddress):
  if distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)] == "":
    return(float(distances[addressInd(truckAddress)][addressInd(packageHashTable.search(packageID).address)]))
  else:
    return float(distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)])
    
#create truck objects from the truck class to carry the packages
truckOne = Truck(datetime.timedelta(hours=9), "HUB", 0.0, 0)

truckTwo = Truck(datetime.timedelta(hours=9), "HUB", 0.0, 0)

truckThree = Truck(datetime.timedelta(hours=8), "HUB", 0.0, 0)

#Determine the packages that get into the different trucks
listTruckOnePackages = [4, 40, 6, 17, 31, 32, 35, 27, 13, 39]

listTruckTwoPackages = [20, 21, 1, 28, 2, 33, 7, 29, 10, 5, 37, 38, 8, 9, 30, 3]

listTruckThreePackages = [14, 15, 16, 34, 26, 22, 24, 19, 36, 12, 23, 11, 18, 25]

#Function to load each truck with the list of packages from above
def truckLoad(listOfPackages):
    truckPackages = []
    for packageId in listOfPackages:
        truckPackages.append(packageHashTable.search(packageId))
    return truckPackages
  
# call load function to load the packages from the list of packages and sort them by delivery deadline and address
truckOne.packages = sorted(truckLoad(listTruckOnePackages), key=lambda key: (key.delivery_deadline, key.address))

truckTwo.packages = sorted(truckLoad(listTruckTwoPackages), key=lambda key: (key.delivery_deadline, key.address))

truckThree.packages = (truckLoad(listTruckThreePackages))



print("Truck One's packages")
print("")
for package in truckOne.packages:
  truckOne.mileage += distanceBetweenTruckPackages(package.ID, truckOne.address)
  truckOne.address = package.address
  package.delivery_time = truckOne.time + datetime.timedelta(hours=float(truckOne.mileage/18))
  print(package.ID, truckOne.mileage, package.delivery_deadline, package.address, package.delivery_time)
  
ui_time = datetime.timedelta(hours=9)
for package in truckOne.packages:
  if ui_time < truckOne.time:
    package.delivery_status = "Loaded"

  elif package.delivery_time > ui_time:
    package.delivery_status = "En Route"

  else:
    package.delivery_status = "Delivered"
  
  #print("Package", package.ID, "is ", package.delivery_status, "at", package.delivery_time, "with deadline", package.delivery_deadline)
print("Truck one mileage is", truckOne.mileage)
#Truck two packages
print("")
print("Truck Two's packages")
print("")
for package in truckTwo.packages:
  truckTwo.mileage += distanceBetweenTruckPackages(package.ID, truckTwo.address)
  truckTwo.address = package.address
  package.delivery_time = datetime.timedelta(hours=8) + datetime.timedelta(hours=float(truckTwo.mileage/18))
  print(package.ID, truckTwo.mileage, package.delivery_deadline, package.address,package.delivery_time)
  if ui_time < truckTwo.time:
    package.delivery_status = "Loaded"

  elif package.delivery_time > ui_time:
    package.delivery_status = "En Route"

  else:
    package.delivery_status = "Delivered"
    #print("Package", package.ID, "is ", package.delivery_status, "at", package.delivery_time, "with deadline", package.delivery_deadline)
print("Truck two mileage is", truckTwo.mileage)



print("")
print("Truck Three's packages")
print("")

for package in truckThree.packages:
  truckThree.mileage += distanceBetweenTruckPackages(package.ID, truckThree.address)
  truckThree.address = package.address
  package.delivery_time = datetime.timedelta(hours=8) + datetime.timedelta(hours=float(truckThree.mileage/18))
  print(package.ID, truckThree.mileage, package.delivery_deadline, package.address,package.delivery_time)
  if ui_time < truckThree.time:
    package.delivery_status = "Loaded"

  elif package.delivery_time > ui_time:
    package.delivery_status = "En Route"

  else:
    package.delivery_status = "Delivered"
  
  #print("Package", package.ID, "is ", package.delivery_status, "at", package.delivery_time, "with deadline", package.delivery_deadline)
  #print("Package", package.ID, "was delivered at ", package.delivery_time)
print("Truck three mileage is", truckThree.mileage)


print("Total mileage is ", truckOne.mileage + truckTwo.mileage + truckThree.mileage)
#print(package.delivery_time)

#ui_time = datetime.timedelta(hours=int(input("Hours")), minutes=int(input("mins")))








