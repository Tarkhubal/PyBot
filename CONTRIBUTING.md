# Contribuer à PyBot

Merci pour votre intérêt pour PyBot 🎉  
Les contributions sont les bienvenues, à condition de respecter les règles ci-dessous.

L'objectif est de permettre des ajouts communautaires **sans compromettre la stabilité du bot**.

## Règle d'or

- **Une feature = un dossier**
- Le core du bot est maintenu par le staff

## Ce que vous pouvez faire

- Ajouter une **nouvelle feature** dans `feature/<slug>/`
- Améliorer une feature existante
- Corriger un bug dans une feature
- Améliorer la documentation

## Ce que vous ne pouvez pas faire

- Modifier le core (`bot/`, `core/`)
- Modifier `enabled_features`
- Modifier la logique du loader
- Ajouter une dépendance Python
- Introduire de l'I/O au chargement d'une feature

Toute PR hors de ces règles sera refusée.

## La collaboration

### Structure d'une feature

Une feature doit respecter **strictement** la structure suivante :

```markdown
features/<slug>/
    __init__.py
    feature.py
```

Le `slug` :

- doit être unique
- en minuscule
- sans espace
- doit correspondre exactement à `FEATURE["slug"]`

### Contrat obligatoire

Chaque `feature.py` doit exposer ces informations :

1) `FEATURE` (constante dictionnaire)

    ```python
    FEATURE = {
        "slug": "ping",
        "name": "Ping",
        "description": "Commande ping simple",
        "requires_config": False,
        "permissions": [],
    }
    ```

    Champs requis :

    - `slug` : identifiant unique
    - `name` : nom lisible
    - `description` : description
    - `requires_config` : booléen
    - `permissions` : liste (ex : `[]`, `["send_message"]`)

2) `register(tree, config)`

    Rôle :

    - enregistrer les slash commands de la feature

    Règles strictes :

    - **aucun I/O** au chargement ou dans `register`
    - pas d'accès à l'environnement
    - pas de tâches longues
    - pas d'effet de bord à l'import

    Les opérations d'I/O sont **autorisées uniquement** dans les handlers des commandes.

### Commandes et conflits

- Les noms de slash commands doivent être uniques.
- Le loader refusera toute feature créant un conflit de nom.
- Il est recommandé d'utiliser un **groupe de commandes par feature**.

### Configuration

- Les secrets vont dans `.env` (non commités).
- La configuration fonctionnelle va dans `config.toml`.

Une feature avec `requires_config = true` doit documenter :

- les clés attendues dans `[features.<slug>]`
- leurs valeurs par défaut

### Travail sur les branches

Les contributions doivent être réalisées sur **une branche dédiée** :

- ne pas travailler directement sur `main`
- une branche = une feature ou une correction
- nommage recommandé :
    - `feature/<slug>`
    - `fix/<slug>`

    Exemples :
    - `feature/say`
    - `fix/ping-ephemeral`

Les Pull Requests doivent cibler la branche `main`.

### Créer sa branche

```bash
git checkout -b feature/<slug>
git add .
git commit -m "Ajout de la feature <slug>"
git push -u origin feature/<slug>
```

### Règle de Pull Request

Une PR valide doit :

- concerner une seule feature
- modifier uniquement `feature/<slug>` (et éventuellement la doc)
- ne pas modifier le core
- ne pas modifier `enabled_features`
- inclure un test manuel simple (2-3 étapes)

### Review et validation

- Toutes les PR passent par review
- Le staff se réserve le droit de refuser une PR :
    - trop complexe
    - mal isolée
    - difficile à maintenir
    - non alignée avec la philosophie du projet

### En cas de doute

- Regardez les features existantes (`ping`, `say`)
- Ouvrez une issue avant de coder
- Posez la question sur le serveur Discord

## Conclusion

Le but n’est pas de freiner les contributions, mais de garder un bot :

- lisible
- stable
- maintenable sur le long terme

Merci de contribuer proprement 🙏
