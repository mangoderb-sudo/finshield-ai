# Documentation — Détection de Fraude : Crédit Consommation (Particuliers)

## Vue d'ensemble

Ce document décrit le modèle de détection de fraude appliqué au crédit consommation pour les particuliers. Il couvre les typologies de fraude, les signaux d'alerte, les variables prédictives, le pipeline de détection, les règles métier et les cas d'usage opérationnels. Il est destiné à être utilisé comme base de connaissance pour un assistant IA spécialisé en détection de fraude financière.

**Domaine :** Fraude au crédit consommation — particuliers
**Périmètre :** Fraude à l'identité, fraude documentaire, fraude comportementale, fraude organisée
**Mots-clés :** fraud detection, identity fraud, synthetic identity, document fraud, anomaly detection, fraud score, AML, KYC, chargeback, mule account

---

## 1. Typologies de Fraude

### 1.1 Fraude à l'Identité (Identity Fraud)

La fraude à l'identité consiste à utiliser les informations personnelles d'une tierce personne (réelle ou fictive) pour obtenir un crédit de manière frauduleuse.

**Usurpation d'identité simple :**
- Utilisation de documents d'identité volés ou perdus
- Détournement de l'identité d'un proche (fraude familiale)
- Achat de données personnelles sur le dark web (nom, adresse, numéro de sécu)

**Signaux caractéristiques :**
- Adresse postale différente de l'adresse déclarée depuis < 30 jours
- Numéro de téléphone enregistré très récemment (< 15 jours)
- Adresse email créée le jour même de la demande
- Incohérence entre l'âge déclaré et la date d'émission de la pièce d'identité
- Victimes souvent : personnes décédées récemment, personnes âgées, personnes sans activité numérique

### 1.2 Fraude à l'Identité Synthétique (Synthetic Identity Fraud)

La fraude synthétique est une forme avancée où le fraudeur crée une identité fictive en combinant des données réelles (ex : un vrai numéro de sécurité sociale) avec de fausses informations (faux nom, fausse adresse).

**Mécanisme :**
1. Création d'un profil hybride avec des données partiellement réelles
2. Construction d'un historique de crédit artificiel sur 6 à 24 mois (crédit à faible montant remboursé correctement)
3. Exploitation finale : demande de crédit élevé → disparition (bust-out fraud)

**Pourquoi c'est difficile à détecter :**
- L'identité synthétique ne correspond à aucune vraie victime → pas de signalement
- Le comportement initial est irréprochable (bons remboursements volontaires)
- Le profil passe les contrôles KYC standards

**Signaux spécifiques :**
- Numéro de sécurité sociale jamais utilisé auparavant mais associé à un adulte
- Historique de crédit très court mais parfait (aucun incident, utilisation maximale)
- Adresse résidentielle partagée avec de nombreuses autres demandes de crédit
- Augmentation soudaine des demandes de crédit sur 30 jours (bust-out pattern)

### 1.3 Fraude Documentaire

La fraude documentaire consiste à falsifier ou fabriquer des pièces justificatives pour tromper le prêteur sur la solvabilité réelle du demandeur.

**Documents les plus fréquemment falsifiés :**
- Bulletins de salaire : modification du salaire net, du nom de l'employeur, des cotisations
- Relevés bancaires : ajout de flux créditeurs fictifs, suppression d'incidents de paiement
- Avis d'imposition : modification du revenu fiscal de référence
- Contrats de travail : faux CDI, fausse ancienneté, faux employeur

**Méthodes de détection :**
- Vérification de cohérence interne (les chiffres sont-ils mathématiquement corrects ?)
- Contrôle de la mise en page (police, espacements, logos — comparaison avec modèles officiels)
- Croisement avec les données déclarées par l'employeur (URSSAF, DSN)
- Analyse des métadonnées du fichier PDF (date de création, logiciel utilisé, modifications)
- OCR + NLP pour détecter des incohérences textuelles

### 1.4 Fraude au Compte Mulet (Mule Account Fraud)

Un compte mulet est un compte bancaire utilisé comme intermédiaire pour recevoir et blanchir des fonds frauduleux. Le titulaire du compte peut être complice (mule consciente) ou victime (mule recrutée via escroquerie).

**Schéma typique :**
1. Un fraudeur obtient un crédit frauduleusement
2. Les fonds sont virés sur un ou plusieurs comptes mulets
3. Les mulets retirent les fonds en espèces ou les transfèrent à l'étranger
4. Le fraudeur disparaît, laissant le crédit impayé

**Signaux sur le compte récepteur :**
- Flux entrants importants et inhabituels suivis de retraits immédiats
- Virements entrants de multiples sources inconnues
- Retraits aux distributeurs dans des zones géographiques éloignées du domicile
- Absence d'utilisation courante du compte (pas de courses, factures, abonnements)

### 1.5 Fraude Organisée (Fraud Ring)

La fraude organisée implique un réseau structuré de fraudeurs qui coordonnent leurs actions pour maximiser les gains tout en évitant la détection.

**Caractéristiques d'un fraud ring :**
- Multiples demandes de crédit avec des caractéristiques similaires (même adresse IP, même appareil, même modèle de revenus)
- Même numéro de téléphone ou adresse email partagée entre plusieurs dossiers
- Plusieurs identités liées à une même adresse postale
- Timing coordonné : rafale de demandes sur une courte période

**Techniques de détection :**
- Graph analytics : détection de clusters d'entités connectées (même device, même adresse, même IP)
- Link analysis : identification des nœuds centraux du réseau
- Velocity checks : surveillance des demandes multiples sur une même session ou adresse

### 1.6 Fraude Interne

La fraude interne est commise par des employés de l'institution financière, qui abusent de leurs accès privilégiés pour valider des dossiers frauduleux ou manipuler des décisions.

**Formes courantes :**
- Validation de dossiers incomplets ou avec pièces falsifiées en échange de rémunération
- Création de faux dossiers clients (ghost accounts)
- Modification de scores ou de décisions dans les systèmes
- Divulgation de données clients à des réseaux de fraude externe

**Signaux :**
- Analyste crédit approuvant systématiquement des dossiers à risque élevé
- Accès aux systèmes en dehors des horaires de travail habituels
- Volume d'approbations anormalement élevé sur une courte période

---

## 2. Variables et Signaux de Fraude

### 2.1 Variables Comportementales Digitales (Digital Footprint)

Ces variables capturent le comportement numérique du demandeur lors de la soumission de la demande en ligne. Elles sont parmi les plus discriminantes.

**Device et session :**
- **Device fingerprint** : identifiant unique de l'appareil (navigateur, OS, résolution, plugins)
- **Adresse IP** : géolocalisation, réputation (IP connue dans des bases de fraude ?), proxy/VPN détecté
- **Vitesse de remplissage du formulaire** : < 2 minutes → suspect (bot ou données pré-remplies)
- **Copier-coller** : champs remplis par copier-coller (vs saisie manuelle) → signal de fraude documentaire

**Cohérence géographique :**
- Localisation IP vs adresse déclarée : écart > 50 km → signal d'alerte
- Localisation IP vs langue du navigateur
- Fuseau horaire du device vs pays déclaré

**Historique du device :**
- Cet appareil a-t-il déjà soumis d'autres demandes ? Avec quelles identités ?
- Nombre de demandes depuis cet appareil sur 30 jours (velocity check)

### 2.2 Variables d'Identité et KYC

**Vérification documentaire :**
- Validité et authenticité de la pièce d'identité (contrôle automatisé par OCR + IA)
- Cohérence entre photo et selfie en temps réel (liveness detection, anti-spoofing)
- Date d'expiration de la pièce d'identité
- Numéro de pièce d'identité dans une base de documents volés ou signalés

**Cohérence des données déclarées :**
- Correspondance nom + adresse + date de naissance avec les bases officielles
- Ancienneté de l'adresse email (< 7 jours = signal fort)
- Ancienneté du numéro de téléphone (< 15 jours = signal fort)
- Format du numéro de téléphone : numéro prépayé vs abonnement (les prépayés sont sur-représentés dans la fraude)

### 2.3 Variables de Vélocité (Velocity Features)

Les features de vélocité mesurent la fréquence des événements similaires sur des fenêtres temporelles glissantes. Elles sont très efficaces pour détecter la fraude organisée.

**Exemples de features de vélocité :**

| Feature | Fenêtre | Seuil d'alerte |
|---|---|---|
| Nb de demandes depuis la même IP | 24h | > 3 |
| Nb de demandes depuis le même device | 7 jours | > 2 |
| Nb de demandes avec le même numéro de tel | 30 jours | > 1 |
| Nb de demandes avec la même adresse postale | 30 jours | > 4 |
| Nb de demandes avec le même IBAN | 7 jours | > 2 |
| Nb de demandes avec la même adresse email | 24h | > 1 |

**Interprétation :** Une seule feature de vélocité déclenchée n'est pas forcément frauduleuse. C'est la combinaison de plusieurs features qui constitue le signal.

### 2.4 Variables Financières Suspectes

**Incohérences revenus / mode de vie :**
- Revenus déclarés très élevés mais absence totale d'historique bancaire
- Revenus déclarés élevés mais adresse dans zone très défavorisée (pas en soi discriminant, mais combiné à d'autres signaux)
- Montant demandé = montant maximum autorisé (comportement typique des fraudeurs qui maximisent l'extraction)

**Signaux sur le compte bancaire fourni :**
- IBAN ouvert très récemment (< 30 jours)
- IBAN appartenant à une néobanque (Revolut, N26, Lydia) associé à une demande de gros montant
- Flux bancaires trop réguliers et arrondis (revenus toujours exactement 2 500,00 € → possible falsification)
- Absence totale de dépenses courantes sur le relevé (loyer, courses, abonnements)

---

## 3. Modèle de Détection de Fraude

### 3.1 Architecture Générale du Modèle

Le modèle de détection de fraude est un système multicouche combinant règles métier et machine learning.

**Couche 1 — Règles déterministes (Hard Rules) :**
- Vérifications binaires immédiates (FICP, liste noire, document volé)
- Résultat : REJECT immédiat ou FLAG pour analyse approfondie
- Avantage : interprétable, pas de faux négatifs sur les cas connus

**Couche 2 — Score de fraude ML :**
- Modèle supervisé (XGBoost, Random Forest, réseau de neurones)
- Entraîné sur des dossiers historiques labellisés fraude / non-fraude
- Output : probabilité de fraude entre 0 et 1 (fraud score)

**Couche 3 — Graph Analytics :**
- Analyse des connexions entre entités (personnes, appareils, adresses, IBANs)
- Détection de clusters frauduleux (fraud rings)
- Complémentaire au score individuel : un dossier peut sembler propre mais faire partie d'un réseau

**Couche 4 — Revue humaine (Fraud Analyst) :**
- Dossiers en zone grise (fraud score entre 0.3 et 0.7)
- Investigations approfondies, contact du client, demandes de pièces complémentaires

### 3.2 Variables Clés du Modèle ML

**Features les plus importantes (classement typique par importance) :**

1. Vélocité IP sur 24h (nombre de demandes depuis la même IP)
2. Ancienneté de l'adresse email
3. Cohérence géographique IP / adresse déclarée
4. Device fingerprint : déjà associé à un dossier frauduleux ?
5. Durée de remplissage du formulaire
6. Ancienneté du numéro de téléphone
7. Montant demandé = montant maximum (flag binaire)
8. IBAN ouvert < 30 jours
9. Nombre de hard inquiries bureau sur 30 jours
10. Score de risque crédit (PD) — une PD très élevée combinée à un profil digital suspect est un signal fort

### 3.3 Seuils de Décision du Fraud Score

| Fraud Score | Zone | Action |
|---|---|---|
| 0.00 – 0.20 | Verte — Faible risque | Traitement normal, pas d'action spécifique |
| 0.20 – 0.40 | Jaune — Surveillance | Monitoring renforcé, vérifications supplémentaires |
| 0.40 – 0.70 | Orange — Suspicion | Revue manuelle obligatoire, contact client possible |
| 0.70 – 0.90 | Rouge — Fraude probable | Blocage préventif, investigation fraud analyst |
| 0.90 – 1.00 | Noir — Fraude quasi-certaine | Rejet immédiat, signalement, archivage |

**Note :** Les seuils doivent être calibrés selon l'appétit au risque de l'institution. Un seuil trop bas génère de faux positifs (clients légitimes bloqués). Un seuil trop haut laisse passer des fraudes.

### 3.4 Métriques de Performance du Modèle Fraude

La fraude est un problème de classification déséquilibrée (< 1% des dossiers sont frauduleux). Les métriques classiques (accuracy) sont inadaptées.

**Métriques adaptées :**

**Precision (Précision) :**
```
Precision = Vrais Positifs / (Vrais Positifs + Faux Positifs)
```
= Parmi les dossiers détectés comme fraude, combien sont vraiment des fraudes ?
Cible : > 80% (éviter de bloquer trop de clients légitimes)

**Recall (Rappel / Sensibilité) :**
```
Recall = Vrais Positifs / (Vrais Positifs + Faux Négatifs)
```
= Parmi toutes les fraudes réelles, combien ont été détectées ?
Cible : > 70% (ne pas laisser passer trop de fraudes)

**F1-Score :**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
Compromis entre précision et rappel. Cible : > 0.75

**AUC-PR (Area Under Precision-Recall Curve) :**
Préférable à l'AUC-ROC pour les datasets déséquilibrés. Cible : > 0.85

**Coût moyen par fraude non détectée vs coût moyen par faux positif :**
- Fraude non détectée : perte = EAD × LGD (ex : 8 000 € × 70% = 5 600 €)
- Faux positif : perte = manque à gagner + coût relationnel (ex : 200 €)
- Ratio : 1 fraude non détectée ≈ 28 faux positifs → calibrer le seuil en conséquence

---

## 4. Règles Métier Anti-Fraude

### 4.1 Règles Bloquantes Automatiques (Hard Rules)

Ces règles entraînent un rejet immédiat et irréversible, sans passer par le modèle ML.

**Règles bloquantes absolues :**
- Pièce d'identité présente dans la base des documents signalés volés / perdus
- Numéro de sécurité sociale associé à une personne décédée dans les registres
- IBAN présent dans la liste noire interne (déjà utilisé dans un dossier de fraude confirmée)
- Adresse IP classée dans les bases de réputation IP comme frauduleuse (IP blacklist)
- Adresse email présente dans la base des emails compromis (Have I Been Pwned ou équivalent)
- Fraud score ≥ 0.90
- Device fingerprint identique à un appareil ayant soumis un dossier de fraude confirmée

### 4.2 Règles de Surveillance Renforcée

Ces règles ne bloquent pas automatiquement mais déclenchent un niveau d'investigation supérieur.

**Déclencheurs de surveillance renforcée :**
- Adresse email créée < 7 jours avant la demande
- Numéro de téléphone activé < 15 jours avant la demande
- IBAN ouvert < 30 jours avant la demande
- Montant demandé = montant maximum de la gamme de produits
- Fraud score entre 0.40 et 0.70
- 2 features de vélocité déclenchées simultanément
- Incohérence géographique IP / adresse > 100 km sans explication
- Formulaire rempli en < 90 secondes

### 4.3 Règles de Challenge Client (Step-Up Authentication)

Lorsqu'un signal de risque est détecté sans atteindre le seuil de blocage, un challenge d'authentification supplémentaire est proposé au client pour confirmer son identité.

**Types de challenges :**
- **OTP (One-Time Password)** : code envoyé par SMS au numéro déclaré
- **Liveness check** : selfie vidéo en temps réel pour vérifier la correspondance avec la pièce d'identité
- **Question de sécurité** : informations que seul le vrai titulaire devrait connaître
- **Vérification bancaire** : micro-virement sur le compte fourni (1 centime) avec code à confirmer

**Cas d'usage du challenge :**
- Fraud score entre 0.20 et 0.40 + 1 feature de vélocité déclenchée
- Nouvelle adresse déclarée depuis < 30 jours
- Premier accès depuis un nouvel appareil non reconnu

---

## 5. Processus Opérationnel Anti-Fraude

### 5.1 Pipeline de Détection en Temps Réel

Le pipeline de détection doit répondre en temps réel (< 500 ms) pour ne pas dégrader l'expérience client.

**Étape 1 — Collecte des données de session (0–50 ms) :**
- Capture device fingerprint, IP, comportement de navigation
- Horodatage de chaque interaction avec le formulaire

**Étape 2 — Vérifications synchrones immédiates (50–150 ms) :**
- Consultation des listes noires (IP, IBAN, email, numéro de tel)
- Vérification FICP
- Contrôle format et validité pièce d'identité (OCR)

**Étape 3 — Calcul du fraud score ML (150–300 ms) :**
- Construction du vecteur de features
- Appel au modèle de scoring (API interne)
- Calcul des features de vélocité (base de données temps réel)

**Étape 4 — Application des règles métier (300–400 ms) :**
- Application des hard rules
- Combinaison fraud score + règles métier → décision

**Étape 5 — Décision et action (400–500 ms) :**
- APPROVE / CHALLENGE / REVIEW / REJECT
- Logging complet pour audit et réentraînement du modèle

### 5.2 Workflow de la Revue Manuelle (Fraud Analyst)

Lorsqu'un dossier est orienté en revue manuelle (fraud score entre 0.40 et 0.70), un analyste fraude prend le relais.

**Étapes de la revue manuelle :**

1. **Consultation du dossier complet** : pièces justificatives, score, features déclenchées, historique du device
2. **Vérification externe** : appel téléphonique au client sur le numéro déclaré, vérification employeur
3. **Analyse documentaire approfondie** : métadonnées des fichiers, cohérence des données chiffrées
4. **Consultation des bases partenaires** : bureau de crédit, registres officiels
5. **Décision motivée** : APPROVE / REJECT avec justification documentée

**SLA (Service Level Agreement) pour la revue manuelle :**
- Priorité haute (fraud score > 0.60) : réponse en < 4h ouvrées
- Priorité standard (fraud score 0.40–0.60) : réponse en < 24h ouvrées

### 5.3 Gestion des Alertes et Signalement

**Signalement interne :**
- Tout dossier confirmé comme fraude est archivé dans la base de fraudes confirmées
- Mise à jour des listes noires (IP, IBAN, email, device, numéro de téléphone)
- Partage des indicateurs de fraude avec les équipes risque et conformité

**Signalement externe (obligations légales) :**
- **TRACFIN** : déclaration de soupçon obligatoire si suspicion de blanchiment (LCB-FT)
- **Banque de France** : signalement des fraudes documentaires graves
- **Police / Justice** : dépôt de plainte pour fraude confirmée > seuil (généralement > 5 000 €)
- **FFA (France Assureurs)** / **ASF** : partage des données fraude sectorielles

---

## 6. Cas d'Usage Opérationnels

### 6.1 Cas d'Usage : Détection d'Usurpation d'Identité Simple

**Contexte :** Un client demande un prêt personnel de 12 000 €.

**Signaux détectés :**
- Adresse email créée 3 jours avant la demande ⚠️
- IP géolocalisée à Lyon, adresse déclarée à Marseille (distance : 310 km) ⚠️
- Formulaire rempli en 1 minute 12 secondes ⚠️
- Numéro de téléphone activé 8 jours avant la demande ⚠️
- Fraud score calculé : **0.74** → Zone Rouge

**Action déclenchée :** Blocage préventif + transmission au fraud analyst.

**Investigation :**
- Appel téléphonique : la vraie titulaire de l'identité répond, confirme ne pas avoir fait de demande de crédit
- Confirmation : usurpation d'identité
- Actions : rejet du dossier, mise à liste noire de l'IP et du device, signalement TRACFIN si suspicion de blanchiment

### 6.2 Cas d'Usage : Détection d'une Fraude Synthétique (Bust-Out)

**Contexte :** Un client existant depuis 18 mois avec un historique parfait demande une augmentation de sa limite revolving à 6 000 €.

**Historique du profil :**
- 18 mois de remboursements parfaits sur un crédit revolving de 1 500 €
- Taux d'utilisation toujours entre 60% et 80%
- Aucun incident, aucun signal de fraude lors de l'ouverture

**Signaux récents déclencheurs :**
- 4 demandes de crédit auprès d'autres établissements sur les 30 derniers jours ⚠️
- Demande d'augmentation de limite à son maximum ⚠️
- Changement d'adresse il y a 15 jours ⚠️
- Taux d'utilisation passé de 70% à 99% en 2 semaines ⚠️

**Pattern reconnu :** Bust-out fraud classique (phase d'exploitation après la phase de construction)

**Action :** Gel de la demande d'augmentation, revue complète du profil, contact client approfondi, surveillance renforcée des comptes liés.

### 6.3 Cas d'Usage : Détection d'un Fraud Ring

**Contexte :** Analyse des demandes reçues sur une semaine.

**Données issues du graph analytics :**
- 7 dossiers différents (7 identités différentes) partagent la même adresse IP
- 4 de ces dossiers partagent le même device fingerprint
- 3 dossiers ont le même numéro de téléphone de référence
- Les 7 demandes ont été soumises entre 2h00 et 4h00 du matin
- Montants demandés : tous entre 9 500 € et 10 000 € (juste sous le seuil de déclaration)

**Pattern reconnu :** Fraud ring structuré, possiblement avec tentative de contournement des seuils de déclaration TRACFIN (structuring).

**Actions :**
- Rejet automatique des 7 dossiers
- Mise en liste noire de l'IP, du device, du numéro de téléphone
- Déclaration de soupçon TRACFIN (structuring + fraude organisée)
- Alerte à l'équipe sécurité pour analyse approfondie du réseau

### 6.4 Cas d'Usage : Faux Positif — Client Légitime Bloqué

**Contexte :** Un client de 28 ans, étudiant récemment diplômé, fait sa première demande de crédit.

**Signaux déclenchés :**
- Adresse email créée 5 jours avant la demande (nouvelle adresse professionnelle)
- Pas d'historique de crédit (premier crédit)
- IBAN d'une néobanque (N26)
- Formulaire rempli en 1 minute 45 secondes (données saisies vite)
- Fraud score : **0.45** → Zone Orange (revue manuelle)

**Investigation :**
- Appel téléphonique : le client répond, explique son contexte (jeune diplômé)
- Vérification employeur : CDI confirmé par l'entreprise
- Liveness check réussi

**Décision :** Approbation après revue manuelle.

**Apprentissage :** Ce profil (jeune primo-accédant au crédit, néobanque, email récent) génère des faux positifs. Le modèle doit être enrichi avec un segment "primo-accédants" pour réduire le fraud score sur ce profil spécifique.

---

## 7. Réglementation et Conformité Anti-Fraude

### 7.1 LCB-FT (Lutte Contre le Blanchiment et le Financement du Terrorisme)

La LCB-FT impose aux établissements de crédit une vigilance constante sur leurs clients et leurs transactions.

**Obligations KYC (Know Your Customer) :**
- Vérification d'identité obligatoire à l'entrée en relation
- Mise à jour périodique des informations client (au moins tous les 3 ans)
- Identification du bénéficiaire effectif (UBO — Ultimate Beneficial Owner)

**Obligations de vigilance renforcée :**
- Personnes Politiquement Exposées (PPE) : contrôles additionnels obligatoires
- Pays à risque élevé (listes GAFI) : vigilance renforcée systématique
- Transactions > 10 000 € : identification obligatoire

**Déclaration de soupçon (TRACFIN) :**
- Obligation de déclarer tout soupçon de blanchiment ou financement du terrorisme
- Délai : dès la naissance du soupçon, sans délai
- Confidentialité absolue : interdiction d'informer le client ("tipping-off")

### 7.2 Directive DSP2 (Authentification Forte — SCA)

La directive sur les services de paiement 2 (DSP2) impose une authentification forte du client pour les paiements et opérations sensibles.

**Critères d'authentification forte (2 facteurs parmi 3) :**
- **Connaissance** : mot de passe, PIN, question secrète
- **Possession** : téléphone (SMS OTP), token physique
- **Inhérence** : biométrie (empreinte, reconnaissance faciale)

**Exemptions à la SCA :**
- Transactions < 30 € (cumul plafonné à 100 €)
- Bénéficiaires de confiance préalablement enregistrés
- Analyse de risque de transaction (TRA) concluant à un risque faible

### 7.3 RGPD et Données de Fraude

**Conservation des données de fraude :**
- Données de fraude confirmée : conservation jusqu'à 5 ans après la clôture du dossier
- Données de suspects non confirmés : suppression sous 1 an si pas de confirmation
- Droit d'accès RGPD : applicable, mais possible restriction si investigation en cours

**Listes noires internes :**
- Toute inscription dans une liste noire doit être documentée et justifiée
- Droit de contestation possible (sauf si procédure judiciaire en cours)
- Partage de listes noires entre établissements : encadré par des accords sectoriels (ex : GUILD, fichiers partagés FBF)

---

## 8. Glossaire

| Terme | Définition |
|---|---|
| Fraud Score | Probabilité de fraude calculée par le modèle ML (0 = pas de fraude, 1 = fraude certaine) |
| Hard Rule | Règle déterministe entraînant un rejet automatique indépendamment du score |
| Soft Rule | Règle qui augmente le score ou déclenche une surveillance sans bloquer |
| Identity Fraud | Utilisation de l'identité d'une autre personne pour obtenir frauduleusement un crédit |
| Synthetic Identity | Identité fictive créée en combinant des éléments réels et faux |
| Bust-Out Fraud | Fraude où le fraudeur construit un historique de crédit positif avant d'extraire le maximum de fonds |
| Mule Account | Compte bancaire utilisé pour recevoir et transférer des fonds frauduleux |
| Fraud Ring | Réseau organisé de fraudeurs coordonnant leurs actions |
| Device Fingerprint | Identifiant unique d'un appareil basé sur ses caractéristiques techniques |
| Velocity Check | Vérification de la fréquence d'un événement sur une fenêtre temporelle |
| Liveness Detection | Vérification biométrique confirmant qu'un selfie est bien un humain en temps réel |
| OTP | One-Time Password : code à usage unique envoyé par SMS |
| KYC | Know Your Customer : processus de vérification d'identité client |
| AML | Anti-Money Laundering : lutte contre le blanchiment d'argent |
| LCB-FT | Lutte Contre le Blanchiment et le Financement du Terrorisme |
| TRACFIN | Traitement du renseignement et action contre les circuits financiers clandestins |
| PPE | Personne Politiquement Exposée |
| Tipping-Off | Informer un suspect qu'une déclaration de soupçon a été effectuée (interdit) |
| DSP2 | Directive sur les Services de Paiement 2 — impose l'authentification forte |
| SCA | Strong Customer Authentication — authentification à deux facteurs |
| TRA | Transaction Risk Analysis — analyse permettant d'exempter la SCA |
| Precision | Part des alertes déclenchées qui sont de vraies fraudes |
| Recall | Part des fraudes réelles qui ont été détectées |
| F1-Score | Moyenne harmonique de la précision et du rappel |
| AUC-PR | Aire sous la courbe Précision-Rappel — métrique adaptée aux datasets déséquilibrés |
| False Positive | Client légitime incorrectement identifié comme fraudeur |
| False Negative | Fraude réelle non détectée par le modèle |
| Graph Analytics | Analyse des connexions entre entités pour détecter des réseaux frauduleux |
| Link Analysis | Identification des relations et nœuds centraux dans un graphe de fraude |
| Structuring | Division de transactions pour passer sous les seuils de déclaration (infraction pénale) |
