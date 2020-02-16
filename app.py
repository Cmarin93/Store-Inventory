import csv

with open('inventory.csv', 'r', newline='') as csvfile:
     inventory = csv.reader(csvfile)
     next(inventory)
     for line in inventory:
         print(line[0])
