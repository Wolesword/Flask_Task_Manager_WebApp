# install pip install pipenv
# Pipenv install flask flask-sqlalchemy flaks-marshamllow marshmallow-sqlalchemy
# Touch app.py (create a file app.py)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os  # file path , database file

# init App
app = Flask(__name__)  # create me app

basedir = os.path.abspath(os.path.dirname(__file__))  # base directory

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
# looks for db.sqlite in the base directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init Db
db = SQLAlchemy(app)
# Init Marshmallow
ma = Marshmallow(app)


# Product Class / Model

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# Product Schema
class ProductsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


# Init Schema
product_Schema = ProductsSchema()  # alternative if error ProductsSchema(Strict = True)
products_Schema = ProductsSchema(many=True)


# Test port 5000
@app.route('/', methods=['GET'])
def test_the_thing():
    one_product = Product.query.first()
    output = products_Schema.dump(one_product).data
    return jsonify({'user': output})  # f'This is a new test code!'


# Create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)  # data from postman or our clients, __init__ function

    db.session.add(new_product)
    db.session.commit()

    return products_Schema.jsonify(new_product)


# Get All products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_Schema.dump(all_products)

    return jsonify(result)


# Get single products
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    return products_Schema.jsonify(product)
    # return str(id)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)

# https://www.youtube.com/watch?v=PTZiDnuC86g&ab_channel=TraversyMedia
# There are still some issues with this code to review
