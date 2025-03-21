from flask.cli import FlaskGroup
import xml.etree.ElementTree as ET
import os
from project import app, db, Patient, Tissue, Cell, Serum, Genome, DiagnosisMaterial, Sex, RetrievalType, MaterialType

cli = FlaskGroup(app)

XLM_PREFIX = "{http://www.bbmri.cz/schemas/biobank/data}"

bool_dict = {
    "true": True,
    "false": False
}

sex_dict = {
    "male": Sex.male,
    "female": Sex.female,
    "undefined": Sex.undefined,
}

retrieval_type_dict = {
    "preop": RetrievalType.preop,
    "operational": RetrievalType.operational,
    "postop": RetrievalType.postop,
    "unknown": RetrievalType.unknown
}


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(MaterialType("Nádor maligní", "1"))
    db.session.add(MaterialType("Metastáza", "2"))
    db.session.add(MaterialType("Nádor benigní", "3"))
    db.session.add(MaterialType("Zdravá tkáň", "4"))
    db.session.add(MaterialType("Premaligní tkáň", "5"))
    db.session.add(MaterialType("Maligní (RNA-LATER)", "53"))
    db.session.add(MaterialType("Zdravá (RNA-LATER)", "54"))
    db.session.add(MaterialType("Metastáza (RNA-LATER)", "55"))
    db.session.add(MaterialType("Benigní (RNA-LATER)", "56"))
    db.session.add(MaterialType("PBMNC", "7"))
    db.session.add(MaterialType("Genomová DNA", "gD"))
    db.session.add(MaterialType("Plazma Li-heparin dusík", "L"))
    db.session.add(MaterialType("Plasma dusík", "PD"))
    db.session.add(MaterialType("Plná krev", "PK"))
    db.session.add(MaterialType("Primokultury", "PR"))
    db.session.add(MaterialType("Sérum", "S"))
    db.session.add(MaterialType("Sérum dusík", "SD"))
    db.session.add(MaterialType("Plazma CTAD dusík", "T"))
    db.session.add(MaterialType("Plazma K3EDTA dusík", "K"))
    db.session.add(MaterialType("Plná krev se stabilizátorem DNA", "PS"))
    db.session.add(MaterialType("Plazma se stabilizátorem DNA", "C"))
    db.session.commit()


def _process_xml_export(rt):
    mat_type_dict = dict([(val[0].key, int(val[0].id)) for val in db.session.execute(db.select(MaterialType)).all()])
    sample_data = []
    lts = rt.find(f"{XLM_PREFIX}LTS")
    birth_date = f'{rt.get("month").replace("--", "")}-01-{rt.get("year")}'
    sample_data.append(Patient(
        id=rt.get("id"),
        birth_date=birth_date,
        sex=sex_dict[rt.get("sex")],
        consent=bool_dict[rt.get("consent")]))
    if lts is not None:
        for child in lts:
            if "tissue" in child.tag:
                sample_data.append(Tissue(
                    sample_id=child.get("sampleId"),
                    patient_id=rt.get("id"),
                    biopsy_id=child.get("biopsy"),
                    predictive_id=child.get("predictive_number"),
                    samples_no=child.find(f"{XLM_PREFIX}samplesNo").text,
                    available_samples_no=child.find(f"{XLM_PREFIX}availableSamplesNo").text,
                    material_type_id=mat_type_dict[child.find(f"{XLM_PREFIX}materialType").text],
                    diagnosis=child.find(f"{XLM_PREFIX}diagnosis").text if child.find(f"{XLM_PREFIX}diagnosis") is not None else "",
                    ptnm=child.find(f"{XLM_PREFIX}pTNM").text if child.find(f"{XLM_PREFIX}pTNM") is not None else "",
                    morphology=child.find(f"{XLM_PREFIX}morphology").text if child.find(f"{XLM_PREFIX}morphology") is not None else "",
                    cut_time=child.find(f"{XLM_PREFIX}cutTime").text,
                    freeze_time=child.find(f"{XLM_PREFIX}freezeTime").text,
                    retrieved=retrieval_type_dict[child.find(f"{XLM_PREFIX}retrieved").text]
                ))
            if "genome" in child.tag:
                sample_data.append(Genome(
                    sample_id=child.get("sampleId"),
                    patient_id=rt.get("id"),
                    biopsy_id=child.get("biopsy"),
                    predictive_id=child.get("predictive_number"),
                    samples_no=child.find(f"{XLM_PREFIX}samplesNo").text,
                    available_samples_no=child.find(f"{XLM_PREFIX}availableSamplesNo").text,
                    material_type_id=mat_type_dict[child.find(f"{XLM_PREFIX}materialType").text],
                    retrieved=retrieval_type_dict[child.find(f"{XLM_PREFIX}retrieved").text],
                    taking_date=child.find(f"{XLM_PREFIX}takingDate").text
                ))
            if "serum" in child.tag:
                sample_data.append(Serum(
                    sample_id=child.get("sampleId"),
                    patient_id=rt.get("id"),
                    biopsy_id=child.get("biopsy"),
                    predictive_id=child.get("predictive_number"),
                    samples_no=child.find(f"{XLM_PREFIX}samplesNo").text,
                    available_samples_no=child.find(f"{XLM_PREFIX}availableSamplesNo").text,
                    material_type_id=mat_type_dict[child.find(f"{XLM_PREFIX}materialType").text],
                    diagnosis=child.find(f"{XLM_PREFIX}diagnosis").text if child.find(f"{XLM_PREFIX}diagnosis") is not None else "",
                    taking_date=child.find(f"{XLM_PREFIX}takingDate").text
                ))
            if "cell" in child.tag:
                sample_data.append(Cell(
                    sample_id=child.get("sampleId"),
                    patient_id=rt.get("id"),
                    biopsy_id=child.get("biopsy"),
                    predictive_id=child.get("predictive_number"),
                    samples_no=child.find(f"{XLM_PREFIX}samplesNo").text,
                    available_samples_no=child.find(f"{XLM_PREFIX}availableSamplesNo").text,
                    material_type_id=mat_type_dict[child.find(f"{XLM_PREFIX}materialType").text],
                ))

    sts = rt.find(f"{XLM_PREFIX}STS")
    if sts is not None:
        for child in sts:
            if "diagnosisMaterial" in child.tag:
                sample_data.append(DiagnosisMaterial(
                    sample_id=child.get("sampleId"),
                    patient_id=rt.get("id"),
                    taking_date=child.find(f"{XLM_PREFIX}takingDate").text,
                    diagnosis=child.find(f"{XLM_PREFIX}diagnosis").text if child.find(f"{XLM_PREFIX}diagnosis") is not None else "",
                    retrieved=retrieval_type_dict[child.find(f"{XLM_PREFIX}retrieved").text],
                    material_type_id=mat_type_dict[child.find(f"{XLM_PREFIX}materialType").text]
                ))

    return sample_data


def _upload_new_data_to_db(sample_data):
    for val in sample_data:
        if isinstance(val, DiagnosisMaterial):
            found_data = db.session.execute(db.select(type(val)).filter_by(sample_id=val.sample_id)).all()
        elif isinstance(val, Patient):
            found_data = db.session.execute(db.select(type(val)).filter_by(id=val.id)).all()
        else:
            found_data = db.session.execute(db.select(type(val)).filter_by(sample_id=val.sample_id, predictive_id=val.predictive_id)).all()
        if len(found_data) < 1:
            db.session.add(val)


@cli.command("fill_db")
def fill_db():
    for file in os.listdir("/exports/"):
        try:
            tree = ET.parse(os.path.join("/exports", file))
        except ET.ParseError:
            print("Could not parse file:", file)
        specimen = _process_xml_export(tree.getroot())
        _upload_new_data_to_db(specimen)
    db.session.commit()


if __name__ == "__main__":
    cli()
