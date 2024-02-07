import pandas as pd
import requests
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from database import engine
import models

app = FastAPI()

# ----- Methodes -------------------------------------------------------------

def get_db():
    """
    Intialise une connection avec la base de donnée
    """

    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

def get_geoloc(nom_commune):
    """
    Utilise l'API Openstreetmap pour obtenir le geo code d'une commune.
    """

    url = f"https://nominatim.openstreetmap.org/search?city={nom_commune}&format=json&limit=1"
    response = requests.get(url)
    data = response.json()

    if data:
        code_geoloc = f"{data[0]['lat']}, {data[0]['lon']}"
        return code_geoloc
    
    else:
        return None
    
def update_missing_geolocs():
    """
    Cherche les entrées dans la bdd dont le 'code_geoloc' est manquant.
    """

    db = next(get_db())
    try:
        communes = db.query(models.Commune).filter(models.Commune.code_geoloc == None).all()

        for commune in communes:
            code_geoloc = get_geoloc(commune.nom_commune_complet.lower())
            if code_geoloc:
                commune.code_geoloc = code_geoloc

        db.commit()

    finally:
        db.close()


# ----- startup -----------------------------------------------------------------

@app.on_event("startup")
async def startup_event():

    print("Application startup") 

    models.Base.metadata.create_all(bind=engine)

    ## Téléchargement --------------------------------
    csv_url = "https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"
    df = pd.read_csv(csv_url)

    ## opérations de traitement ----------------------
    df = df[['code_postal', 'nom_commune_complet']]

    df['code_postal'] = df['code_postal'].astype(str).apply(lambda x:'0' + x if len(x) == 4 and not x.startswith('97') else x)
    df['nom_commune_complet'] = df['nom_commune_complet'].str.upper()
    df['departement'] = df['code_postal'].str[:2]
    df['code_geoloc'] = None

    ## Insertion dans la base de données -------------
    db = next(get_db())
    for _, row in df.iterrows():

        ## Vérification ------------------------------
        existant = db.query(models.Commune).filter_by(code_postal= row['code_postal'], nom_commune_complet= row['nom_commune_complet']).first()

        if not existant:

            commune = models.Commune(
                code_postal = row['code_postal'],
                nom_commune_complet = row['nom_commune_complet'],
                departement = row['departement'],
                code_geoloc = None
            )
            db.add(commune)

    # update_missing_geolocs()  # ne fonctionne pas ou alors est très long, solution en cours

    db.commit()

# ----- Routes -------------------------------------------------------------

@app.get("/")
def read_root():
    return {
        "title": "my_FASTAPI",
        "description": "Une API pour gérer l'import de données sur les communes de france dans une base de données POSGRESQL",
        "version": "1.0.0",
        "contact": {
            "name": "Vivien Schneider",
            "email": "schneidervvn@gmail.com",
        },
        "endpoints": {
            "GET /commune/{nom_commune}": "Obtenir les informations d'une commune par son nom",
            "GET /communes/departement/{departement}": "Obtenir toutes les communes d'un département",
            "POST /communes/": "Ajouter ou mettre à jour une commune",
        },
    }

@app.get("/communes/{nom_commune}")
def get_commune_info(nom_commune: str, db: Session = Depends(get_db)):
    """
    Récupère les infos d'une commune.
    """

    info = db.query(models.Commune).filter(models.Commune.nom_commune_complet == nom_commune).first()

    if info is None:
        raise HTTPException(status_code=404, detail="Commune not found")

    return info

@app.get("/communes/departement/{departement}")
def get_communes_by_departement(departement: str, db: Session = Depends(get_db)):
    """
    Récupère toutes les communes d'un département.
    """

    communes = db.query(models.Commune).filter(models.Commune.departement == departement).all()

    return communes

@app.post("/communes/")
def add_or_update_commune(commune_update: models.CommuneCreate, db: Session = Depends(get_db)):
    """
    Ajoute ou met à jour une commune dans la BDD.
    """

    existing_commune = db.query(models.Commune).filter(
        models.Commune.code_postal == commune_update.code_postal,
        models.Commune.nom_commune_complet == commune_update.nom_commune_complet
    ).first()

    if existing_commune:
        existing_commune.departement = commune_update.departement,
        existing_commune.code_postal = commune_update.code_postal,
        existing_commune.code_geoloc = commune_update.code_geoloc

    else:
        new_commune = models.Commune(
            code_postal = commune_update.code_postal,
            nom_commune_complet = commune_update.nom_commune_complet,
            departement = commune_update.departement,
            code_geoloc = commune_update.code_geoloc
        )
        db.add(new_commune)

    db.commit()

    return {"message": f"{new_commune.nom_commune_complet} ajoutée ou mise à jour avec succès"}


# =================================================================================================