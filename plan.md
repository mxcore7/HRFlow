# 📌 HRFlow - Application Desktop de Gestion des Ressources Humaines

## 🎯 Objectif
Développer une application desktop avec interface graphique (PyQt) permettant de gérer les employés, leur présence, leurs tâches et leurs performances avec un système intelligent de KPI et de primes.

---

## 🧩 Modules principaux

### 1. Gestion des employés
- Création / modification / suppression
- Informations :
  - Nom
  - Prénom
  - Matricule (unique)
  - Poste
  - Salaire de base
  - Photo

---

### 2. Badge employé
- Génération automatique
- Contient :
  - Photo
  - Nom + prénom
  - Matricule
  - QR Code
- Export PDF / impression

---

### 3. Gestion de présence
- Pointage manuel :
  - Saisie du matricule
  - Détection automatique entrée/sortie
- Enregistrement :
  - Heure arrivée
  - Heure départ
- Calcul :
  - Durée de travail
  - Retard
- Historique des présences

---

### 4. Gestion des congés
- Demande de congé
- Validation / refus
- Suivi des jours restants

---

### 5. Gestion des tâches
- Attribution de tâches
- Statuts :
  - Assigné
  - En cours
  - Terminé
  - Livré
  - Annulé

---

### 6. Système de KPI
- Calcul basé sur :
  - % tâches complétées
  - Retards
  - Présence
- Score global sur 100

---

### 7. Gestion des salaires
- Salaire de base
- Prime automatique :
  - basée sur KPI
- Génération fiche de paie (PDF)

---

### 8. Dashboard
- Graphiques :
  - Performance employés
  - Taux de présence
  - Tâches complétées

---

### 9. Configuration
- Paramétrage KPI
- Paramétrage primes
- Gestion des rôles

---

## 🖥️ Interface utilisateur (PyQt)

- Application desktop avec :
  - Sidebar (menu)
  - Pages :
    - Dashboard
    - Employés
    - Présences
    - Tâches
    - Congés
    - Salaires
- Fenêtres modales (dialog)
- Tables dynamiques (QTableWidget / QTableView)
- Formulaires (QLineEdit, QComboBox, etc.)

---

## 🗄️ Base de données (PostgreSQL)

Tables principales :
- employees
- attendances
- leaves
- tasks
- salaries
- kpis
- users

---

## 🛠️ Technologies

- Langage : Python
- Interface : PyQt5 / PyQt6
- Base de données : PostgreSQL
- ORM : SQLAlchemy
- PDF : ReportLab
- QR Code : qrcode

---

## 🏗️ Architecture

- models/ → modèles BD
- services/ → logique métier
- ui/ → interfaces PyQt
- controllers/ → liaison UI ↔ logique
- utils/ → helpers (PDF, QR code)

---

## 🎯 Objectif final
Créer un logiciel RH desktop professionnel avec interface graphique, permettant une gestion complète des employés et une évaluation intelligente des performances.