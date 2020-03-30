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
            valid_date_entry = re.match(r"^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$", date)
            if valid_date_entry:
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
                numbers = re.compile(r"[^\d]+") # Where should this go?
                digits_only_price = numbers.sub("", price)
            else:
                raise TypeError()
        except TypeError:
            digits_only_price = 0
        # duplicate name found!
        if not product_record[1]:
            # compare dates
            # the most recent date is the winner!
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
# valid_date_entry regex by "Dany Lauener": http://regexlib.com/UserPatterns.aspx?authorId=81355952-f53d-4142-bc5c-aab2beae19f3 (not secure conection)