# Installation File Manager CRUD

Diese Anleitung beschreibt, wie das Projekt gestartet wird.

---

# Option 1 – Installation mit Docker 

## Voraussetzungen

- Docker
- Docker Compose

---

## 1️⃣ Repository klonen

```bash
git clone <DEIN_GITHUB_REPO_URL>
cd <DEIN_REPO_ORDNER>
```

---

## 2️⃣ Container builden und starten

```bash
docker-compose up --build
```

---

## 3️⃣ Anwendung öffnen

Frontend:
```
http://localhost:5173
```

Backend (Swagger):
```
http://localhost:8000/docs
```

---

## 4️⃣ Container stoppen

```bash
docker-compose down
```

# Option 2 – Lokale Installation (ohne Docker)

## 🔧 Backend starten

### 1️⃣ In Backend wechseln

```bash
cd BACKEND
```

### 2️⃣ Virtuelle Umgebung erstellen

**macOS / Linux**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3️⃣ Dependencies installieren

```bash
pip install -r requirements.txt
```

Oder manuell:

```bash
pip install fastapi uvicorn sqlalchemy pydantic passlib bcrypt python-jose python-multipart
```

### 4️⃣ Environment-Datei erstellen

Erstelle:

```
BACKEND/.env
```

Mit folgendem Inhalt:

```
SECRET_KEY=replace_with_your_secure_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=2
DATABASE_URL=sqlite:///./your_database_name.db
```

### 5️⃣ Backend starten

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend läuft unter:

```
http://localhost:8000/docs
```

---

## Frontend starten

### 1️⃣ In Frontend wechseln

```bash
cd FRONTEND
```

### 2️⃣ Dependencies installieren

```bash
npm install
```

### 3️⃣ Environment Datei erstellen

Datei erstellen:

`FRONTEND/.env`

Inhalt:

```
VITE_API_URL=http://localhost:8000
DATABASE_URL=sqlite:///./files.db
```

### 4️⃣ Frontend starten

```bash
npm run dev
```

Frontend läuft unter:

```
http://localhost:5173
```

---