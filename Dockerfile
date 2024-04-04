# Utilisez une image Python officielle comme base
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers requis dans le conteneur
COPY requirements.txt .
COPY app.py .
COPY templates templates

# Installez les dépendances Python
RUN pip install --no-cache-dir Flask google-api-python-client

# Exposez le port sur lequel l'application Flask fonctionne
EXPOSE 5000

# Commande pour exécuter l'application Flask lorsque le conteneur démarre
CMD ["python", "app.py"]