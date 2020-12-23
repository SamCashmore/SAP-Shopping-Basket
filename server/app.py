from flask import Flask, request, render_template, jsonify
from api_requests import get_quantity_from_api, post_reservation, get_reservations
import os

app = Flask(__name__)

port = int(os.environ.get('PORT', 3000))

product_list = [
        {
            'id': 'DYSON-248F-TORQUE-IR',
            'name': 'Dyson V11',
            'price': 549,
            'image': 'image3.jpg',
            'products_image': 'image2.jpg'
        },
        {
            'id': '2',
            'name': 'Dyson Big Ball Multi Floor 2 vacuum',
            'price': 249,
            'image': 'image1.jpeg',
            'products_image': 'image2.jpg'
        },
        {
            'id': '3',
            'name': 'Dyson 360 Heurist',
            'price': 799.99,
            'image': 'image1.jpeg'
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

@app.route('/products/<product_id>', methods=['GET', 'POST'])
def product(product_id):
    if request.method == 'POST':
        product_id = request.form.get('formProductId')
        quantity = request.form.get('formQuantity')
        postcode = request.form.get('formPostcode')
        return product_id, quantity, postcode
    else:
        product_item = next((product for product in product_list if product['id'] == product_id), None)
        if product_item is not None:
            try:
                quantity = get_quantity_from_api(product_item['id'])
            except:
                quantity = 0
            return render_template('product.html', product = product_item, quantity = quantity)
        else:
            return 'Product does not exist'
        # Apply conditional for 'None' either here or in html

@app.route('/add_to_basket/<product_id>', methods=['GET', 'POST'])
def add_to_basket(product_id):
    return 'Adds to basket - Use API...'

@app.route('/reserve_products', methods=['POST'])
def reserve_products():
    product_id = request.form['formProductId']
    quantity = request.form['formQuantity']
    postcode = request.form['formPostcode']
    try:
        result = post_reservation(product_id, quantity, postcode)
    except:
        result = None
        print('ERRORS')
    product_item = next((product for product in product_list if product['id'] == product_id), None)
    if product_item is not None and result is not None:
        return render_template('reserve_products.html', product=product_item, reservation_details=result)
    else:
        print('Error reserving product')
        return render_template('errorPages/reserve_products.html')

# test_data = {
#   "DYSON-248F-TORQUE-IR": [
#     {
#       "reservationId": "4ba8ab91-76d7-4476-bcfe-62feeba3c911",
#       "quantity": 1.0,
#       "sourceId": "abc123",
#       "sourceType": "STORE",
#       "reservationTime": "2020-12-15T10:40:26.174Z",
#       "expiryTime": "2020-12-22T10:40:26.174Z"
#     },
#     {
#       "reservationId": "cfc999d4-13f0-499d-832e-90e250a36fb7",
#       "quantity": 3.0,
#       "sourceId": "abc123",
#       "sourceType": "STORE",
#       "reservationTime": "2020-12-20T18:12:31.606Z",
#       "expiryTime": "2020-12-20T18:42:31.606Z"
#     },
#     {
#       "reservationId": "5527cf57-3b70-45e5-916c-3be221e27dbf",
#       "quantity": 2.0,
#       "sourceId": "abc123",
#       "sourceType": "STORE",
#       "reservationTime": "2020-12-20T18:12:50.519Z",
#       "expiryTime": "2020-12-20T18:42:50.519Z"
#     }
#   ],
#   "2": [
#     {
#       "reservationId": "4ba8ab91-76d7-4476-bcfe-62feeba3c911",
#       "quantity": 1.0,
#       "sourceId": "abc123",
#       "sourceType": "STORE",
#       "reservationTime": "2020-12-15T10:40:26.174Z",
#       "expiryTime": "2020-12-22T10:40:26.174Z"
#     },
#     {
#       "reservationId": "cfc999d4-13f0-499d-832e-90e250a36fb7",
#       "quantity": 3.0,
#       "sourceId": "abc123",
#       "sourceType": "STORE",
#       "reservationTime": "2020-12-20T18:12:31.606Z",
#       "expiryTime": "2020-12-20T18:42:31.606Z"
#     },
#     {
#       "reservationId": "5527cf57-3b70-45e5-916c-3be221e27dbf",
#       "quantity": 2.0,
#       "sourceId": "abc123",
#       "sourceType": "STORE",
#       "reservationTime": "2020-12-20T18:12:50.519Z",
#       "expiryTime": "2020-12-20T18:42:50.519Z"
#     }
#   ],
# }

@app.route('/reservations')
def reservations():
    reservations_dict = get_reservations()
    # reservations_dict = test_data
    reserved_products = []
    for product in product_list:
        if product['id'] in reservations_dict:
            product['reservations'] = reservations_dict[product['id']]
            reserved_products.append(product)
    return render_template('reservations.html', reserved_products=reserved_products)

@app.route('/reservations2')
def reservations2():
    reservations_dict = get_reservations()
    reserved_products = []
    for product in product_list:
        if product['id'] in reservations_dict:
            product['reservations'] = reservations_dict[product['id']]
            reserved_products.append(product)
    return jsonify(reserved_products)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=port, debug=True)
