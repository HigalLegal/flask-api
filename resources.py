from flask_restful import Resource, reqparse, abort
from flask import jsonify
from models import db,Tutor,Pet,TutorSchema,PetSchema

class TutorResource(Resource):
    def get(self, tutor_id=None):
        if tutor_id is None:
            tutor = Tutor.query.all()
            return TutorSchema(many=True).dumps(tutor),200
        
        tutor = Tutor.query.get(tutor_id)
        tutorschema = TutorSchema()
        result = tutorschema.dump(tutor)
        return jsonify(result)
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True, help='Nome do Tutor')
        parser.add_argument('pets', type=list, location='json', required=True, help='Lista de Pets')
        args = parser.parse_args()

        novo_tutor = Tutor(nome=args['nome'])

        print(args)
        for pet_data in args['pets']:
            novo_pet = Pet()
            novo_pet.nome = pet_data['nome']
            
            novo_tutor.pets.append(novo_pet)

        db.session.add(novo_tutor)
        db.session.commit()

        return {'message': 'Tutor e Pets cadastrados com sucesso'}, 201
    
    def delete(self, tutor_id=None):
        if tutor_id is None:
            abort(404, message="ID {} do tutor não encontrado".format(tutor_id))
        Tutor.query.filter_by(id=tutor_id).delete()
        db.session.commit()

        return jsonify(msg = {
            "Resposta": "Tutor do id {} deletado com sucesso!".format(tutor_id)
        })
    
    def put(self, tutor_id=None):
        if tutor_id is None:
            abort(404, message="ID {} do tutor não encontrado".format(tutor_id))
            
        parser = reqparse.RequestParser()
        parser.add_argument('nomeTutor', type=str, required=True)
        args = parser.parse_args()
        
        tutor = Tutor.query.get(tutor_id)
        tutor.nome = args["nomeTutor"]
        
        db.session.commit()
        return TutorSchema().dump(tutor), 200
    
class PetResource(Resource):
    
    def get(self, pet_id=None):
        if pet_id is None:
            pet = Pet.query.all()
            return PetSchema(many=True).dumps(pet),200

        pet = Pet.query.get(pet_id)
        return PetSchema().dump(pet), 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nomePet', type=str, required=True)
        parser.add_argument('tutorId', type=int, required=True)
        args = parser.parse_args()

        pet = Pet(nome=args['nomePet'], tutor_id=args['tutorId'])
        db.session.add(pet)
        db.session.commit()
        return TutorSchema().dump(pet), 201
    
    def put(self, pet_id=None):
        if pet_id is None:
            abort(404, message="ID pet não encontrado")
        
        parser = reqparse.RequestParser()
        parser.add_argument('nomePet', type=str, required=True)
        parser.add_argument('tutorId', type=int, required=True)
        args = parser.parse_args()

        pet = Pet.query.get(pet_id)

        pet.nome = args["nomePet"]
        pet.tutor_id = args["tutorId"]

        db.session.commit()
        return TutorSchema().dump(pet), 200
    
    def delete(self, pet_id=None):
        
        if pet_id is None:
             abort(404, message="Recurso não encontrado")
        Pet.query.filter_by(id=pet_id).delete()
        db.session.commit()

        return jsonify(msg = {
            "Resposta": "Pet {} deletado com sucesso.".format(pet_id)
        })