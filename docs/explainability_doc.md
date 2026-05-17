# Documentation — Explicabilité des Modèles : Crédit Consommation & Détection de Fraude

## Vue d'ensemble

Ce document décrit les méthodes, outils et obligations liés à l'explicabilité des modèles de machine learning utilisés dans le cadre du crédit consommation et de la détection de fraude pour les particuliers. Il couvre les techniques d'interprétabilité (SHAP, LIME, feature importance), les obligations réglementaires (RGPD article 22, SR 11-7), les processus d'explication aux clients et les bonnes pratiques de gouvernance des modèles.

**Domaine :** Explicabilité des modèles IA — crédit consommation et fraude
**Périmètre :** Modèles de scoring crédit (PD), modèles de détection de fraude, modèles de LGD
**Mots-clés :** explainability, interpretability, SHAP, LIME, feature importance, XAI, droit à l'explication, model governance, biais algorithmique, RGPD article 22, SR 11-7

---

## 1. Concepts Fondamentaux de l'Explicabilité

### 1.1 Pourquoi l'Explicabilité est Indispensable

L'explicabilité des modèles ML répond à trois besoins distincts et complémentaires dans le contexte du crédit et de la fraude :

**Besoin réglementaire :**
- Le RGPD (article 22) interdit les décisions entièrement automatisées sans possibilité d'explication
- La réglementation bancaire (SR 11-7 aux USA, lignes directrices BCE en Europe) impose la validation et la transparence des modèles
- Tout refus de crédit basé sur un modèle automatique doit pouvoir être justifié au client

**Besoin métier :**
- Les équipes de risque doivent comprendre pourquoi un modèle prend une décision pour le valider et le contrôler
- Les analystes crédit en revue manuelle ont besoin des facteurs explicatifs pour décider
- Les équipes de conformité doivent s'assurer de l'absence de discrimination algorithmique

**Besoin opérationnel :**
- Détecter les biais et dérives du modèle (data drift, concept drift)
- Debugger les erreurs du modèle (faux positifs, faux négatifs inexpliqués)
- Améliorer le modèle en comprenant quelles variables contribuent le plus

### 1.2 Explicabilité Globale vs Locale

**Explicabilité Globale :**
Décrit le comportement général du modèle sur l'ensemble des données. Répond à la question : "Quelles variables sont les plus importantes dans les décisions du modèle en général ?"

- Utile pour : validation du modèle, détection de biais, reporting réglementaire
- Exemples : feature importance globale, courbes de dépendance partielle (PDP)

**Explicabilité Locale :**
Décrit pourquoi le modèle a pris une décision spécifique pour un individu donné. Répond à la question : "Pourquoi ce client précis a-t-il été refusé ?"

- Utile pour : explication au client, revue manuelle, contestation de décision
- Exemples : SHAP values individuelles, LIME, counterfactual explanations

### 1.3 Modèles Interprétables vs Modèles Boîtes Noires

**Modèles intrinsèquement interprétables :**
Ces modèles sont transparents par conception — leur logique de décision est directement lisible.

| Modèle | Niveau d'interprétabilité | Usage typique |
|---|---|---|
| Régression logistique | Très élevé | Scoring crédit standard (scorecard) |
| Arbre de décision (profondeur ≤ 5) | Élevé | Règles métier, audit |
| Scorecard (WoE + régression) | Très élevé | Standard industrie bancaire |
| Régression linéaire | Très élevé | Estimation LGD simple |

**Modèles boîtes noires (nécessitent des outils XAI) :**

| Modèle | Performance | Complexité d'explication |
|---|---|---|
| XGBoost / LightGBM | Très élevée | Moyenne (SHAP disponible) |
| Random Forest | Élevée | Moyenne (SHAP disponible) |
| Réseau de neurones (MLP) | Élevée | Élevée |
| Deep Learning (LSTM, Transformer) | Très élevée | Très élevée |

**Arbitrage performance / interprétabilité :**
Dans le secteur bancaire régulé, il est souvent préférable d'utiliser un modèle légèrement moins performant mais plus interprétable (régression logistique + features engineerées) plutôt qu'un modèle opaque plus performant. La réglementation SR 11-7 impose de documenter et justifier ce choix.

---

## 2. Méthodes d'Explicabilité

### 2.1 SHAP (SHapley Additive exPlanations)

SHAP est la méthode d'explicabilité la plus utilisée dans le secteur bancaire. Elle est basée sur la théorie des jeux (valeurs de Shapley) et garantit des propriétés mathématiques solides.

**Principe de fonctionnement :**
SHAP mesure la contribution marginale de chaque variable à la prédiction, en moyennant toutes les combinaisons possibles de variables. Pour chaque prédiction individuelle :

```
Prédiction = Valeur de base (moyenne du modèle) + Σ SHAP values de chaque variable
```

**Propriétés garanties par SHAP :**
- **Efficacité** : la somme des SHAP values = prédiction - valeur de base
- **Symétrie** : deux variables identiques reçoivent la même contribution
- **Absence de fantôme** : une variable sans impact reçoit une SHAP value de 0
- **Additivité** : contributions combinables de façon linéaire

**Types de SHAP selon le modèle :**
- **TreeSHAP** : optimisé pour XGBoost, LightGBM, Random Forest (< 1 ms par prédiction)
- **KernelSHAP** : modèle-agnostique, plus lent (utilisé pour réseaux de neurones)
- **LinearSHAP** : pour les modèles linéaires (régression logistique)

**Interprétation des SHAP values :**
- SHAP value positive → la variable augmente la probabilité de défaut / fraude
- SHAP value négative → la variable diminue la probabilité de défaut / fraude
- |SHAP value| → magnitude de l'impact (plus la valeur absolue est grande, plus l'impact est fort)

**Exemple concret (crédit consommation) :**
```
PD de base (moyenne portefeuille) : 4.2%
+ DTI élevé (38%)          : +2.1%  (SHAP = +0.021)
+ Incident FICP récent     : +1.8%  (SHAP = +0.018)
- Ancienneté emploi (8 ans): -0.9%  (SHAP = -0.009)
- CDI                      : -0.6%  (SHAP = -0.006)
+ Crédit revolving saturé  : +0.8%  (SHAP = +0.008)
= PD finale prédite        : 7.4%
```

### 2.2 LIME (Local Interpretable Model-agnostic Explanations)

LIME est une méthode d'explicabilité locale qui entraîne un modèle simple (linéaire) autour d'une prédiction spécifique pour approximer le comportement du modèle complexe localement.

**Principe de fonctionnement :**
1. Génération de N échantillons perturbés autour de l'observation à expliquer
2. Calcul des prédictions du modèle sur ces échantillons perturbés
3. Entraînement d'un modèle linéaire local pondéré par la proximité à l'observation originale
4. Les coefficients du modèle linéaire = importance locale des variables

**Avantages de LIME :**
- Modèle-agnostique (fonctionne avec tout type de modèle)
- Facile à implémenter
- Résultats intuitifs (coefficients d'une régression linéaire)

**Limites de LIME :**
- Instabilité : deux appels sur la même observation peuvent donner des résultats différents (aléatoire dans la perturbation)
- Sensible au choix du noyau de pondération (kernel)
- Moins fiable que SHAP sur les interactions entre variables

**Quand préférer LIME à SHAP :**
- Modèles non-arborescents (réseaux de neurones, SVM) où TreeSHAP n'est pas disponible
- Prototypage rapide
- Cas où l'on veut une explication purement locale sans contrainte globale

### 2.3 Feature Importance Globale

La feature importance globale mesure la contribution moyenne de chaque variable à la performance du modèle sur l'ensemble du jeu de données.

**Méthodes de calcul :**

**Impurity-based importance (pour les modèles d'arbres) :**
- Mesure la réduction moyenne de l'impureté (Gini ou entropie) apportée par chaque variable
- Rapide à calculer
- **Biais connu** : surreprésente les variables avec beaucoup de modalités ou à haute cardinalité

**Permutation importance :**
- Mélange aléatoirement les valeurs d'une variable et mesure la dégradation des performances
- Plus robuste que l'impurity-based importance
- **Formule** : Importance(variable) = Performance(modèle original) - Performance(modèle avec variable permutée)

**SHAP importance globale :**
- Moyenne des valeurs absolues des SHAP values sur tout le dataset
- La plus fiable car hérite des propriétés mathématiques de SHAP
- **Formule** : Importance globale(variable j) = mean(|SHAP_j(i)|) pour tout i

**Visualisations standards :**
- **Bar plot** : importance globale de chaque variable (classée par ordre décroissant)
- **Beeswarm plot** : distribution des SHAP values par variable (montre l'effet positif/négatif)
- **Dependence plot** : relation entre la valeur d'une variable et son SHAP value

### 2.4 Counterfactual Explanations (Explications Contrefactuelles)

Les explications contrefactuelles répondent à la question : "Que devrait changer ce client pour obtenir une décision différente ?"

**Principe :**
Trouver le point le plus proche dans l'espace des features qui conduirait à une décision inverse, en minimisant les changements nécessaires.

**Exemple pour un refus de crédit :**
```
Décision actuelle : REFUS (PD = 12%)

Explication contrefactuelle :
"Si votre DTI passait de 38% à 32% (réduction des charges de 150 €/mois)
ET si vous n'aviez pas eu d'incident de paiement dans les 12 derniers mois,
votre demande aurait été approuvée (PD estimée : 6.8%)."
```

**Contraintes importantes dans le contexte bancaire :**
- Les changements suggérés doivent être **actionnables** (un client ne peut pas changer son âge)
- Les changements doivent être **réalistes** dans un délai raisonnable
- Éviter de suggérer des changements qui pourraient induire une manipulation du modèle

**Algorithmes courants :** DICE (Diverse Counterfactual Explanations), ALIBI, Wachter et al.

### 2.5 Courbes de Dépendance Partielle (PDP — Partial Dependence Plots)

Les PDP montrent l'effet marginal d'une variable sur la prédiction, en moyennant l'effet de toutes les autres variables.

**Utilité dans le contexte crédit / fraude :**
- Visualiser la relation entre le DTI et la PD → vérifier que la relation est bien monotone et cohérente avec la théorie
- Identifier des effets non-linéaires inattendus (ex : PD qui remonte pour les très hauts revenus → signal de sur-apprentissage)
- Détecter des biais algorithmiques (ex : relation entre l'âge et le score qui ne devrait pas exister)

**Limite des PDP :** supposent l'indépendance des variables, ce qui est rarement vrai en pratique. Les ICE plots (Individual Conditional Expectation) sont une alternative qui montre les effets individuels.

---

## 3. Explicabilité Appliquée au Modèle de Crédit

### 3.1 Explication d'un Refus de Crédit au Client

Le RGPD (article 22) et la réglementation française imposent de fournir une explication compréhensible à tout client refusé suite à une décision automatisée.

**Structure d'une explication client (format réglementaire) :**

1. **Décision** : refus de la demande de crédit
2. **Motifs principaux** (3 à 5 maximum, par ordre d'importance décroissante)
3. **Informations sur le droit de recours** : possibilité de demander une révision humaine

**Traduction des SHAP values en langage client :**

| SHAP value (interne) | Motif client (externe) |
|---|---|
| DTI SHAP = +0.021 (élevé) | "Votre taux d'endettement actuel est trop élevé au regard de vos revenus" |
| FICP SHAP = +0.018 | "Un incident de remboursement récent a été détecté dans votre historique" |
| Ancienneté emploi SHAP = +0.012 | "Votre situation professionnelle actuelle présente une instabilité" |
| Revolving saturé SHAP = +0.009 | "Vos crédits existants sont utilisés à un niveau élevé" |

**Règles de communication au client :**
- Utiliser un langage simple, sans jargon technique
- Mentionner les 3 à 5 facteurs les plus impactants seulement (pas toutes les variables)
- Ne jamais mentionner le nom du modèle ni les valeurs numériques exactes du score
- Toujours inclure les informations sur le droit à la révision humaine
- Archiver l'explication fournie (obligation RGPD, durée minimale 5 ans)

### 3.2 Explication pour les Analystes Crédit (Revue Manuelle)

Les analystes crédit en charge de la revue manuelle ont besoin d'une explication plus détaillée que les clients.

**Format d'explication pour l'analyste :**
- Score global et PD associée
- Top 10 des variables par importance SHAP (positives et négatives)
- Comparaison avec le profil moyen du portefeuille (benchmark)
- Signaux d'alerte spécifiques déclenchés
- Historique du client (si existant)

**Dashboard analyste — éléments clés :**
```
Score : 480 / 1000 | PD : 8.3% | Zone : Orange (revue manuelle)

Facteurs aggravants :              Facteurs atténuants :
+ DTI : 33% (+2.1%)               - Ancienneté CDI : 6 ans (-0.9%)
+ Incident DPD30 il y a 8 mois    - Pas de FICP (-0.6%)
  (+1.8%)                         - Bon comportement bancaire (-0.4%)
+ Revolving utilisé à 88% (+0.8%)

Profil moyen zone orange :
DTI moyen : 30% | PD moyenne : 6.1%
Ce client : DTI = 33% | PD = 8.3% → légèrement au-dessus de la moyenne
```

### 3.3 Surveillance de la Stabilité et de la Cohérence du Modèle

L'explicabilité globale permet de surveiller que le modèle reste cohérent dans le temps.

**Vérifications de cohérence métier :**
- Le DTI doit être une variable positivement corrélée à la PD → SHAP positif pour les DTI élevés
- L'ancienneté d'emploi doit être négativement corrélée à la PD → SHAP négatif
- Le revenu doit être négativement corrélé à la PD (toutes choses égales par ailleurs)
- L'inscription FICP doit être la variable la plus impactante

**Alertes de dérive (Model Drift) :**
- Si le ranking des variables importantes change significativement → investigation requise
- Si une variable normalement peu importante devient très importante → data quality issue ?
- Si la relation entre une variable et la PD s'inverse → concept drift, recalibrage nécessaire

---

## 4. Explicabilité Appliquée au Modèle de Fraude

### 4.1 Explication d'une Alerte Fraude au Fraud Analyst

Contrairement au crédit, les explications du modèle de fraude ne sont jamais communiquées directement au client suspect (risque de gaming du modèle).

**Format d'explication pour le fraud analyst :**

```
Fraud Score : 0.74 | Zone : Rouge (fraude probable)

Signaux déclencheurs principaux :
1. Email créé 3 jours avant la demande        SHAP = +0.18 (très fort)
2. IP distante de l'adresse déclarée (310 km) SHAP = +0.15 (fort)
3. Formulaire rempli en 72 secondes           SHAP = +0.12 (fort)
4. Tel activé 8 jours avant la demande        SHAP = +0.10 (modéré)
5. Montant = maximum de la gamme              SHAP = +0.08 (modéré)

Facteurs atténuants :
- Score crédit correct (680)                  SHAP = -0.05
- Aucune IP connue en liste noire             SHAP = -0.03

Pattern reconnu : profil proche de 47 cas de fraude confirmés
en base (similitude cosinus : 0.89)
```

### 4.2 Explication en Cas de Faux Positif (Client Légitime Bloqué)

Lorsqu'un client légitime conteste un blocage, l'institution doit pouvoir expliquer la décision sans révéler les mécanismes anti-fraude.

**Formulation recommandée au client :**
"Votre demande a nécessité une vérification complémentaire de sécurité. Nous avons besoin de confirmer votre identité via [méthode de vérification]. Cette étape est standard pour protéger nos clients contre toute utilisation frauduleuse de leurs données."

**Ne jamais dire au client :**
- Quelles variables ont déclenché l'alerte
- Quel seuil de score a été franchi
- Que son device fingerprint ou son IP ont été signalés

**Pour le fraud analyst (explication interne du faux positif) :**
- Analyser les SHAP values du cas
- Identifier le profil type qui génère des faux positifs (ex : jeunes primo-accédants avec néobanque)
- Créer un segment spécifique dans le modèle pour réduire le taux de faux positifs sur ce profil

### 4.3 Analyse Post-Mortem des Fraudes Non Détectées (Faux Négatifs)

Pour chaque fraude confirmée qui n'a pas été détectée par le modèle, une analyse post-mortem est nécessaire.

**Questions à répondre :**
- Quel était le fraud score au moment de la demande ?
- Quelles variables ont "protégé" ce fraudeur (SHAP très négatifs) ?
- S'agissait-il d'un nouveau type de fraude non représenté dans les données d'entraînement ?
- Comment enrichir le modèle pour détecter ce pattern à l'avenir ?

**Processus d'amélioration continue :**
1. Labellisation des fraudes confirmées dans la base d'entraînement
2. Analyse des SHAP values des faux négatifs → identification du pattern manqué
3. Feature engineering pour capturer le nouveau pattern
4. Réentraînement et validation du modèle
5. Déploiement et surveillance

---

## 5. Réglementation et Gouvernance

### 5.1 RGPD — Article 22 : Droit à l'Explication

L'article 22 du RGPD encadre les décisions basées uniquement sur un traitement automatisé.

**Obligations :**
- Informer le client de l'existence d'une prise de décision automatisée
- Lui fournir des informations utiles sur la logique sous-jacente
- Lui permettre de demander une intervention humaine pour révision
- Lui permettre d'exprimer son point de vue et de contester la décision

**Ce que le RGPD n'impose pas (contrairement aux idées reçues) :**
- Il n'impose pas de fournir une explication technique exhaustive
- Il n'interdit pas les modèles complexes (boîtes noires)
- Il n'impose pas de fournir les valeurs exactes du score

**Délai de réponse :**
- Demande d'explication : réponse dans un délai d'1 mois (extensible à 3 mois si complexe)
- Demande de révision humaine : même délai

**Documentation obligatoire :**
- Registre des traitements mentionnant l'existence du modèle automatisé
- Description de la logique du modèle (niveau AIPD — Analyse d'Impact sur la Protection des Données)
- Conservation des explications fournies aux clients (5 ans minimum)

### 5.2 SR 11-7 — Lignes Directrices sur la Validation des Modèles

La circulaire SR 11-7 de la Fed (appliquée par analogie en Europe via les lignes directrices BCE) définit les standards de gouvernance des modèles.

**Trois piliers de la validation des modèles :**

**1. Évaluation conceptuelle et théorique :**
- Le modèle est-il théoriquement fondé ? Les relations entre variables et output sont-elles cohérentes avec la théorie économique et financière ?
- Les variables utilisées sont-elles pertinentes et légitimes ?
- Le modèle présente-t-il des biais connus ?

**2. Vérification des processus et données :**
- La qualité des données d'entraînement est-elle documentée ?
- Les transformations et feature engineering sont-elles justifiées ?
- Le découpage train/test/validation est-il correct ?

**3. Test des outcomes (backtesting) :**
- Les prédictions du modèle correspondent-elles aux observations réelles ?
- Le modèle reste-t-il performant sur de nouvelles données (out-of-time testing) ?
- Y a-t-il dérive significative (PSI, CSI) ?

**Fréquence de validation recommandée :**
- Validation complète : annuelle minimum
- Surveillance continue : mensuelle (KPIs performance + stabilité)
- Revue ad hoc : à chaque changement significatif des données ou de l'environnement

### 5.3 Détection et Gestion des Biais Algorithmiques

Un modèle de crédit ou de fraude ne doit pas discriminer sur des critères protégés (genre, origine, âge, handicap).

**Variables directement discriminantes (interdites) :**
- Genre, origine ethnique, nationalité, religion, état de santé, orientation sexuelle

**Variables indirectement discriminantes (proxies — à surveiller) :**
- Code postal → peut être corrélé à l'origine ethnique (redlining)
- Prénom → peut être corrélé au genre ou à l'origine
- Type de téléphone (prépayé vs abonnement) → peut défavoriser certaines populations

**Tests de détection de biais :**

**Disparate Impact Analysis :**
```
Ratio = Taux d'approbation groupe minoritaire / Taux d'approbation groupe majoritaire
```
Seuil réglementaire : ratio < 0.80 → discrimination adverse potentielle (règle des 4/5)

**Equal Opportunity :**
Vérifier que le recall (taux de détection) est équivalent entre groupes pour le modèle de fraude → éviter que certains groupes soient sur-surveillés

**Actions correctives :**
- Suppression de la variable biaisée si possible
- Re-pondération des données d'entraînement (reweighting)
- Post-processing du score pour corriger l'écart (calibration par groupe)
- Changement d'algorithme (certains modèles sont intrinsèquement plus équitables)

### 5.4 Documentation et Traçabilité des Modèles

**Model Card (fiche modèle) — éléments obligatoires :**
- Nom et version du modèle
- Date de développement et date de mise en production
- Objectif du modèle (PD 12 mois, fraud score, etc.)
- Périmètre d'application (segment de clientèle, produits)
- Données d'entraînement (période, volume, source)
- Performance sur le jeu de validation (AUC, Gini, KS, F1)
- Variables utilisées et leur importance globale
- Limites connues et zones d'incertitude
- Fréquence de révision et responsable du modèle

**Versioning des modèles :**
- Chaque version du modèle doit être archivée (code + données + artefacts)
- Les prédictions historiques doivent pouvoir être reproduites (reproductibilité)
- Un registre des modèles centralise toutes les versions en production

---

## 6. Outils et Implémentation

### 6.1 Librairies Python Recommandées

**SHAP :**
```python
import shap

# Pour XGBoost / LightGBM (TreeSHAP — très rapide)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# SHAP value pour une observation individuelle
shap.force_plot(explainer.expected_value, shap_values[0], X.iloc[0])

# Importance globale
shap.summary_plot(shap_values, X)

# Dependence plot (relation variable → SHAP)
shap.dependence_plot("DTI", shap_values, X)
```

**LIME :**
```python
from lime.lime_tabular import LimeTabularExplainer

explainer = LimeTabularExplainer(
    X_train.values,
    feature_names=feature_names,
    class_names=["Non-défaut", "Défaut"],
    mode="classification"
)

# Explication locale pour une observation
explanation = explainer.explain_instance(
    X_test.iloc[0].values,
    model.predict_proba,
    num_features=10
)
explanation.show_in_notebook()
```

**Alibi (Counterfactual Explanations) :**
```python
from alibi.explainers import CounterfactualProto

cf = CounterfactualProto(model.predict, shape=(1, n_features))
cf.fit(X_train)
explanation = cf.explain(X_test[0:1])
print("Counterfactual :", explanation.cf['X'])
```

### 6.2 Pipeline d'Explicabilité en Production

Pour générer des explications en temps réel sans impacter les performances, l'architecture recommandée est :

**Calcul synchrone (temps réel) :**
- TreeSHAP pour les modèles d'arbres : < 5 ms par prédiction → intégrable dans le pipeline temps réel
- Extraction des top 5 SHAP values (positives + négatives) → stockées avec la décision

**Calcul asynchrone (batch) :**
- Explication complète (toutes les variables) générée en batch après la décision
- Stockée dans un datastore d'explicabilité (associée à l'ID de la décision)
- Accessible pour les analystes, les audits et les réponses aux clients

**Stockage des explications :**
```json
{
  "decision_id": "DEC-2024-001234",
  "client_id": "CLI-789456",
  "timestamp": "2024-03-15T14:32:11Z",
  "model_version": "credit_scoring_v2.3",
  "score": 480,
  "pd": 0.083,
  "decision": "REVIEW",
  "top_shap_positive": [
    {"feature": "dti", "value": 0.33, "shap": 0.021},
    {"feature": "incident_dpd30_12m", "value": 1, "shap": 0.018},
    {"feature": "revolving_utilization", "value": 0.88, "shap": 0.008}
  ],
  "top_shap_negative": [
    {"feature": "employment_seniority_years", "value": 6, "shap": -0.009},
    {"feature": "contract_type_cdi", "value": 1, "shap": -0.006}
  ],
  "client_explanation": "Votre taux d'endettement actuel est élevé..."
}
```

---

## 7. Cas d'Usage Opérationnels

### 7.1 Cas d'Usage : Répondre à une Demande d'Explication Client (RGPD)

**Contexte :** Un client a été refusé pour un prêt de 10 000 €. Il contacte le service client pour comprendre les raisons.

**Données internes (SHAP values) :**
- DTI = 38% → SHAP = +0.021 (facteur le plus impactant)
- Incident DPD30 il y a 8 mois → SHAP = +0.018
- CDD (contrat précaire) → SHAP = +0.012
- Ancienneté crédit courte (2 ans) → SHAP = +0.007

**Réponse au client (conforme RGPD) :**
"Suite à l'analyse de votre dossier, votre demande de crédit n'a pas pu être accordée pour les raisons principales suivantes :
1. Votre taux d'endettement actuel, incluant les remboursements de vos crédits en cours rapportés à vos revenus, dépasse le seuil que nous appliquons.
2. Un incident de remboursement a été enregistré dans votre historique de crédit au cours des 12 derniers mois.
3. Votre situation professionnelle actuelle (contrat à durée déterminée) présente une instabilité aux yeux de notre analyse.
Vous avez le droit de demander une révision de cette décision par un conseiller humain. Pour exercer ce droit, contactez-nous au [numéro] ou par courrier à [adresse]."

### 7.2 Cas d'Usage : Audit Réglementaire du Modèle

**Contexte :** Le régulateur demande une revue du modèle de scoring crédit. Il veut s'assurer de l'absence de discrimination.

**Analyse de disparate impact par tranche d'âge :**

| Tranche d'âge | Taux d'approbation | Ratio vs 30-40 ans |
|---|---|---|
| 18–25 ans | 52% | 0.78 → sous le seuil 0.80 ⚠️ |
| 26–40 ans | 67% | 1.00 (référence) |
| 41–60 ans | 71% | 1.06 ✅ |
| 61–75 ans | 58% | 0.87 ✅ |

**Analyse des SHAP values par groupe d'âge :**
- Les 18–25 ans ont un taux d'approbation plus faible principalement à cause de l'ancienneté d'emploi courte et de l'historique de crédit court → discrimination indirecte mais justifiée économiquement (et non basée sur l'âge directement)
- Action : documenter la justification économique, surveiller l'évolution du ratio

### 7.3 Cas d'Usage : Détection de Dérive du Modèle

**Contexte :** La feature importance du modèle de fraude est analysée mensuellement. On observe une anomalie.

**Analyse :**
- En janvier : top feature = "email_age_days" (SHAP moyen = 0.18)
- En mars : top feature = "email_age_days" (SHAP moyen = 0.32) → doublement de l'importance

**Investigation :**
- Une campagne de fraude spécifique utilise des emails très récents (< 2 jours)
- Le modèle a bien détecté cette tendance mais le seuil de score doit être ajusté
- Nouvelle règle métier ajoutée : email < 2 jours → hard rule (blocage immédiat)

---

## 8. Glossaire

| Terme | Définition |
|---|---|
| XAI (Explainable AI) | Intelligence artificielle explicable : ensemble des techniques visant à rendre les modèles ML interprétables |
| SHAP | SHapley Additive exPlanations : méthode d'explicabilité basée sur la théorie des jeux |
| SHAP Value | Contribution marginale d'une variable à une prédiction individuelle |
| TreeSHAP | Implémentation rapide de SHAP optimisée pour les modèles d'arbres |
| LIME | Local Interpretable Model-agnostic Explanations : méthode d'explicabilité locale par approximation linéaire |
| Feature Importance | Mesure de la contribution relative de chaque variable à la performance globale du modèle |
| Permutation Importance | Feature importance calculée en mesurant la dégradation de performance après permutation aléatoire d'une variable |
| Counterfactual Explanation | Explication contrefactuelle : "que faudrait-il changer pour obtenir une décision différente ?" |
| PDP | Partial Dependence Plot : courbe montrant l'effet marginal d'une variable sur la prédiction |
| ICE Plot | Individual Conditional Expectation : variante du PDP montrant les effets individuels |
| Explicabilité Globale | Comportement général du modèle sur l'ensemble des données |
| Explicabilité Locale | Explication d'une décision spécifique pour un individu donné |
| Boîte Noire | Modèle dont la logique interne n'est pas directement interprétable (XGBoost, réseau de neurones) |
| Scorecard | Modèle de scoring linéaire avec points attribués par variable — intrinsèquement interprétable |
| RGPD Article 22 | Article imposant le droit à l'explication pour les décisions automatisées |
| SR 11-7 | Circulaire réglementaire américaine sur la validation des modèles (référence mondiale) |
| AIPD | Analyse d'Impact sur la Protection des Données (obligatoire pour les traitements à risque élevé) |
| Disparate Impact | Discrimination indirecte mesurée par le ratio de taux d'approbation entre groupes |
| Règle des 4/5 | Seuil de disparate impact : ratio < 0.80 signale une discrimination adverse potentielle |
| Model Card | Fiche standardisée documentant les caractéristiques, performances et limites d'un modèle |
| Concept Drift | Évolution de la relation entre les variables et la cible dans le temps |
| Data Drift | Évolution de la distribution des variables d'entrée du modèle dans le temps |
| PSI | Population Stability Index : mesure la dérive de la distribution du score |
| CSI | Characteristic Stability Index : mesure la dérive variable par variable |
| Backtesting | Vérification des performances du modèle sur des données historiques non utilisées à l'entraînement |
| Out-of-Time Testing | Backtesting sur une période temporelle postérieure à la période d'entraînement |
| Model Registry | Registre centralisant toutes les versions des modèles en production |
| Tipping-Off | Informer un suspect qu'il est sous surveillance (interdit en LCB-FT) |
| Gaming du Modèle | Manipulation délibérée des variables d'entrée pour obtenir un score plus favorable |
