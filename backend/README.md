# BACKEND

# Backend – FastAPI File Manager API

## Projektstruktur

BACKEND/
 ├── app/
 │   ├── main.py
 │   ├── database.py
 │   ├── authentification/
 │   │     └── auth.py
 │   ├── endpoints/
 │   │     ├── users.py
 │   │     └── files.py
 │   ├── models/
 │   │     ├── user.py
 │   │     └── file.py
 ├── uploads/
 ├── files.db
 ├── requirements.txt
 └── .env

---

## Authentifizierung

JWT Authentifizierung.

Login gibt Token zurück.
Token wird übermittelt via:

Authorization: Bearer <token>

Geschützte Endpunkte:
- /files (alle CRUD Operationen)

---

## Endpunkte

### Auth
POST /auth/register  
POST /auth/login  

### Files
GET /files  
POST /files  
PUT /files/{id}  
DELETE /files/{id}  

---