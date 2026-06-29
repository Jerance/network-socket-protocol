# Documentation du Protocole Réseau

Ce document décrit le protocole réseau crée et utilisé entre le client et le serveur à l'aide de sockets. Le protocole comprend des requêtes et des réponses pour gérer les utilisateurs, les jeux, les messages, etc.

## Structure du Protocole

Le protocole est basé sur des messages textuels. Chaque message commence par un type qui indique le type de la requête ou de la réponse. Les différents types incluent USER, GAME, MESSAGE suivi d'un attribut / action avec un potentiel contenu.

```bash
    <TYPE> <attribut> <content?>
```

## Requêtes

### Requêtes Utilisateur

Liste des attributs :

- **create**
- **delete**
- **list**
- **quit**

#### Créer un Utilisateur

- **Format de la Requête**: `USER create <pseudo>`
- **Exemple**: `USER create John`
- **Format de la Réponse**: `USER create <status_ok>`
- **Exemple de Réponse**: `USER create True`

#### Déconnecter un utilisateur à la room

- **Format de la Requête**: `USER create <pseudo>`
- **Exemple**: `USER create John`
- **Format de la Réponse**: `USER create <status_ok>`
- **Exemple de Réponse**: `USER create True`

#### Supprimer tous les utilisateur connecté au serveur

- **Format de la Requête**: `USER create <pseudo>`
- **Exemple**: `USER create John`
- **Format de la Réponse**: `USER create <status_ok>`
- **Exemple de Réponse**: `USER create True`

### Requêtes de Jeu

#### Liste des Jeux

- **Format de la Requête**: `GAME list`
- **Exemple**: `GAME list`
- **Format de la Réponse**: `GAME list <jeux_json>`
- **Exemple de Réponse**: `GAME list [{"id": 1, "name": "jeu 1", "map": {"name": "carte1"}, "players": [{"address": ["yo", 19], "name": "Titi"}, ...]}]`

## Réponses

### Réponse d'Erreur

- **Format**: `ERROR <message_erreur>`
- **Exemple**: `ERROR Erreur de Format de Requête: Attribut manquant`

### Réponse Utilisateur

#### Réponse de Création d'Utilisateur

- **Format**: `USER create <status_ok>`
- **Exemple**: `USER create True`

### Réponse de Jeu

#### Réponse de Liste des Jeux

- **Format**: `GAME list <jeux_json>`
- **Exemple**: `GAME list [{"id": 1, "name": "jeu 1", "map": {"name": "carte1"}, "players": [{"address": ["yo", 19], "name": "Titi"}, ...]}]`

## Exemples

### Requête Client

### Server Response

```python
    response = parse_response("USER create True")
```

## Gestion des Status Code

|     Status     | Code | Message                              |
| :------------: | :--: | :----------------------------------- |
|       OK       |  0   | Requête réalisée comme prévu         |
| UNKNOW COMMAND |  1   | TYPE ❌ ou TYPE ✅, ACTION ❌        |
|   BAD VALUE    |  2   | TYPE ✅ , ACTION ✅, CONTENT❌       |
|     SORRY      |  69  | Tout ✅, mais logique serveur refuse |

Fonctions Principales

- connect_to_server(host: str, port: int, on_message: Callable) -> socket.socket: Établit la connexion avec le serveur et démarre un thread pour la lecture asynchrone des messages.

- send_request(client_socket: socket.socket, request: Request) -> None: Envoie une requête au serveur.

- socket_read(client_socket, on_response: Callable) -> None: Lit de manière asynchrone les messages du serveur et appelle la fonction de gestion des réponses.
