from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False )

class PatientRegistration(db.Model):
    __tablename__ = 'patient_registration'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(80), unique=True, nullable=False)
    patient_data = db.relationship('PatientData', backref='registration', lazy=True)
    next_of_kin = db.relationship('NextofKin', backref='registration', lazy=True)

class PatientData(db.Model):
    __tablename__ = 'patient_data' 

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_registration.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    temperature = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.String(80), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    complaint = db.Column(db.String(255), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=False)
    treatment = db.Column(db.String(255), nullable=False)

class NextofKin(db.Model):
    __tablename__='next_of_kin'

    id=db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_registration.id'), nullable=False)
    next_of_kin=db.Column(db.String(255),nullable=False)
    next_of_kin_contact=db.Column(db.String(255),nullable=False)