#!/usr/bin/env python3
import datetime
import csv
from peewee import *


db = SqliteDatabase('inventory.db')

# with open('inventory.csv', 'r', newline='') as csvfile:
#      inventory = csv.reader(csvfile)
#      next(inventory) # skips first line.
#      for item in inventory:
#          print(item[0])


class Product(Model):  
    #product_id = AutoField(unique=True)
    product_name = CharField(max_length=75, unique=True)
    product_price = IntegerField()
    #product_quantity = IntegerField(default=0)
    #date_updated = DateTimeField(datetime.datetime.now())

    class Meta: #telling the model which database it belongs to.
        database = db



products = [
    {
    'name': 'apple',
    'price': '$1.29'},
    {
    'name': 'banana',
    'price': '$1.98'},
    {
    'name': 'carrot',
    'price': '$2.79'}
] 

def add_products():
    for product in products:
        try:
            Product.create(product_name=product['name'], product_price=product['price'])
        except IntegrityError:
            product_record = Product.get(product_name=product['name']) #gets product out of db
            if product_record.product_price != product['price']:
                print(f"The price of {product_record.product_name} has changed from {product_record.product_price} to {product['price']}.")
                product_record.product_price = product['price'] # set new price
            product_record.save()


def cheapest_product():
    cheap = Product.select().order_by(Product.product_price.asc()).get()
    return cheap.product_name

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    add_products()
    print(f"The cheapest product is: {cheapest_product()}")
    db.close()


    #  3/25/2020 - carlos a marin
