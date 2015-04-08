"""This module helps for uploading and downloading inappproducts from/to play."""
import os
import json
from file_util import mkdir_p
from file_util import list_dir_abspath

def upload(client, source_dir):
    """Upload inappproducts to play store."""
    print('')
    print('upload inappproducs')
    print('---------------------')

    products_folder = os.path.join(source_dir, 'products')
    product_files = filter(os.path.isfile, list_dir_abspath(products_folder))

    current_product_skus = map(lambda product: product['sku'], client.list_inappproducts())
    print(current_product_skus)
    for product_file in product_files:
        with open(product_file) as product_file:
            product = json.load(product_file)
        #check if the product is new
        sku = product['sku']
        product['packageName'] = client.package_name
        print(sku)
        if sku in current_product_skus:
            print("update product {0}".format(sku))
            client.update_inappproduct(product, sku)
        else:
            print("create product {0}".format(sku))
            client.insert_inappproduct(product)


def download(client, target_dir):
    """Download inappproducts from play store."""
    print('')
    print("download inappproducts")
    print('---------------------')
    products = client.list_inappproducts()

    for product in products:
        path = os.path.join(target_dir, 'products')
        del product['packageName']
        mkdir_p(path)
        with open(os.path.join(path, product['sku'] + '.json'), 'w') as outfile:
            print("save product for {0}".format(product['sku']))
            json.dump(
                product, outfile, sort_keys=True,
                indent=4, separators=(',', ': '))
