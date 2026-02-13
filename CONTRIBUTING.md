# Contribuer à PyBot

Merci pour votre intérêt pour PyBot 🎉  
Les contributions sont les bienvenues, à condition de respecter les règles ci-dessous.

L'objectif est de permettre des ajouts communautaires **sans compromettre la stabilité du bot**.

## Règle d'or

- **Une feature = un dossier**
- Le core du bot est maintenu par le staff

## Ce que vous pouvez faire

- Ajouter une **nouvelle feature** dans `features/<slug>/`
- Améliorer une features existante
- Corriger un bug dans une features
- Améliorer la documentation

## Ce que vous ne pouvez pas faire

- Modifier le core (`bot/`, `core/`)
- Modifier `enabled_features`
- Modifier la logique du loader
- Ajouter une dépendance Python sans accord du staff
- Introduire de l'I/O au chargement d'une features

Toute PR hors de ces règles sera refusée.

## La collaboration

### Structure d'une features

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
- doit correspondre exactement à `features["slug"]`

### Contrat obligatoire

Chaque `feature.py` doit exposer ces informations :

1) `features` (constante dictionnaire)

    ```python
    FEATURE = {
        "slug": "ping",
        "name": "Ping",
        "description": "Commande ping simple",
        "requires_config": False,
        "permissions": [],
        "version": "0.0"
        "author":"github"
    }
    ```

    Champs requis :

    - `slug` : identifiant unique
    - `name` : nom lisible
    - `description` : description
    - `requires_config` : booléen
    - `permissions` : liste (ex : `[]`, `["send_message"]`)
    - `version`: version en texte
    - `author`: nom lisible

2) `register(tree, config)`

    Rôle :

    - enregistrer les slash commands de la feature

    Règles strictes :

    - **aucun I/O** au chargement ou dans `register`
    - pas d'accès à l'environnement
    - pas de tâches longues
    - pas d'effet de bord à l'import

    Les opérations d'I/O sont **autorisées uniquement** dans les handlers des commandes.

### Permissions et checks

Des décorateurs globaux sont disponibles pour restreindre l'accès aux commandes.
Import : `from bot.core.checks import is_staff, is_server_admin, ...`

| Décorateur | Rôle |
|---|---|
| `@is_staff()` | Rôle staff (défini dans `.env`) |
| `@is_server_admin()` | Permission administrateur |
| `@is_server_owner()` | Propriétaire du serveur |
| `@is_server_mod()` | Modérateur (manage messages, kick, ban) |
| `@has_permissions(perm=True)` | Permission spécifique |
| `@has_any_role(id)` / `@has_all_roles(id)` | Vérification par rôle |
| `@in_channel(id)` / `@in_category(id)` | Restriction par salon/catégorie |
| `@bot_has_permissions(perm=True)` | Vérifie les permissions du bot |
| `@cooldown(rate, per)` | Limite d'utilisation |

Exemple :

```python
from bot.core.checks import is_staff

def register(tree, config):
    @tree.command(name="secret", description="Commande staff only")
    @is_staff()
    async def secret_cmd(interaction):
        await interaction.response.send_message("Staff only!", ephemeral=True)

### Commandes et conflits

- Les noms de slash commands doivent être uniques.
- Le loader refusera toute features créant un conflit de nom.
- Il est recommandé d'utiliser un **groupe de commandes par features**.

### Configuration

- Les secrets vont dans `.env` (non commités).
- La configuration fonctionnelle va dans `config.toml`.

Une features avec `requires_config = true` doit documenter :

- les clés attendues dans `[features.<slug>]`
- leurs valeurs par défaut

### Travail sur les branches

Les contributions doivent être réalisées sur **une branche dédiée** :

- ne pas travailler directement sur `main`
- utiliser la branche `dev` pour initialiser votre propre branche
- une branche = une feature ou une correction
- nommage recommandé :
    - `features/<slug>`
    - `fix-features/<slug>`

    Exemples :
    - `features/say`
    - `fix-features/ping-ephemeral`
- `fix/<slug>` est réservé aux modification du core du bot 

Les Pull Requests doivent cibler la branche `dev`.

### Créer sa branche

```bash
git checkout dev
git checkout -b features/<slug>
git add .
git commit -m "Ajout de la feature <slug>"
git push -u origin features/<slug>
```

### Règle de Pull Request

Une PR valide doit :

- concerner une seule feature
- modifier uniquement `features/<slug>` (et éventuellement la doc)
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
