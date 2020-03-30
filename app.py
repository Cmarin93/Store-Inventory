#!/usr/bin/env python3
import datetime
import csv
from peewee import *


db = SqliteDatabase('inventory.db')


def fetch_products_from_csv():
    ''' convert csv to a list of ordered dictionaries'''
    with open('inventory.csv', newline='') as csvfile:
        products = list(csv.DictReader(csvfile)) 
    return products

class Product(Model):  
    #product_id = AutoField(unique=True)
    product_name = CharField(max_length=75, unique=True)
    product_price = IntegerField(default=0)
    product_quantity = IntegerField(default=0)
    #date_updated = DateField()

    class Meta: #telling the model which database it belongs to.
        database = db


def add_products():
    products = fetch_products_from_csv()
    for product in products:
        product_record = Product.get_or_create(product_name=product.get('product_name'))
        try:
            quantity = int(product.get('product_quantity'))
        except TypeError:
            quantity = 0
        product_record[0].product_quantity = quantity
        try:
            price = product.get('product_price')
        except TypeError:
            price = 0
        product_record[0].product_price = price
        print(product_record)
        product_record[0].save()
        if not product_record[1]: # if product was not added to db
            print("WAS NOT ADDED")



        # save()
        # try:
        #     # price = cleaned up price value
        # except:
        #     # price = default price value
       

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    add_products()
    db.close()















    #  3/27/2020 - carlos a marin





            #if quantity is not None:
            #     quantity = int(quantity)
            # else: 
            #     quantity = 0




            #         # 
            # product_record = Product.get(product_name=product['name']) #gets product out of db
            # if product_record.product_price != product['price']:
            #     print(f"The price of {product_record.product_name} has changed from {product_record.product_price} to {product['price']}.")
            #     product_record.product_price = product['price'] # set new price
            # product_record.save()



