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
    product_id = AutoField(unique=True)
    product_name = CharField(max_length=75)
    product_price = IntegerField(default=0)
    product_quantity = IntegerField(default=0)
    date_updated = DateField(default=0)

    class Meta: #telling the model which database it belongs to.
        database = db


def add_products():
    """Creates or updates every product"""
    products = fetch_products_from_csv()
    for product in products:
        product_record = Product.get_or_create(product_name=product.get('product_name'))
        # verifying date_update
        try:
            date = product.get('date_updated')
            valid_date_entry = bool(re.match(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", date))
            print(f"{product['product_name']} | {date}")
            print(f'is this a valid entry? {valid_date_entry}')
            if valid_date_entry:
                object_created = product_record[1]
                print(f'object crated? = {product_record[1]}')
                print('')
                if object_created: 
                    pass # object is new
                else:
                    pass # object already exsist
                #     if date < product_record[0].date_updated: 
                #         date = product_record[0].date_updated
                date_object = datetime.strptime(date, '%m/%d/%Y')
            else:
                raise TypeError()
        except TypeError:
            date_object = 0
        # verifying product_quantity
        try:
            quantity = int(product.get('product_quantity'))
        except TypeError:
            quantity = 0
        # verifying product_price
        try:
            price = product.get('product_price')
            valid_price_entry = re.match(r"^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$", price)
            if valid_price_entry:
                numbers = re.compile(r"[^\d]+") ## sets "numbers" every time we loop thru a product. where would be better placement?
                digits_only_price = numbers.sub("", price)
            else:
                raise TypeError()
        except TypeError:
            digits_only_price = 0
        ## duplicate name found!
        if not product_record[1]: ## is there a better way to write this condition?
            # compare dates
            # the most recent date is the Record that shall be saved!
            pass
        # finalizing changes
        product_record[0].product_quantity = quantity
        product_record[0].product_price = digits_only_price
        product_record[0].date_updated = date_object
        product_record[0].save()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    add_products()
    db.close()





# valid_price_entry regex by "Brian Orrell": http://regexlib.com/UserPatterns.aspx?authorId=f77b664d-b24a-4461-8e5f-8ea36aa47f58 (not secure connection)