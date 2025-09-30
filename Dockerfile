# ========================
# Étape 1 : Base Python
# ========================
FROM python:3.11-slim

# Empêcher Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système utiles
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ========================
# Étape 2 : Dépendances
# ========================
# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ========================
# Étape 3 : Code source
# ========================
# Copier tout le projet
COPY . .

# ========================
# Étape 4 : Exposition du port
# ========================
# Port configurable (par défaut 8000)
ENV PORT=8000
EXPOSE ${PORT}

# ========================
# Étape 5 : Lancer l'application
# ========================
# Démarrer FastAPI avec Uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
