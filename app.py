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
            valid_price_entry = re.match(r"^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$", entry['price'])
            if valid_price_entry:
                digit_regex = re.compile(r"[^\d]+") # refector?
                price = digit_regex.sub("", entry['price'])
            else:
                raise TypeError()
        except TypeError:
            price = 0

# verifying product_quantity
        try:
            quantity = int(entry['quantity'])
        except TypeError:
            quantity = 0

 # verifying date_update
        try:
            valid_date = bool(re.match(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", entry['date_updated']))
            if valid_date:
                new_record = product_record[1]
                if new_record:
                    print(f"{entry['name']} has been added to the database!")
                else: 
                    breakpoint()
                    # I need to reinstate this condition
                    if entry["date_updated"] < date: # questionable condition
                        # type(entry["date_updated"]) = <class 'str'>
                        # type(product_record[0].date_updated) = <class 'int'>
                        date = product_record[0].date_updated
                        date_object = datetime.strptime(date, '%m/%d/%Y')
                        input(f"{product_record[0].date_updated} < {date}")
                    else: 
                        date = product_record[0].date_updated
                        date_object = datetime.strptime(date, '%m/%d/%Y')
                date_object = datetime.strptime(date, '%m/%d/%Y')
            else:
                raise TypeError()
        except TypeError:
            breakpoint()
            date_object = 0

# saving data
        product_record[0].quantity = quantity
        product_record[0].price = price
        #breakpoint()
        product_record[0].date_updated = date_object
        product_record[0].save()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    add_products()
    db.close()





# 'valid_price_entry' regex by "Brian Orrell": http://regexlib.com/UserPatterns.aspx?authorId=f77b664d-b24a-4461-8e5f-8ea36aa47f58 (not secure connection)