import os
from setting import load_model, data_transform
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime

def input_data():
    parser.add_argument('age', type=int, required=True)
    parser.add_argument('sex', type=str, required=True, choices=("F", "M"))
    parser.add_argument('chestPainType', type=str, required=True, choices=("ATA", "NAP", "ASY", "TA"))
    parser.add_argument('restingBP', type=int, required=True)
    parser.add_argument('cholesterol', type=int, required=True)
    parser.add_argument('fastingBS', type=int, required=True, choices=(0, 1))
    parser.add_argument('restingECG', type=str, required=True, choices=("Normal", "ST", "LVH"))
    parser.add_argument('maxHR', type=int, required=True)
    parser.add_argument('exerciseAngina', type=str, required=True, choices=("Y", "N"))
    parser.add_argument('oldpeak', type=float, required=True)
    parser.add_argument('ST_Slope', type=str, required=True, choices=("Up", "Flat", "Down"))

based_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(based_dir, 'clothes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app,doc='/',title="My REST API")
db = SQLAlchemy(app)

model = load_model()
parser = reqparse.RequestParser()

input_data()

class Cloth(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    character_from = db.Column(db.String(80), nullable=False)
    product_type = db.Column(db.String(20), nullable=False)
    shop_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return self.product_name

clothes_model = api.model(
    'Cloth',
    {
        'id' : fields.Integer(),
        'product_name' : fields.String(),
        'character_from' : fields.String(),
        'product_type' : fields.String(),
        'shop_name' : fields.String(),
        'price' : fields.Integer(),
        'date_joined' : fields.String()
    }
)

@api.route('/heart_failure')
@api.expect(parser)
class Heart_Failure(Resource):
    def get(self):
        ''' Heart Failure Prediction '''
        age = request.args.getlist('age')[0]
        sex = request.args.getlist('sex')[0]
        chestPainType = request.args.getlist('chestPainType')[0]
        restingBP = request.args.getlist('restingBP')[0]
        cholesterol = request.args.getlist('cholesterol')[0]
        fastingBS = request.args.getlist('fastingBS')[0]
        restingECG = request.args.getlist('restingECG')[0]
        maxHR = request.args.getlist('maxHR')[0]
        exerciseAngina = request.args.getlist('exerciseAngina')[0]
        oldpeak = request.args.getlist('oldpeak')[0]
        ST_Slope = request.args.getlist('ST_Slope')[0]

        input_dict = {"age":int(age), "sex":sex, "chestPainType":chestPainType,
                      "restingBP":int(restingBP), "cholesterol":int(cholesterol), "fastingBS":int(fastingBS),
                      "restingECG":restingECG, "maxHR":int(maxHR), "exerciseAngina":exerciseAngina,
                      "oldpeak":float(oldpeak), "ST_Slope":ST_Slope}

        transform_dict = data_transform(input_dict)
        transform_list = [list(transform_dict.values())]

        pred = model.predict(transform_list)
        pred_proba = model.predict_proba(transform_list)[0][pred[0]]
        target_dict = {0:"Not disease", 1:"Disease"}
        pred_dict = {"Prediction":target_dict[pred[0]], "Probability":float(pred_proba)}
        return jsonify(pred_dict)

@api.route('/clothes')
class Clothes(Resource):

    @api.errorhandler(fields.MarshallingError)
    def handle_exception(error):
        '''Return a custom message and 500 status code'''
        message = "Error: " + getattr(error, 'message', str(error))
        return {'message': message}, getattr(error, 'code', 500)

    @api.marshal_list_with(clothes_model,code=200,envelope="clothes")
    def get(self):
        clothes = Cloth.query.all()
        return clothes
    
    @api.marshal_with(clothes_model,code=201,envelope="cloth")
    @api.doc(params={'product_name':'Product Name', 'character_from':'From Anime/Game', 'product_type':'Product Type',
                     'shop_name':'Shop Name', 'price':'Price'})
    def post(self):

        product_name = request.args.get("product_name")
        character_from = request.args.get("character_from")
        product_type = request.args.get("product_type")
        shop_name = request.args.get("shop_name")
        price = request.args.get("price")

        new_clothes = Cloth(product_name=product_name, character_from=character_from, product_type=product_type,
                              shop_name=shop_name, price=price)
        
        try:
            db.session.add(new_clothes)
            db.session.commit()
            return new_clothes
        except exc.IntegrityError:
            return jsonify({"Message":"Error"})

@api.route('/clothes<int:id>')
class Clothes(Resource):

    @api.errorhandler(fields.MarshallingError)
    def handle_exception(error):
        '''Return a custom message and 500 status code'''
        message = "Error: " + getattr(error, 'message', str(error))
        return {'message': message}, getattr(error, 'code', 500)

    @api.marshal_with(clothes_model,code=200,envelope="book")
    def get(self, id):
        cloth = Cloth.query.get_or_404(id)
        return cloth, 200

    @api.marshal_with(clothes_model,code=200,envelope="book")
    @api.doc(params={'product_name':'Product Name', 'character_from':'From Anime/Game', 'product_type':'Product Type',
                     'shop_name':'Shop Name', 'price':'Price'})
    def put(self, id):
        cloth_to_update = Cloth.query.get_or_404(id)

        cloth_to_update.product_name = request.args.get('product_name')
        cloth_to_update.character_from = request.args.get('character_from')
        cloth_to_update.product_type = request.args.get('product_type')
        cloth_to_update.shop_name = request.args.get('shop_name')
        cloth_to_update.price = request.args.get('price')

        try:
            db.session.commit()
            return cloth_to_update, 200
        except exc.IntegrityError:
            return jsonify({"Message":"Error"})

    @api.marshal_with(clothes_model,code=200,envelope="cloth_deleted")
    def delete(self, id):
        cloth_to_del = Cloth.query.get_or_404(id)

        db.session.delete(cloth_to_del)
        db.session.commit()

        return cloth_to_del, 200

@app.shell_context_processor
def make_shell_context():
    return {
        'db':db,
        'Cloth':Cloth
    }

if __name__=="__main__":
    app.run(debug=True)