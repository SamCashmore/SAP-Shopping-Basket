from flask import Flask, request, render_template
from api_requests import get_quantity_from_api, post_reservation
import os

app = Flask(__name__)

port = int(os.environ.get('PORT', 3000))

product_list = [
        {
            'id': 'DYSON-248F-TORQUE-IR',
            'name': 'Dyson V11',
            'price': 100,
            'image': 'image1.jpg'
        },
        {
            'id': 2,
            'name': 'Dyson Big Ball Multi Floor 2 vacuum',
            'price': 150,
            'image': 'image2.jpeg'
        },
        {
            'id': 3,
            'name': 'Dyson 360 Heurist',
            'price': 150,
            'image': 'image3.jpeg'
        }
    ]

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/products')
def products():
    return render_template('products.html', products = product_list)

@app.route('/products/<product_id>')
def product(product_id):
    product_item = next((product for product in product_list if product['id'] == product_id), None)
    if product_item is not None:
        quantity = get_quantity_from_api(product_item['id'])
        return render_template('product.html', product = product_item, quantity = quantity)
    else:
        return 'Product does not exist'
    # Apply conditional for 'None' either here or in html

@app.route('/add_to_basket/<product_id>')
def add_to_basket(product_id):
    return 'Adds to basket - Use API...'

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=port)