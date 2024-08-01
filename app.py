from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from config import Config 
from models import db

migrate = Migrate()
bcrypt=Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app

app = create_app()

@app.route("/signup", methods=["POST"])
def signup():
    from models import User
    body=request.get_json()
    username=body['username']
    email=body['email']
    role=body['role']
    password=body['password']
    hashed_password=bcrypt.generate_password_hash(password).decode("utf-8")
    user=User(username=username,email=email,role=role,password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"Hello new user"}),200
@app.route("/login",methods=['POST'])
def login():
    from models import User
    body=request.get_json()
    email=body['email']
    password=body['password']
    user=User.query.filter_by(email=email).first()
    if user:
        checked_pass=bcrypt.check_password_hash(user.password.encode("utf-8"),password)
        if checked_pass:
         access_token=create_access_token(identity={"id":user.id,"name":user.username})
         return jsonify({"message":"Success"},{"token":access_token}),200
        else:
            return jsonify({"error":"Invalid password"}),401
    elif not user:
        return jsonify({"error":"Invalid email address"}),401

@app.route ("/registration",methods=["POST"]) 
@jwt_required() 
def registration():
    from  models import  PatientRegistration 
    body=request.get_json()
    name=body['name']
    gender=body['gender']
    age=body['age']
    address=body['address']
    contact=body['contact']
    data=PatientRegistration(name=name,gender=gender,age=age,address=address,contact=contact)
    db.session.add(data)
    db.session.commit()
    return jsonify({"message":"patient registered successfuly"}),201


@app.route("/patient_data",methods=['POST'])
@jwt_required()
def add_patient_data():
    from models import PatientData
    body=request.get_json() 
    patient_id=body["patient_id"] 
    temperature=body["temperature"]
    blood_pressure=body["blood_pressure"]
    weight=body["weight"]
    complaint=body["complaint"]
    diagnosis=body["diagnosis"]
    treatment=body["treatment"]
    patient_data=PatientData(patient_id=patient_id,temperature=temperature,
                             blood_pressure=blood_pressure,weight=weight,complaint=complaint,
                             diagnosis=diagnosis,treatment=treatment)
    db.session.add(patient_data)
    db.session.commit()
    return jsonify({"message":"patient data updated successfully"}),201


@app.route('/registration/<int:patient_id>', methods=['PATCH'])
def update_registration(patient_id):
    from models import PatientRegistration
    existing_patient=PatientRegistration.query.get(patient_id)
    if not existing_patient:
        return jsonify({"error":"Patient not found"}),404
    
    updated_patient=request.get_json()
    if 'name' in updated_patient:
        existing_patient.name=updated_patient['name']
    if 'gender' in updated_patient:
        existing_patient.gender=updated_patient['gender']
    if 'age' in updated_patient:
        existing_patient.age=updated_patient['age']
    if 'address' in updated_patient:
        existing_patient.address=updated_patient['address']
    if 'contact' in updated_patient:
        existing_patient.contact=updated_patient['contact']

    db.session.commit()
    return jsonify({"message":"Patient updated successfully"}),200

@app.route('/patient_data/<int:patient_id>', methods=['PATCH'])
def get_patient_data(patient_id):
        from models import PatientData
        existing_patient = PatientData.query.get(patient_id)
        if not existing_patient:
            return jsonify({"error":"Patient data not found"}),404
        updated_patient_data = request.get_json()
        if 'temperature' in updated_patient_data:
            existing_patient.temperature = updated_patient_data['temperature']
        if 'blood_pressure' in updated_patient_data:
            existing_patient.blood_pressure = updated_patient_data['blood_pressure']
        if 'weight' in updated_patient_data:
            existing_patient.weight = updated_patient_data['weight']
        if 'complaint' in updated_patient_data:
            existing_patient.complaint = updated_patient_data['complaint']
        if 'diagnosis' in updated_patient_data:
            existing_patient.diagnosis = updated_patient_data['diagnosis']
        if 'treatment' in updated_patient_data:
            existing_patient.treatment = updated_patient_data['treatment']
            
        db.session.commit()
        return jsonify({"message":"Patient data updated successfully"}),200

@app.route("/registration/<int:id>", methods=['DELETE'])
def delete_patient(id):
        from models import PatientRegistration
        deleting_patient=PatientRegistration.query.get(id)
        if not deleting_patient:
            return jsonify({"error": "patient not found"}), 404
        
        db.session.delete(deleting_patient)
        db.session.commit()
        return jsonify({"message":"patient deleted successfully"})
    

if __name__ == '__main__':
    app.run(debug=True)