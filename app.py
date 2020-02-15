import csv

with open('inventory.csv', newline='') as csvfile:
     inventory = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in inventory:
         print(', '.join(row))