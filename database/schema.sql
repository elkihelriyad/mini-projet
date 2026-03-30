DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS specialties;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS users;

CREATE TABLE specialties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    career_paths TEXT,
    subjects TEXT,
    additional_info TEXT
);

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texte TEXT NOT NULL,
    texte_en TEXT,
    texte_ar TEXT,
    dimensions TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    access_code TEXT NOT NULL,
    nom_complet TEXT,
    role TEXT,
    is_active INTEGER DEFAULT 1,
    last_result_json TEXT,
    profile_type TEXT,
    date_test DATETIME
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date_test DATETIME,
    result_json TEXT,
    profile_type TEXT,
    duration INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
