# PyBot

![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Discord](https://img.shields.io/badge/discord-slash%20commands-5865F2.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Code Owners](https://img.shields.io/badge/code%20owners-enforced-orange.svg)

Bot Discord modulaire, écrit en Python, basé exclusivement sur les **slash commands**.  
Le bot est mono-serveur et extensible via son système de *features* validées par le staff.

L'objectif du projet est de permettre à la communauté de proposer des fonctionnalités et de les coder via des **Pull Request**, sans compromettre la stabilité du bot.

## Fonctionnement général

- Le core du bot est maintenu par le staff (Aucune modification de ce core ne sera acceptée hors membre du staff)
- Les fonctionnalités sont isolées dans un système de **features**
- Une feature n'est chargée que si elle est explicitement activée dans la configuration
- L'instance du bot ne tourne que sur le serveur PyPro

## Créer votre propre feature

### Prérequis

- Python : 3.13+
- Un bot Discord créé via le *Discord Developer Portal*
- Le scope OAuth2 `application.commands` activé

### Installation (local)

```cmd
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

Créer un fichier .env (exemple dans config/.env.example)

```env
DISCORD_TOKEN=your_discord_token_here
GUILD_ID=your_guild_id_here
CONFIG_PATH=./config/config.toml
LOG_LEVEL=info
STAFF_ROLES_IDS=
```

Lancer le bot :

```cmd
python -m bot.core.app
```

## Structure du projet

```markdown
bot/
  core/
    app.py        # point d’entrée
    config.py     # chargement et validation de la config
    loader.py     # chargement des features
features/
  ping/
    feature.py
  say/
    feature.py
config/
  config.toml
  .env
```

## Système de features

Chaque feature est autonome et vit dans son propre dossier.

```markdown
features/<slug>/
  __init__.py
  feature.py
```

### Contrat obligatoire

Chaque `feature.py` doit exposer ces informations :

1) `FEATURE` (constante dictionnaire)

  ```Python
  FEATURE = {
    "slug": "ping",
    "name": "Ping",
    "description": "Simple ping command",
    "requires_config": False,
    "permissions": [],
  }
  ```

  Contraintes :
  - `slug` doit correspondre **exactement** au nom du dossier
  - Le slug est unique dans le projet

2) `register(tree, config)`

  ```Python
  def register(tree, config)
  ```

  Rôles :
  - Enregistrer les slash commands de la feature

  Règles strictes :
  - Pas d’I/O (pas de fichiers, pas de réseau) dans register, à faire dans la fonction de la commande
  - Pas d’accès à l’environnement
  - Pas de boucles ou tâches longues
  - Pas d’effets de bord à l’import

  Le paramètre `config` correspond au bloc `[features.<slug>]` du fichier TOML.

## Organisation interne des features

Chaque feature est libre d'organiser son dossier interne comme elle le souhaite.  
En dehors des fichiers obligatoires (`feature.py`, `__init__.py`), une feature peut contenir :

- Des modules Python internes
- Des sous-dossiers
- Des fichiers de données (JSON, SQL, etc.)

```markdown
features/example/
  feature.py
  __init__.py
  service.py
  repository.py
  data/
    defaults.json
```

Contraintes :
- Le point d'entrée reste **toujours** `feature.py`
- Aucun fichier externe à `feature.py` ne doit être importé par le core
- L'I/O reste interdit au chargement (`import/register`), mais autorisé à l'exécution des commandes

## Configuration

- Les secrets vont dans .env (jamais commités)
- Le comportement va dans `config.toml`

Activation des features :

```toml
enabled_features = ["ping", "say"]
```

Configuration par feature :

```toml
[features.say]
ephemeral_default = false
```

Si `requires_config = true` et que la section est absente, la feature est refusée au chargement.

## Sécurité et stabilité

- Les conflits de noms de slash commands sont détectés automatiquement
- Une feature en erreur ne bloquera pas le bot
- Le core est protégé via CODEOWNERS et règles de branche

## Contribuer

Les contributions se font exclusivement via **Pull Request**.

Règle de base :
- Une PR = une feature
- Ne pas modifier le core
- Ne pas modifier `enabled_features` (lors de la PR, amusez-vous en local)
- Ne pas ajouter de dépendance sans validation
- Inclure un test manuel simple

Voir `CONTRIBUTING.md` pour plus de détails.

## Licence

Ce projet est distribué sous licence [MIT](LICENSE).

