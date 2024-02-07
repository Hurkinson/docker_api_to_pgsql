CREATE TABLE IF NOT EXISTS communes (
    id SERIAL PRIMARY KEY,
    code_postal VARCHAR(255),
    nom_commune_complet VARCHAR(255),
    departement VARCHAR(255),
    code_geoloc VARCHAR(255)
);