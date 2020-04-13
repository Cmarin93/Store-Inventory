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
    date_updated = DateField(default=0) # replace default w/ datetime.date object?

    class Meta: #telling the model which database it belongs to.
        database = db


def convert_price(entry):
    digit_dissection = re.compile(r"[^\d]+")
    price_reformed = digit_dissection.sub("", entry['price'])
    entry['price'] = price_reformed

def verify_product_data(entry):
    print("")
    validate_price(entry)
    validate_quantity(entry)
    validate_date(entry)
    print("")
# DESIGN QUESTION: Should I convert fields within the validation on the entry?

def validate_price(entry):
    isValidPrice = bool(re.match(r"^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$", entry['price']))
    if isValidPrice:
        convert_price(entry)
    else:
        raise TypeError()

def validate_quantity(entry):
    try:
        int(entry['quantity'])
    except TypeError:
        print("Invalid quantity")
        raise TypeError()

def validate_date(entry):
    """Validates entries date"""
    isValidDate = bool(re.match(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", entry['date_updated']))
    if isValidDate:
        #convert entry['date_updated'] to a datetime.date object.
        print(f"{entry['name']} was entered into the system on {entry['date_updated']}") 
    else:
        raise ValueError()


def compare_entry_with_records():
    pass


def import_products():
    """Creates or updates every product"""
    productEntries = fetch_products_from_csv()
    for entry in productEntries:
        try:
            verify_product_data(entry)
            #
            # attempt to get record w/ same name + date.
            # if found: rewrite, price + quantity. 
            # if not found: create new record.
            breakpoint()

            # type(entry['date_updated']) = <class 'str'>   

            # This format imports only name (all other values = 0)
            product_record = Product.get_or_create(name=entry['name']) # mapping of field names to value.
            # This format will place dulicates.
            product_record2 = Product.get_or_create(name=entry['name'], price=entry['price'], quantity=entry['quantity'], date_updated=entry['date_updated'])

        except:
            print(f"{entry['name']}: Invalid entry.")
            continue


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True) # Structure of table is set-up, but no data is inserted.
    import_products()
    db.close()

