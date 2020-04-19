8#!/usr/bin/env python3
from datetime import datetime
from dateutil.parser import parse
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
#        What if there are 2 identital product entries entered within the same date? (add the later entry)

class Product(Model):  
    id = AutoField(unique=True)
    name = CharField(max_length=75, unique=True)
    price = IntegerField(default=0) 
    quantity = IntegerField(default=0)
    date_updated = DateField(default=0) # replace default w/ datetime.date object?

    class Meta: #telling the model which database it belongs to.
        database = db


def verify_product_data(entry):
    print("")
    validate_date(entry)
    validate_price(entry)
    validate_quantity(entry)
    print("")


def validate_date(entry):
    """Validates entries date"""
    isValidDate = bool(re.match(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", entry['date_updated']))
    if isValidDate:
        datetime_object = parse(entry['date_updated'])
        date_object = datetime_object.date()   
        entry['date_updated'] = date_object
    else:
        print("Invalid date.")
        raise ValueError()

# Price

def convert_price(entry):
    digit_dissection = re.compile(r"[^\d]+") 
    price_reformed = digit_dissection.sub("", entry['price']) 
    entry['price'] = price_reformed

def validate_price(entry):
    isValidPrice = bool(re.match(r"^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$", entry['price']))
    if isValidPrice:
        convert_price(entry)
    else:
        print("Invalid Price.")
        raise TypeError()


# Quantity

def validate_quantity(entry):
    try:
        int(entry['quantity'])
    except TypeError:
        print("Invalid quantity")
        raise TypeError()

def compare_entry_with_records():
    pass


def import_products():
    """Creates or updates every product"""
    entries = fetch_products_from_csv()
    for entry in entries:
        try:
            verify_product_data(entry) # entries data is verified in : correct_format
            #breakpoint()
        except:
            print(f"{entry['name']}: Invalid entry.")
            continue


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True) # Structure of table is set-up, but no data is inserted.
    import_products()
    db.close()