# Documentation — Modèle de Risque de Crédit Consommation (Particuliers)

## Vue d'ensemble

Ce document décrit le modèle de risque de crédit appliqué aux particuliers dans le cadre du crédit consommation. Il couvre les concepts fondamentaux, les métriques de risque, les composantes du scoring, les règles de décision et les cas d'usage opérationnels. Il est destiné à être utilisé comme base de connaissance pour un assistant IA spécialisé en analyse de risque de crédit.

**Domaine :** Crédit consommation — particuliers (retail lending)
**Périmètre :** Prêts personnels, crédits revolving, crédits affectés
**Mots-clés :** credit risk, default, scoring, PD, LGD, EAD, EL, creditworthiness, underwriting, bureau de crédit

---

## 1. Concepts Fondamentaux du Risque de Crédit

### 1.1 Définition du Risque de Crédit

Le risque de crédit est le risque qu'un emprunteur ne rembourse pas tout ou partie de sa dette selon les termes contractuels. Dans le contexte du crédit consommation, il se matérialise lorsqu'un particulier cesse de rembourser son prêt personnel, son crédit revolving ou son crédit affecté (automobile, électroménager, etc.).

**Synonymes :** risque de contrepartie, risque de défaut, credit default risk
**Impact :** perte financière directe pour le prêteur, provisionnement réglementaire, capital réglementaire (Bâle III/IV)

### 1.2 Définition du Défaut (Default)

Un emprunteur est en situation de défaut lorsqu'il remplit l'une des conditions suivantes :
- **Retard de paiement :** impayé supérieur à 90 jours consécutifs (critère réglementaire Bâle III)
- **Improbabilité de paiement (UTP) :** la banque estime que le client ne remboursera pas sans recours à des garanties ou saisies
- **Dépôt de bilan ou surendettement :** procédure légale engagée (dossier Commission de Surendettement, liquidation judiciaire)

**Seuil de matérialité :** Un retard est significatif si le montant impayé dépasse 100 € ET représente plus de 1% de l'exposition totale (seuil EBA 2021).

### 1.3 Perte Attendue (Expected Loss — EL)

La perte attendue est le montant moyen de perte qu'un prêteur anticipe sur un portefeuille de crédit sur une période donnée (généralement 12 mois).

**Formule :**
```
EL = PD × LGD × EAD
```

- **PD** = Probability of Default (probabilité de défaut)
- **LGD** = Loss Given Default (perte en cas de défaut)
- **EAD** = Exposure at Default (exposition au moment du défaut)

**Exemple :** Pour un prêt de 10 000 €, avec PD = 5%, LGD = 60%, EAD = 10 000 € :
```
EL = 0.05 × 0.60 × 10 000 = 300 €
```
Ce montant correspond au provisionnement minimum attendu (IFRS 9 Stage 1).

---

## 2. Métriques Clés du Modèle

### 2.1 Probabilité de Défaut (PD — Probability of Default)

La PD mesure la probabilité qu'un emprunteur entre en situation de défaut dans les 12 prochains mois. C'est la sortie principale du modèle de scoring.

**Plage de valeurs :** 0 (aucun risque) à 1 (défaut certain)
**Expression courante :** en pourcentage (ex : PD = 3,2%)

**Segmentation typique par niveau de PD :**

| Segment | PD | Interprétation |
|---|---|---|
| Très faible risque | < 1% | Emprunteur excellent, historique irréprochable |
| Faible risque | 1% – 3% | Profil standard, approbation automatique possible |
| Risque modéré | 3% – 8% | Revue manuelle recommandée |
| Risque élevé | 8% – 20% | Conditions restrictives ou garanties exigées |
| Très haut risque | > 20% | Refus probable ou offre dégradée |

**Méthodes de calcul :**
- Régression logistique (modèle standard, interprétable)
- Gradient Boosting (XGBoost, LightGBM) — meilleure performance prédictive
- Réseaux de neurones — utilisés pour des volumes très élevés

### 2.2 Perte en Cas de Défaut (LGD — Loss Given Default)

La LGD représente la fraction de l'exposition que le prêteur ne récupèrera pas après qu'un défaut s'est produit, compte tenu des recouvrements (garanties, saisies, négociations).

**Formule :**
```
LGD = 1 - Taux de Recouvrement
```

**Valeurs typiques pour le crédit consommation non garanti :**
- LGD moyenne : 60% à 80% (peu de garanties sur les prêts personnels)
- Avec garantie (caution, hypothèque) : LGD peut descendre à 20%-40%

**Facteurs qui influencent la LGD :**
- Présence ou absence de garanties (collatéral)
- Ancienneté du défaut (plus il est vieux, plus le recouvrement est difficile)
- Profil socio-économique (revenus, actifs)
- Efficacité du processus de recouvrement interne

### 2.3 Exposition au Moment du Défaut (EAD — Exposure at Default)

L'EAD est le montant total que l'emprunteur doit au moment où il entre en défaut. Pour un crédit consommation classique (amortissable), l'EAD diminue au fil du temps. Pour un crédit revolving, l'EAD peut dépasser le solde actuel (tirage supplémentaire avant défaut).

**Pour un prêt amortissable :**
```
EAD ≈ Capital restant dû (CRD)
```

**Pour un crédit revolving :**
```
EAD = Solde actuel + (Limite disponible × CCF)
```
Où **CCF** (Credit Conversion Factor) estime le taux d'utilisation supplémentaire avant défaut (typiquement 50%–75%).

### 2.4 Score de Crédit (Credit Score)

Le score de crédit est un indicateur synthétique (généralement entre 0 et 1000) qui traduit la PD en une valeur facilement interprétable par les équipes métier.

**Correspondance score ↔ PD :**

| Score | PD estimée | Décision suggérée |
|---|---|---|
| 800 – 1000 | < 1% | Approbation automatique |
| 650 – 799 | 1% – 3% | Approbation standard |
| 500 – 649 | 3% – 8% | Revue manuelle |
| 350 – 499 | 8% – 20% | Conditions restrictives |
| 0 – 349 | > 20% | Refus recommandé |

**Note :** La correspondance exacte score ↔ PD dépend du calibrage du modèle (scorecard calibration). Elle doit être recalibrée régulièrement (typiquement annuellement).

### 2.5 Ratio Coût du Risque (Cost of Risk — CoR)

Le coût du risque mesure le niveau de provisionnement rapporté à l'encours total.

**Formule :**
```
CoR = Dotations aux provisions / Encours moyen × 100
```

**Benchmarks crédit consommation France :**
- Conjoncture normale : 1,5% – 2,5%
- Période de stress : 3,0% – 5,0%
- Crise majeure (ex : COVID-19 2020) : jusqu'à 7%

---

## 3. Variables et Facteurs de Risque

### 3.1 Variables Socio-Démographiques

Ces variables décrivent le profil personnel de l'emprunteur. Elles contribuent à la segmentation mais sont soumises à des contraintes réglementaires anti-discrimination (RGPD, égalité de traitement).

**Variables autorisées et pertinentes :**
- **Âge :** corrélé à la stabilité financière ; les très jeunes (18–25 ans) et très âgés (>75 ans) présentent des profils spécifiques
- **Situation familiale :** nombre de personnes à charge (impact sur le reste à vivre)
- **Statut de résidence :** propriétaire / locataire / hébergé (stabilité résidentielle)
- **Ancienneté à l'adresse actuelle :** proxy de stabilité

**Variables interdites ou sensibles :** origine ethnique, nationalité, état de santé (hors assurance décès-invalidité), religion.

### 3.2 Variables Financières et Revenus

Ces variables sont les plus prédictives du risque de défaut. Elles permettent d'évaluer la capacité de remboursement réelle.

**Revenu net mensuel (RNM) :**
- Source : bulletins de salaire, avis d'imposition, relevés bancaires
- Composantes : salaire net, allocations, pensions, revenus locatifs (décote de 20%–30%)
- Les revenus variables (primes, intérim) sont souvent décotés de 50%

**Taux d'endettement (Debt-to-Income — DTI) :**
```
DTI = Total des charges mensuelles de crédit / Revenu net mensuel × 100
```
- Seuil réglementaire HCSF France : DTI ≤ 35% (depuis janvier 2022)
- Au-delà de 35% : refus automatique ou dérogation limitée (20% des dossiers)

**Reste à vivre (RAV) :**
```
RAV = Revenu net mensuel - Total des charges mensuelles (loyer + crédits + charges fixes)
```
- Seuil minimal accepté : variable selon composition familiale
- Exemple : 800 €/mois pour une personne seule, 400 €/mois par enfant supplémentaire

### 3.3 Variables Comportementales (Données Bancaires)

Les données comportementales issues des relevés de compte bancaire sont parmi les plus prédictives du risque à court terme.

**Signaux de risque positifs (réducteurs de PD) :**
- Solde créditeur moyen en hausse sur 3 mois
- Épargne régulière (virement automatique vers livret)
- Absence d'incidents de paiement sur 12 mois
- Régularité des flux entrants (salaire mensuel stable)

**Signaux de risque négatifs (augmentateurs de PD) :**
- Découverts récurrents (>3 fois/trimestre)
- Utilisation maximale du crédit revolving (>80% de la limite)
- Remboursements minimum uniquement sur carte de crédit
- Refus de prélèvement SEPA sur 6 mois
- Augmentation soudaine des dépenses en jeux ou paris

### 3.4 Variables d'Historique de Crédit (Bureau de Crédit)

En France, le principal registre négatif est le Fichier national des Incidents de remboursement des Crédits aux Particuliers (**FICP**), géré par la Banque de France.

**Statut FICP :**
- Inscription FICP active → quasi-systématiquement éliminatoire
- Sortie FICP depuis < 12 mois → risque résiduel élevé

**Autres données bureau :**
- Nombre de crédits en cours (multi-endettement)
- Nombre de demandes de crédit récentes (hard inquiries) sur 6 mois → signal négatif si >3
- Ancienneté du premier crédit (credit history length) → signal positif si >5 ans
- Taux d'utilisation global des lignes de crédit disponibles

### 3.5 Variables Liées à l'Emploi

La stabilité professionnelle est un facteur clé de la capacité de remboursement future.

**Facteurs favorables :**
- CDI (Contrat à Durée Indéterminée) : ancienneté > 6 mois
- Fonctionnaire titulaire : profil très stable
- Professions libérales : revenus vérifiés sur 3 exercices comptables

**Facteurs défavorables :**
- CDD ou intérim : revenus instables, emploi non pérenne
- Période d'essai (< 3 mois d'ancienneté)
- Travailleur indépendant avec moins de 2 ans d'activité
- Chômage ou en cours de reconversion

---

## 4. Processus de Scoring et Décision

### 4.1 Pipeline de Scoring — Vue Générale

Le pipeline de scoring d'un dossier de crédit consommation suit les étapes suivantes :

1. **Collecte des données** : formulaire client + pièces justificatives + données bureau
2. **Vérification et enrichissement** : contrôle de cohérence, croisement FICP, données bancaires
3. **Calcul du score** : application du modèle ML (régression logistique ou GBDT)
4. **Transformation en PD** : calibration du score → probabilité de défaut
5. **Application des règles métier** : règles éliminatoires, seuils DTI, âge minimum/maximum
6. **Décision finale** : automatique (approve/reject) ou renvoi en revue manuelle
7. **Justification et archivage** : RGPD, droit à l'explication (article 22)

### 4.2 Règles Éliminatoires Automatiques

Ces règles entraînent un rejet immédiat, indépendamment du score calculé.

**Règles éliminatoires absolues :**
- Inscription FICP active au moment de la demande
- DTI calculé > 35% après intégration du nouveau crédit (règle HCSF)
- Âge < 18 ans ou capacité juridique non établie
- Revenus non vérifiables ou pièces justificatives manquantes
- Interdit bancaire (fichage Banque de France)
- Fausse déclaration détectée sur le dossier

**Règles éliminatoires conditionnelles (peuvent être levées) :**
- Score < 350 : rejet sauf dérogation avec garantie solide
- RAV < seuil minimum : rejet sauf co-emprunteur solvable

### 4.3 Zones de Décision et Workflow

**Zone Verte — Approbation automatique :**
- Score ≥ 650 ET DTI ≤ 30% ET aucune règle éliminatoire
- Décision en temps réel (< 2 secondes)
- Aucune intervention humaine requise

**Zone Orange — Revue manuelle :**
- Score entre 350 et 649, OU DTI entre 30% et 35%, OU signal comportemental négatif isolé
- Dossier transmis à un analyste crédit
- Délai de décision : 24h à 72h ouvrées
- L'analyste peut approuver, rejeter, ou proposer une contre-offre

**Zone Rouge — Rejet automatique :**
- Score < 350 OU règle éliminatoire absolue déclenchée
- Notification immédiate au client
- Motif de refus communiqué (obligation légale en France)

### 4.4 Personnalisation de l'Offre (Risk-Based Pricing)

En zone orange ou pour des profils intermédiaires, le taux d'intérêt et les conditions peuvent être ajustés en fonction du risque.

**Principe du Risk-Based Pricing :**
```
Taux proposé = Taux de référence + Prime de risque
Prime de risque ∝ PD × LGD (coût du risque attendu)
```

**Exemples d'ajustements :**
- PD < 2% → taux préférentiel (-50 bps à -100 bps vs taux standard)
- PD entre 5% et 10% → majoration de 150 bps à 300 bps
- Réduction du montant accordé (75% ou 50% du montant demandé)
- Exigence d'un co-emprunteur ou d'une assurance renforcée

---

## 5. Segmentation du Portefeuille

### 5.1 Segmentation par Produit

**Prêt personnel amortissable :**
- Durée : 12 à 84 mois
- Montant : 1 000 € à 75 000 €
- Taux fixe, mensualités constantes
- EAD = Capital restant dû (décroissant)
- LGD élevée (pas de garantie standard)

**Crédit revolving (réserve d'argent) :**
- Limite : 500 € à 6 000 €
- Utilisation variable (taux utilisation = signal comportemental fort)
- EAD = Solde + CCF × (Limite – Solde utilisé)
- Risque de spirale d'endettement si remboursements minimums uniquement

**Crédit affecté (automobile, électroménager) :**
- Lié à un achat spécifique (résiliable si achat annulé)
- Bien financé peut servir de garantie partielle → LGD plus faible
- Durée : 6 à 60 mois

**Rachat de crédits :**
- Regroupement de plusieurs crédits en un seul
- Profil souvent à risque élevé (surendettement potentiel)
- Analyse approfondie du passif total obligatoire

### 5.2 Segmentation par Profil de Risque

**Prime (Faible risque) :**
- PD < 2%, DTI < 25%, CDI ancienneté > 2 ans, aucun incident
- Stratégie : acquisition, fidélisation, offres pré-approuvées

**Standard (Risque modéré) :**
- PD entre 2% et 8%, DTI entre 25% et 33%, emploi stable
- Stratégie : scoring standard, conditions normales

**Near-prime (Risque élevé mais acceptable) :**
- PD entre 8% et 15%, historique avec 1–2 incidents anciens
- Stratégie : revue manuelle, conditions restrictives, montant réduit

**Subprime (Très haut risque) :**
- PD > 15%, FICP récent, multi-endettement
- Stratégie : refus ou offre très limitée avec garanties

---

## 6. Surveillance et Suivi du Portefeuille

### 6.1 Indicateurs de Performance du Modèle

**Gini / AUC-ROC :**
- Mesure la capacité discriminante du modèle
- Valeur cible en crédit consommation : Gini ≥ 45% (AUC ≥ 0,725)
- En dessous de 35% : modèle insuffisant, recalibrage nécessaire

**KS (Kolmogorov-Smirnov) :**
- Mesure la séparation maximale entre distribution des bons et mauvais payeurs
- Valeur cible : KS ≥ 35%

**PSI (Population Stability Index) :**
- Mesure la stabilité de la distribution du score entre deux périodes
- PSI < 0,10 : distribution stable (pas d'action requise)
- PSI entre 0,10 et 0,25 : dérive légère (surveillance accrue)
- PSI > 0,25 : dérive significative (recalibrage du modèle requis)

### 6.2 Indicateurs de Qualité du Portefeuille

**Taux de défaut (Default Rate) :**
```
Default Rate = Nombre de nouveaux défauts / Encours en début de période
```
- Seuil d'alerte : +20% vs période précédente

**Vintage Analysis :**
Suivi des cohortes de prêts accordés au même trimestre pour mesurer l'évolution du taux de défaut cumulé dans le temps. Permet d'identifier les millésimes sous-performants et d'ajuster les critères d'octroi.

**Early Warning Indicators (EWI) — Signaux précurseurs :**
- Taux d'utilisation revolving > 90% sur 2 mois consécutifs
- Retard de 30 jours (DPD30) → précurseur de défaut dans 60% des cas sur horizon 6 mois
- Baisse de plus de 30% des flux créditeurs mensuels

### 6.3 Gestion du Cycle de Vie du Crédit

**Pré-défaut (Early Collection) :**
- Déclenchement : DPD > 7 jours
- Actions : rappels automatiques (SMS, email), proposition de report d'échéance
- Objectif : cure rate (retour à la normale) > 70% sur DPD 7–30

**Contentieux (Late Collection) :**
- Déclenchement : DPD > 90 jours (classement en défaut)
- Actions : mise en demeure, proposition de restructuration, saisine huissier
- Provisionnement : passage en Stage 3 (IFRS 9), provision = LGD × EAD

**Cession de créances (Debt Sale) :**
- Créances en défaut > 12 mois cédées à des sociétés de recouvrement
- Prix de cession typique : 5% à 15% de la valeur nominale
- Impacte directement le taux de recouvrement et donc le LGD observé

---

## 7. Réglementation et Conformité

### 7.1 Réglementation Prudentielle (Bâle III / CRR2)

Le cadre réglementaire Bâle III impose aux établissements de crédit de détenir un capital minimum proportionnel à leur exposition au risque de crédit.

**Approche Standard (SA) :**
- Pondérations fixes définies par le régulateur selon le type d'exposition
- Crédit consommation non garanti : pondération de 75% (retail exposure)
- Calcul : RWA = EAD × Pondération

**Approche Fondée sur les Notations Internes (IRB) :**
- Utilisation des modèles internes PD, LGD, EAD validés par le régulateur
- Conditions d'accès : historique de données > 5 ans, validation interne et externe

### 7.2 IFRS 9 — Provisionnement

La norme IFRS 9 impose un provisionnement prospectif basé sur les pertes attendues.

**Trois stages de provisionnement :**

| Stage | Critère | Provision |
|---|---|---|
| Stage 1 | Aucune dégradation significative | ECL 12 mois = EL annuelle |
| Stage 2 | Dégradation significative du risque | ECL lifetime (durée résiduelle totale) |
| Stage 3 | Défaut avéré | ECL lifetime + provision spécifique |

**Critères de passage Stage 1 → Stage 2 :**
- Hausse de la PD relative > 100% depuis l'octroi (doublement du risque)
- DPD > 30 jours
- Restructuration accordée pour difficultés financières

### 7.3 Réglementation Française Spécifique

**Loi Lagarde (2010) :**
- Encadrement du crédit revolving : mention obligatoire du coût total
- Obligation de proposer le prêt amortissable en alternative au revolving

**Recommandation HCSF (2022) :**
- DTI ≤ 35% (charges crédit / revenu net)
- Durée maximale : 25 ans (27 ans avec différé)
- Marge de dérogation : 20% des nouveaux crédits par trimestre

**Droit à l'explication (RGPD, article 22) :**
- Tout refus basé sur une décision automatisée doit être explicable au client
- Le client peut demander une intervention humaine pour révision
- Obligation d'archivage des décisions et de leurs justifications (5 ans minimum)

---

## 8. Cas d'Usage Opérationnels

### 8.1 Cas d'Usage : Évaluation d'un Nouveau Dossier

**Contexte :** Un client demande un prêt personnel de 15 000 € sur 60 mois.

**Données collectées :**
- Revenu net mensuel : 2 800 €
- Charges actuelles : loyer 700 €, crédit auto 280 €
- DTI avant nouveau crédit : (280 / 2 800) = 10%
- Mensualité estimée nouveau crédit (taux 5%, 60 mois) : 283 €/mois
- DTI après : (280 + 283) / 2 800 = **20%** → sous le seuil HCSF ✅
- Score calculé : 710 → PD estimée : 1,8%
- RAV : 2 800 - 700 - 280 - 283 = **1 537 €/mois** → suffisant ✅
- FICP : non inscrit ✅

**Décision :** Approbation automatique — Zone Verte.

### 8.2 Cas d'Usage : Profil Limite (Zone Orange)

**Contexte :** Un client demande 8 000 € sur 48 mois.

**Données :**
- Revenu net : 1 900 € (CDD depuis 4 mois)
- DTI actuel : 18%, DTI projeté après crédit : 31%
- Score : 520 → PD : 5,5%
- RAV projeté : 490 € → proche du seuil (personne seule)
- Incident bancaire il y a 18 mois (DPD 45 jours, régularisé)

**Décision :** Revue manuelle — Zone Orange.
- Points d'attention pour l'analyste : stabilité emploi (CDD), RAV limite, incident récent
- Option : réduire le montant à 5 000 € pour améliorer le DTI et le RAV

### 8.3 Cas d'Usage : Détection de Dégradation en Portefeuille

**Contexte :** Surveillance mensuelle d'un client existant (crédit revolving).

**Signaux détectés :**
- Taux d'utilisation revolving : passé de 40% à 92% en 2 mois
- 2 refus de prélèvement sur le compte bancaire principal
- Baisse des flux créditeurs de 35% (changement d'employeur ?)
- DPD actuel : 0 (pas encore en retard)

**Action :** Déclenchement d'une alerte Early Warning (EWI).
- Gel des augmentations de limite
- Contact proactif du client (proposition d'étalement)
- Passage en surveillance Stage 2 (IFRS 9) si la situation persiste
- Provisionnement ECL lifetime calculé sur la durée résiduelle

---

## 9. Glossaire

| Terme | Définition |
|---|---|
| PD (Probability of Default) | Probabilité qu'un emprunteur entre en défaut sur 12 mois |
| LGD (Loss Given Default) | Fraction de l'EAD non récupérée après défaut |
| EAD (Exposure at Default) | Montant dû au moment du défaut |
| EL (Expected Loss) | Perte attendue = PD × LGD × EAD |
| UL (Unexpected Loss) | Perte au-delà de l'EL, couverte par le capital |
| DTI (Debt-to-Income) | Ratio charges crédit / revenu net |
| RAV (Reste à vivre) | Revenu net - toutes charges mensuelles |
| DPD (Days Past Due) | Nombre de jours de retard de paiement |
| FICP | Fichier national des Incidents de remboursement des Crédits aux Particuliers |
| PSI (Population Stability Index) | Indicateur de dérive de la distribution du score |
| KS (Kolmogorov-Smirnov) | Indicateur de séparation bons / mauvais payeurs |
| AUC-ROC | Aire sous la courbe ROC — discriminance du modèle |
| Gini | 2 × AUC - 1 — version normalisée de l'AUC |
| CCF (Credit Conversion Factor) | Facteur de conversion pour EAD sur crédit revolving |
| ECL (Expected Credit Loss) | Perte de crédit attendue (terminologie IFRS 9) |
| RWA (Risk-Weighted Assets) | Actifs pondérés par le risque (Bâle III) |
| EWI (Early Warning Indicator) | Indicateur précurseur de défaut |
| HCSF | Haut Conseil de Stabilité Financière (régulateur macroprudentiel français) |
| Vintage | Cohorte de crédits accordés sur une même période |
| Stage 1/2/3 | Niveaux de provisionnement IFRS 9 selon la dégradation du risque |
| IRB (Internal Ratings-Based) | Approche de calcul du capital réglementaire basée sur modèles internes |
| Scorecard | Outil de scoring linéaire avec points attribués par variable |
| Calibration | Ajustement du modèle pour que les PD prédites correspondent aux taux de défaut observés |
| Cure Rate | Taux de retour à la normale après un incident de paiement |
