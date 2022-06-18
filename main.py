# Hi! My name is Brandon Mukum, student ID is 010080169.
import csv
import math
import datetime
from operator import itemgetter, attrgetter
from classes import *


# load the attached addresses from the addresses.csv into a variable using the csv module
addresses = list(csv.reader(open('addresses.csv', encoding='utf-8-sig')))

# load the distances from the distance_data.csv file into a distances variable using the csv module
distances = list(csv.reader(open("distance_data.csv", encoding='utf-8-sig')))


# Function to load all the data from the package.csv file into the package hash table object
##https://srm--c.na127.visual.force.com/apex/coursearticle?Id=kA03x000001DbBGCA0
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


# Create new instance of package hash table from the class, and load the package into it.
packageHashTable = HashTable()
loadPackageData('package.csv')


# Function to return the index of an address to compute determine the packageID
def addressInd(address):
    for item in addresses:
        if address in item[1]:
            return int(item[0])
    print(address)


# Function to calculate the distance between a package address and the truck to determine the mileage and next location to deliver
# https://srm--c.na127.visual.force.com/apex/coursearticle?Id=kA03x000001DbBGCA0
def distanceBetweenTruckPackages(packageID, truckAddress):
  if distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)] == "":
    return(float(distances[addressInd(truckAddress)][addressInd(packageHashTable.search(packageID).address)]))
  else:
    return float(distances[addressInd(packageHashTable.search(packageID).address)][addressInd(truckAddress)])


# create truck objects from the truck class to carry the packages
truckOne = Truck(datetime.timedelta(hours=9, minutes=6), "HUB", 0.0, 0)

truckTwo = Truck(datetime.timedelta(hours=8, minutes=6), "HUB", 0.0, 0)

truckThree = Truck(datetime.timedelta(hours=10), "HUB", 0.0, 0)

# Determine list of presorted package IDs
list_pkgs = [4, 40, 6, 17, 31, 32, 35, 27, 13, 39,20, 15, 21, 1, 2, 33, 7, 29, 10, 5, 37, 38, 8, 9, 30, 3, 14, 34, 16, 26, 22, 24, 19, 36, 12, 23, 11, 18, 25,28]

# Write the function to load the trucks
# https://srm--c.na127.visual.force.com/apex/coursearticle?Id=kA03x000001DbBGCA0
def truckLoad(listOfPackages):
    truckPackages = [] #empty list to hold package IDs from loop
    for packageId in listOfPackages:
        truckPackages.append(packageHashTable.search(packageId))
    return truckPackages


# call load function to load the packages from the list of packages and sort them by delivery deadline and address or leave in default pre-sorted order.
truckOne.packages = truckLoad(list_pkgs[:10])
truckTwo.packages = truckLoad(list_pkgs[10:26])
truckThree.packages = sorted(truckLoad(list_pkgs[26:]), key=lambda key: ( key.delivery_deadline, key.address))

#Function that serves the user interface with package delivery status
# https://srm--c.na127.visual.force.com/apex/coursearticle?Id=kA03x000001DbBGCA0
def getPackageStatus(time):
    print("Package status and info:")
    for package in truckOne.packages:
        truckOne.mileage += distanceBetweenTruckPackages(package.ID, truckOne.address)
        truckOne.address = package.address
        package.delivery_time = truckOne.time + datetime.timedelta(hours=float(truckOne.mileage / 18))
        if ui_time < truckOne.time:
            package.delivery_status = "In the Hub"

        elif package.delivery_time > ui_time:
            package.delivery_status = "En Route"

        else:
            package.delivery_status = "Delivered"
        #print("")
        print("PackageID =", package.ID, ", Address:", package.address, ", City:", package.city, ", State:",package.state, ", Zip:", package.zip, ", Delivery deadline:", package.delivery_deadline, ", Weight(kilo):", package.weight, ", Delivery Status:", package.delivery_status, ", Delivery time:",package.delivery_time)

    for package in truckTwo.packages:
        truckTwo.mileage += distanceBetweenTruckPackages(package.ID, truckTwo.address)
        truckTwo.address = package.address
        package.delivery_time = truckTwo.time + datetime.timedelta(hours=float(truckTwo.mileage / 18))
        if ui_time < truckTwo.time:
            package.delivery_status = "In the Hub"

        elif package.delivery_time > ui_time:
            package.delivery_status = "En Route"

        else:
            package.delivery_status = "Delivered"
        print("PackageID =", package.ID, ", Address:", package.address, ", City:", package.city, ", State:",package.state, ", Zip:", package.zip, ", Delivery deadline:", package.delivery_deadline, ", Weight(kilo):", package.weight, ", Delivery Status:", package.delivery_status, ", Delivery time:",package.delivery_time)

    for package in truckThree.packages:
        truckThree.mileage += distanceBetweenTruckPackages(package.ID, truckThree.address)
        truckThree.address = package.address
        package.delivery_time = truckThree.time + datetime.timedelta(hours=float(truckThree.mileage / 18))
        if ui_time < truckThree.time:
            package.delivery_status = "In the Hub"

        elif package.delivery_time > ui_time:
            package.delivery_status = "En Route"

        else:
            package.delivery_status = "Delivered"

        print("PackageID =", package.ID, ", Address:", package.address, ", City:", package.city, ", State:",package.state, ", Zip:", package.zip, ", Delivery deadline:", package.delivery_deadline, ", Weight(kilo):", package.weight, ", Delivery Status:", package.delivery_status, ", Delivery time:",package.delivery_time)

    print("Total mileage for all trucks is ", truckOne.mileage + truckTwo.mileage + truckThree.mileage)

print("Check the status and information for all packages:")
ui_time = datetime.timedelta(hours=int(input("Please enter the hour in 24-hour format: ")), minutes=int(input("Please enter the minute: ")))
getPackageStatus(ui_time)








