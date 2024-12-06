from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import enum


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class Sex(enum.Enum):
    male = 1
    female = 2
    undefined = 3

    def __int__(self):
        return self.value


class RetrievalType(enum.Enum):
    preop = 1
    operational = 2
    postop = 3
    unknown = 4

    def __int__(self):
        return self.value


class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.Date, nullable=False)
    sex = db.Column(Enum(Sex), nullable=False)
    consent = db.Column(db.Boolean, nullable=False)

    def __init__(self, id, birth_date, sex, consent):
        self.id = id
        self.birth_date = birth_date
        self.sex = sex
        self.consent = consent


class Tissue(db.Model):
    __tablename__ = "tissue"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    biopsy_id = db.Column(db.String(128))
    predictive_id = db.Column(db.String(128))
    samples_no = db.Column(db.Integer)
    available_samples_no = db.Column(db.Integer)
    material_type_id = db.Column(db.Integer, db.ForeignKey('material_type.id'))
    diagnosis = db.Column(db.String(128))
    ptnm = db.Column(db.String(128))
    morphology = db.Column(db.String(128))
    cut_time = db.Column(db.DateTime)
    freeze_time = db.Column(db.DateTime)
    retrieved = db.Column(Enum(RetrievalType))

    def __init__(self, sample_id, patient_id, biopsy_id, predictive_id, samples_no, available_samples_no, material_type_id, diagnosis, ptnm, morphology, cut_time, freeze_time, retrieved):
        self.sample_id = sample_id
        self.patient_id = patient_id
        self.biopsy_id = biopsy_id
        self.predictive_id = predictive_id
        self.samples_no = samples_no
        self.available_samples_no = available_samples_no
        self.material_type_id = material_type_id
        self.diagnosis = diagnosis
        self.ptnm = ptnm
        self.morphology = morphology
        self.cut_time = cut_time
        self.freeze_time = freeze_time
        self.retrieved = retrieved


class Serum(db.Model):
    __tablename__ = "serum"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    biopsy_id = db.Column(db.String(128))
    predictive_id = db.Column(db.String(128))
    samples_no = db.Column(db.Integer)
    available_samples_no = db.Column(db.Integer)
    material_type_id = db.Column(db.Integer, db.ForeignKey('material_type.id'))
    diagnosis = db.Column(db.String(128))
    taking_date = db.Column(db.Date)

    def __init__(self, sample_id, patient_id, biopsy_id, predictive_id, samples_no, available_samples_no, material_type_id, diagnosis, taking_date):
        self.sample_id = sample_id
        self.patient_id = patient_id
        self.biopsy_id = biopsy_id
        self.predictive_id = predictive_id
        self.samples_no = samples_no
        self.available_samples_no = available_samples_no
        self.material_type_id = material_type_id
        self.diagnosis = diagnosis
        self.taking_date = taking_date


class Genome(db.Model):
    __tablename__ = "genome"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    biopsy_id = db.Column(db.String(128))
    predictive_id = db.Column(db.String(128))
    samples_no = db.Column(db.Integer)
    available_samples_no = db.Column(db.Integer)
    material_type_id = db.Column(db.Integer, db.ForeignKey('material_type.id'))
    retrieved = db.Column(Enum(RetrievalType))
    taking_date = db.Column(db.Date)

    def __init__(self, sample_id, patient_id, biopsy_id, predictive_id, samples_no, available_samples_no, material_type_id, retrieved, taking_date):
        self.sample_id = sample_id
        self.patient_id = patient_id
        self.biopsy_id = biopsy_id
        self.predictive_id = predictive_id
        self.samples_no = samples_no
        self.available_samples_no = available_samples_no
        self.material_type_id = material_type_id
        self.retrieved = retrieved
        self.taking_date = taking_date


class Cell(db.Model):
    __tablename__ = "cell"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    biopsy_id = db.Column(db.String(128))
    predictive_id = db.Column(db.String(128))
    samples_no = db.Column(db.Integer)
    available_samples_no = db.Column(db.Integer)
    material_type_id = db.Column(db.Integer, db.ForeignKey('material_type.id'))

    def __init__(self, sample_id, patient_id, biopsy_id, predictive_id, samples_no, available_samples_no, material_type_id):
        self.sample_id = sample_id
        self.patient_id = patient_id
        self.biopsy_id = biopsy_id
        self.predictive_id = predictive_id
        self.samples_no = samples_no
        self.available_samples_no = available_samples_no
        self.material_type_id = material_type_id


class DiagnosisMaterial(db.Model):
    __tablename__ = "diagnosis_material"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    material_type_id = db.Column(db.Integer, db.ForeignKey('material_type.id'))
    diagnosis = db.Column(db.String(128))
    taking_date = db.Column(db.Date)
    retrieved = db.Column(Enum(RetrievalType))

    def __init__(self, sample_id, patient_id, taking_date, diagnosis, retrieved, material_type_id):
        self.sample_id = sample_id
        self.patient_id = patient_id
        self.taking_date = taking_date
        self.diagnosis = diagnosis
        self.retrieved = retrieved
        self.material_type_id = material_type_id


class MaterialType(db.Model):
    __tablename__ = "material_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    key = db.Column(db.String(128))

    def __init__(self, name, key):
        self.name = name
        self.key = key


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/api/patients_with_consent", methods=["GET"])
def api_get_patients_with_consent():
    patients = db.session.execute(db.select(Patient).filter_by(consent=True)).all()

    res = [{
        "ID": patient[0].id,
        "Birth date": patient[0].birth_date,
        "Sex": int(patient[0].sex),
        "Consent": patient[0].consent,
    } for patient in patients]

    return jsonify(
        values=res
    )


def __convert_to_dict(val, mat_type_dict):

    res = {
        "type": "Cell",
        "ID": val.id,
        "predictive_id": val.predictive_id,
        "sample_id": val.sample_id,
        "biopsy_id": val.biopsy_id,
        "patient_id": val.patient_id,
        "samples_no": val.samples_no,
        "available_samples_no": val.available_samples_no,
        "material_type_id": mat_type_dict[val.material_type_id]
    }

    if isinstance(val, Tissue):
        res["type"] = "Tissue"
        res["diagnosis"] = val.diagnosis
        res["ptnm"] = val.ptnm
        res["morphology"] = val.morphology
        res["cut_time"] = val.cut_time
        res["freeze_time"] = val.freeze_time
        res["retrieved"] = str(val.retrieved)
    elif isinstance(val, Genome):
        res["type"] = "Genome"
        res["retrieved"] = str(val.retrieved)
        res["taking_date"] = val.taking_date
    elif isinstance(val, Serum):
        res["type"] = "Serum"
        res["diagnosis"] = val.diagnosis
        res["taking_date"] = val.taking_date

    return res


@app.route("/api/specimen/<pred_number>", methods=["GET"])
def api_get_tissue_by_id(pred_number):
    mat_type_dict = dict([(val[0].id, val[0].key) for val in db.session.execute(db.select(MaterialType)).all()])

    pred_number = pred_number.replace("-", "/")
    tissues = db.session.execute(db.select(Tissue).filter_by(predictive_id=pred_number)).all()
    serums = db.session.execute(db.select(Serum).filter_by(predictive_id=pred_number)).all()
    genomes = db.session.execute(db.select(Genome).filter_by(predictive_id=pred_number)).all()
    cells = db.session.execute(db.select(Cell).filter_by(predictive_id=pred_number)).all()

    specimen = tissues + serums + genomes + cells
    res = [__convert_to_dict(spec[0], mat_type_dict) for spec in specimen]

    return jsonify(res), 200


@app.route("/api/patient/<id>", methods=["GET"])
def get_patient_by_id(id):
    patient = db.session.get(Patient, id)
    if patient is not None:
        return jsonify({
            "ID": patient.id,
            "birth_date": patient.birth_date,
            "sex": int(patient.sex),
            "consent": patient.consent
        }), 200
    else:
        return jsonify(None), 404
