#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )


@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get("name"),
        price=data.get("price"),
        bakery_id=data.get("bakery_id")
    )
    db.session.add(new_baked_good)
    db.session.commit()
    baked_good_dict = new_baked_good.to_dict()
    response = make_response(baked_good_dict, 201)
    return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        response_body = {"message": "Bakery not found"}
        response = make_response(response_body, 404)
        return response
    
    data = request.form
    new_name = data.get('name')
    if new_name:
        bakery.name = new_name
        db.session.commit()
        bakery_dict = bakery.to_dict()
        response = make_response(bakery_dict, 200)
    else:
        response_body = {"message": "No changes to be made"}
        response = make_response(response_body, 400)
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        response_body = {"message": "Baked good not found"}
        response = make_response(response_body, 404)
        return response

    db.session.delete(baked_good)
    db.session.commit()
    response_body = {"message": "Baked good deleted successfully"}
    response = make_response(response_body, 200)
    return response









if __name__ == '__main__':
    app.run(port=5555, debug=True)