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
#             Hypo:  2. When looping thru entries - the rest of entires data overides the records data.

class Product(Model):  
    id = AutoField(unique=True)
    name = CharField(max_length=75)
    price = IntegerField(default=0)
    quantity = IntegerField(default=0)
    date_updated = DateField(default=0)

    class Meta: #telling the model which database it belongs to.
        database = db


def add_products():
    """Creates or updates every product"""
    product_enteries = fetch_products_from_csv()
    for entry in product_enteries:
        product_record = Product.get_or_create(name=entry.get('name'))

# verifying product_price
        try:
            print('')
            valid_price_entry = re.match(r"^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$", entry['price'])
            if valid_price_entry:
                digit_regex = re.compile(r"[^\d]+")
                price = digit_regex.sub("", entry['price'])
            else:
                raise TypeError()
        except TypeError:
            price = 0
        product_record[0].price = price
# verifying product_quantity
        try:
            quantity = int(entry['quantity'])
        except TypeError:
            quantity = 0
        product_record[0].quantity = quantity
 # verifying date_update
        try:
            finalDate = product_record[0].date_updated
            isValidDate = bool(re.match(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", entry['date_updated'])) 
            if isValidDate:
                isNewProduct = product_record[1]
                if isNewProduct:
                    finalDate = datetime.strptime(entry['date_updated'], '%m/%d/%Y').date()
                    print(f"{entry['name']} has been added to the database!")
                else:
                    record_date = product_record[0].date_updated
                    entry_date = datetime.strptime(entry['date_updated'], '%m/%d/%Y').date()
                    finalDate = greater_then_date(record_date, entry_date)
                    print(f"{entry['name']} has been updated!")
            else:
                raise TypeError()
        except TypeError as e:
            date_object = 0
        product_record[0].date_updated = finalDate
        product_record[0].save()
    print('')


def verify_date(record, entry):
    pass


def greater_then_date(record, entry):
    if record > entry:
        greater_date = record
    else:
        greater_date = entry
    return greater_date


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    add_products()
    db.close()





# 'valid_price_entry' regex by "Brian Orrell": http://regexlib.com/UserPatterns.aspx?authorId=f77b664d-b24a-4461-8e5f-8ea36aa47f58 (not secure connection)

# notes about 'valid price entry':
# '$0.00' = '000'


