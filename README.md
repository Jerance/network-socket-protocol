# Network Socket Protocol

Ce projet est une application Python de type client/serveur basée sur des sockets TCP. Il permet à plusieurs utilisateurs de se connecter à un serveur, de choisir un pseudo, de créer ou rejoindre des rooms, et d’échanger des messages via un protocole textuel personnalisé.

## Présentation

L’application est structurée autour d’un serveur central qui gère :

- les connexions clientes,
- l’enregistrement des utilisateurs,
- la création et la gestion de rooms de jeu,
- la diffusion de messages entre clients.

Elle inclut également une interface graphique côté client et une interface d’administration côté serveur.

## Fonctionnalités

- Connexion d’un client au serveur via TCP
- Création d’un pseudo utilisateur
- Liste et création de rooms
- Rejointure de rooms existantes
- Envoi de messages diffusés à tous les utilisateurs
- Interface d’administration pour visualiser les utilisateurs et les rooms

## Structure du projet

- client/ : interface utilisateur du client et logique de connexion
- server/ : serveur, logique métier et interface d’administration
- protocol/ : définition du protocole réseau et sérialisation/désérialisation des messages
- commons/ : modèles de données partagés et utilitaires

## Protocole réseau

Le protocole repose sur des messages textuels simples. Les messages sont structurés selon le format suivant :

```text
<TYPE> <action> <contenu?>
```

Exemples :

```text
USER create John
GAME list
MESSAGE all Bonjour
```

La documentation détaillée du protocole est disponible dans [protocol.md](protocol.md).

## Prérequis

- Python 3.10+
- Bibliothèques Python suivantes :
  - flet
  - dataclasses_json

Vous pouvez les installer avec :

```bash
pip install flet dataclasses_json
```

## Lancer le projet

Depuis la racine du projet :

### 1. Démarrer le serveur

```bash
python server/admin_server_ui.py
```

### 2. Lancer l’interface client

```bash
python client/client_ui.py
```

## Architecture technique

- Le serveur écoute sur le port 2020.
- Les communications sont gérées via des sockets TCP.
- Les messages envoyés entre client et serveur sont sérialisés dans un format texte spécifique.
- Les modèles de données sont définis dans [commons/models.py](commons/models.py).

## Notes

Ce projet est avant tout un exercice de réseau et de protocole de communication. Il montre comment implémenter un échange client/serveur simple en Python, sans framework réseau externe.
