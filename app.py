#!/usr/bin/env python3
import datetime
import csv
from peewee import *


db = SqliteDatabase('stock.db')

with open('inventory.csv', 'r', newline='') as csvfile:
     inventory = csv.reader(csvfile)
     next(inventory) # skips first line.
     for item in inventory:
         print(item[0])


class Product(Model):
    id = AutoField(unique=True)
    name = CharField(max_length=255, unique=True)
    price = IntegerField()
    quantity = IntegerField()
    last_checked = DateTimeField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)



    # another day for progress 2/7/2020 - carlosa a marin
