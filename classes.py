# Hash table function with initial capacity and functions defined
class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=40):  # there are 40 packages provided
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Adding new items to the hash table.
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)  # find bucket and bucket array to insert the item
        bucket_l = self.table[bucket]

        # set the key if it's already in the bucket
        for key_value in bucket_l:
            if key_value[0] == key:
                key_value[1] = item
                return True

        # append the item to the bucket array if it's not present
        key_value = [key, item]
        bucket_l.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    def search(self, key):
        bucket = hash(key) % len(self.table)  # locating the bucket
        bucket_l = self.table[bucket]
        # search for the key in the bucket list
        for key_value in bucket_l:
            if key_value[0] == key:
                return key_value[1]
        return None

# create package object for packages
class Package:
    def __init__(self, ID, address, city, state, zip, delivery_deadline, weight, status, delivery_time):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time

    def __str__(self):  # overwite print(Movie) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
        self.ID, self.address, self.city, self.state, self.zip, self.delivery_deadline, self.weight, self.status, self.delivery_time)

class Truck:
    def __init__(self, time, address, mileage, packages):
        self.time = time
        self.address = address
        self.mileage = mileage
        self.packages = packages
    def __str__(self):  # overwite print otherwise it will print object reference
        return "%s, %s, %s, %s" % (self.time, self.address, self.mileage, self.packages)