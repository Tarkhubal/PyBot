# PyBot

Bot discord modulaire, écrit en Python, basé exclusivmeent sur les **slash commands**.
Le bot est mono-serveur et extensible via son système de *features* validées par le staff.

L'objectif du projet est de permettre à la communauté de proposer des fonctionnalités et de les coder via des **Pull Request**, sans compromettre la stabilité du bot.

## Fonctionnement général

- Le core du bot est maintenu par le staff (Aucune modification de ce core ne sera acceptée hors membre du staff)

- Les fonctionnalités sont isolées dans un système de **features**

- Une feature n'est chargée que si elle est explicitement activée dans la configuration

- L'instance du bot ne tourne que sur le serveur PyPro

## Créer votre propre feature

### Prérequis
- Python: 3.13+
- Un bot discord crééé via le *Discord Developer Portal*
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

Lancer le bot:
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

Chaque feature est autonome et vit dans son propre dossier

```markdown
features/<slug>/
    __init__.py
    feature.py
```

### Contrat obligatoire

Chaque `feature.py` doit exposer ces informations:

1) `FEATURE` (Constante dictionnaire)
    ```Python
    FEATURE = {
        "slug": "ping",
        "name": "Ping",
        "description": "Simple ping command",
        "requires_config": False,
        "permissions": [],
    }
    ```

    Contraintes:
        - `slug` doit correspondre **exactement** au nom du dossier
        - Le slug est unique dans le projet

2) `register(tree, config)`
    
    ```Python
    def register(tree, config)
    ```
    
    Rôles:
        - Enregistrer les slash commands de la feature
    
    Règles strictes :
        - Pas d’I/O (pas de fichiers, pas de réseau)

        - Pas d’accès à l’environnement

pas de boucles ou tâches longues

pas d’effets de bord à l’import

Le paramètre config correspond au bloc [features.<slug>] du fichier TOML.