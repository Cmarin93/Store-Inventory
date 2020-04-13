#!/usr/bin/env python3
from datetime import datetime
import csv
import re
from peewee import *


db = SqliteDatabase('inventory.db')


def fetch_products_from_csv():
    """ returns 'products' : a list of ordered dictionaries"""
    with open('inventory.csv', newline='') as csvfile:
        products = list(csv.DictReader(csvfile)) 
    return products



# ERROR WITH LOGIC:  1. The date needs to determine what data shall be saved into the DB.
#
#        What if there are 2 entries entered within the same date?

class Product(Model):  
    id = AutoField(unique=True)
    name = CharField(max_length=75)
    price = IntegerField(default=0)
    quantity = IntegerField(default=0)
    date_updated = DateField(default=0)

    class Meta: #telling the model which database it belongs to.
        database = db

# CURRENTLY: researching how to skip an iteration of an entry that has been rejected.
def verify_product_data(entry):
    validate_date(entry)
    validate_price(entry)
    validate_quantity(entry)


def validate_date(entry):
    try:
        isValidDate = bool(re.match(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", entry['date_updated']))
        if isValidDate:
            print(f"{entry['name']} | {entry['date_updated']}") # NAME | DATE
        else:
            raise ValueError()
    except ValueError:
        input(f"{entry['name']}: Invalid date.")
        breakpoint()

def validate_price(entry):
    try:
        isValidPrice = bool(re.match(r"^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$", entry['price']))
        if isValidPrice:
            print(f"Price: {entry['price']}")
        else:
            raise TypeError()
    except TypeError:
        input(f"{entry['name']}: Invalid price")
        #continue

def validate_quantity(entry):
    try:
        int(entry['quantity'])
        print(f"Qty: {entry['quantity']}")
        input("")
    except TypeError:
        print(f"{entry['name']}: Invalid quantity.")
        input("")
        #continue


# WRITE: CONVERT_DATA or Implement data into validation.




def add_products():
    """Creates or updates every product"""
    product_enteries = fetch_products_from_csv()
    for entry in product_enteries:
        verify_product_data(entry)
        # I do not understand this function completely.
        product_record = Product.get_or_create(name=entry['name'], date_updated=entry['date_updated']) # mapping of field names to value.


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True) # Structure of table is set-up, but no data is inserted.
    add_products()
    db.close()



                    # PRICE CONVERTION
            # digit_dissection = re.compile(r"[^\d]+")
            # price_reformed = digit_dissection.sub("", entry['price'])
            # entry['price'] = price_reformed




