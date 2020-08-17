from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/HCAPP2.db'
db = SQLAlchemy(app)
app.secret_key = 'shalusecretkey'


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(12), nullable=False)

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password


class Patient(User):

    id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    race = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    doctor_num = db.Column(db.Integer, nullable=True)

    def set_weight(self, weight):
        self.weight = weight

    def set_height(self, height):
        self.height = height


class Organization(User):

    id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    organizationName = db.Column(db.String(50), nullable=False)
    organization_speciality = db.Column(db.String(50), nullable=False)

    def add_members(self, doctor):
        doctor.organization_speciality = self.organization_speciality
        doctor.organizationID = self.id

    def add_patient(self, doctor, patient):
         return patient_of_db(org_id=self.id, doc_id=doctor.id, patient_id=patient.id)

    def add_record(self, path, doctor, patient):
        return Record(org_id=self.id, record_path=path, doc_id=doctor.id, patient_id=patient.id)

    @staticmethod
    def change_username(doctor, username):
        doctor.username = username

    @staticmethod
    def change_password(doctor, password):
        doctor.password = password


class Doctor(User):

    id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    organization_speciality = db.Column(db.String(50), nullable=True)
    organizationID = db.Column(db.Integer, nullable=True)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_path = db.Column(db.String(200), unique=True)
    org_id = db.Column(db.Integer, nullable=False)
    doc_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)


class patient_of_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, nullable=False)
    doc_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)


db.create_all()
