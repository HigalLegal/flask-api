from flask import Flask, render_template
from flask_restful import Api
from models import db, ma
from resources import TutorResource, PetResource

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

api.add_resource(TutorResource, '/tutor', '/tutor/<int:tutor_id>')
api.add_resource(PetResource, '/pet', '/pet/<int:pet_id>')

if __name__ == '__main__':
    app.run(debug=True)