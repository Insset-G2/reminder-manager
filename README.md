# API de Rappels

Cette API permet aux utilisateurs de gérer des rappels. Les principales fonctionnalités incluent la création, la mise à jour, la récupération et la suppression de rappels. Elle offre également la possibilité de récupérer les rappels actuels dus dans la prochaine minute et envoie des notifications par email lors de la création d'un rappel.

## Table des Matières

- [Installation](#installation)
- [Points de terminaison](#points-de-terminaison)
  - [Obtenir les rappels actuels](#obtenir-les-rappels-actuels)
  - [Lister tous les rappels](#lister-tous-les-rappels)
  - [Créer un rappel](#créer-un-rappel)
  - [Mettre à jour un rappel](#mettre-à-jour-un-rappel)
  - [Supprimer un rappel](#supprimer-un-rappel)
  - [Récupérer un rappel par ID](#récupérer-un-rappel-par-id)
- [Fonctionnalité d'envoi d'email](#fonctionnalité-denvoi-demail)

## Installation

1. Clonez le dépôt.
2. Installez les dépendances nécessaires :
    ```bash
    pip install -r requirements.txt
    ```
3. Lancez l'application :
    ```bash
    python app.py
    ```

## Points de terminaison

### Obtenir les rappels actuels

Récupère les rappels qui sont dus dans la prochaine minute.

### Lister tous les rappels

Récupère tous les rappels enregistrés.

### Créer un rappel

Permet de créer un nouveau rappel en fournissant les informations nécessaires telles que l'ID utilisateur, le titre, la description, l'heure de déclenchement et l'email.

### Mettre à jour un rappel

Permet de mettre à jour un rappel existant en fournissant les nouvelles informations telles que le titre, la description, l'heure de déclenchement et l'email.

### Supprimer un rappel

Permet de supprimer un rappel existant en fournissant son ID.

### Récupérer un rappel par ID

Permet de récupérer un rappel spécifique en fournissant son ID.

## Fonctionnalité d'envoi d'email

Lorsqu'un rappel est créé, une notification par email est envoyée à l'adresse fournie dans le rappel. L'email contient le titre du rappel et une confirmation de création. La création du rappel fonctionne avec l'API de [Noah Gallo](https://github.com/NoahGallo).

